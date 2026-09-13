"""Python measurement backend. Fills model.Mod from ast."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

from maintainability.model import Corpus, Mod, Unit

LANGUAGE = "python"
WORKING_SET = 15
SUFFIX = ".py"


@dataclass
class Payload:
    tree: ast.Module


def parse_file(path: Path, root: Path) -> Mod | None:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return None
    qname = module_qname(root, path)
    mod = Mod(
        path=path,
        qname=qname,
        language=LANGUAGE,
        source=source,
        payload=Payload(tree),
    )
    _collect_units(mod, tree)
    _collect_import_edges(mod, tree)
    return mod


def module_qname(root: Path, path: Path) -> str:
    rel = path.resolve().relative_to(root)
    parts = list(rel.with_suffix("").parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) or path.stem


def resolve_corpus(corpus: Corpus) -> None:
    project_mods = {m.qname: m for m in corpus.modules}
    project_tops = {q.split(".")[0] for q in project_mods}
    for mod in corpus.modules:
        if mod.language != LANGUAGE or not isinstance(mod.payload, Payload):
            continue
        tree = mod.payload.tree
        for unit in mod.units:
            node = _unit_node(tree, unit, mod.qname)
            if node is None:
                continue
            unit.refs = _fanout_refs(node, unit, project_mods, project_tops)


def _unit_node(tree: ast.Module, unit: Unit, mod_qname: str) -> ast.AST | None:
    if unit.kind == "module":
        return tree
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.lineno == unit.lineno and node.name == unit.qname.split(".")[-1]:
                return node
    return None


def _fanout_refs(
    node: ast.AST, unit: Unit, project_mods: dict[str, Mod], project_tops: set[str]
) -> set[str]:
    local: set[str] = set()
    for ch in ast.walk(node):
        if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if ch is not node:
                local.add(ch.name)
        if isinstance(ch, ast.Name) and isinstance(getattr(ch, "ctx", None), ast.Store):
            local.add(ch.id)
    imported_project: dict[str, str] = {}
    for ch in ast.walk(node):
        if isinstance(ch, ast.ImportFrom) and ch.module:
            if ch.module.split(".")[0] in project_tops:
                for alias in ch.names:
                    imported_project[alias.asname or alias.name] = (
                        f"{ch.module}.{alias.name}" if alias.name != "*" else ch.module
                    )
        elif isinstance(ch, ast.Import):
            for alias in ch.names:
                if is_stdlib(alias.name):
                    continue
                top = alias.name.split(".")[0]
                if top not in project_tops and alias.name not in project_mods:
                    continue
                imported_project[alias.asname or top] = alias.name
    refs: set[str] = set()
    for ch in ast.walk(node):
        if isinstance(ch, ast.Name) and isinstance(ch.ctx, ast.Load):
            if ch.id in local:
                continue
            if ch.id in imported_project:
                target = imported_project[ch.id]
                if is_stdlib(target):
                    continue
                if target.split(".")[0] in project_tops:
                    refs.add(target)
        elif isinstance(ch, ast.Attribute) and isinstance(ch.ctx, ast.Load):
            if isinstance(ch.value, ast.Name) and ch.value.id in imported_project:
                target = imported_project[ch.value.id]
                if target.split(".")[0] in project_tops:
                    refs.add(target)
    return refs


def _collect_import_edges(mod: Mod, tree: ast.Module) -> None:
    edges: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            base = abs_import(mod.qname, node)
            if base:
                edges.append(base)
                for a in node.names:
                    edges.append(f"{base}.{a.name}")
        elif isinstance(node, ast.Import):
            edges.extend(a.name for a in node.names)
    mod.import_edges = edges


def _collect_units(mod: Mod, tree: ast.Module) -> None:
    end = max(getattr(tree, "end_lineno", 1) or 1, 1)
    mod.units.append(
        Unit(
            mod.qname,
            "module",
            mod.path,
            1,
            end,
            statement_count(tree),
            cognitive_complexity(tree),
            WORKING_SET,
            LANGUAGE,
        )
    )

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack = [mod.qname]

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            q = f"{self.stack[-1]}.{node.name}"
            mod.units.append(
                Unit(
                    q,
                    "class",
                    mod.path,
                    node.lineno,
                    node.end_lineno or node.lineno,
                    statement_count(node),
                    cognitive_complexity(node),
                    WORKING_SET,
                    LANGUAGE,
                )
            )
            self.stack.append(q)
            self.generic_visit(node)
            self.stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._fn(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._fn(node)

        def _fn(self, node) -> None:
            q = f"{self.stack[-1]}.{node.name}"
            mod.units.append(
                Unit(
                    q,
                    "function",
                    mod.path,
                    node.lineno,
                    node.end_lineno or node.lineno,
                    statement_count(node),
                    cognitive_complexity(node),
                    WORKING_SET,
                    LANGUAGE,
                )
            )
            self.stack.append(q)
            self.generic_visit(node)
            self.stack.pop()

        def visit_Assign(self, node: ast.Assign) -> None:
            if self.stack[-1] == mod.qname:
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        mod.assigns.append((f"{mod.qname}.{t.id}", node.lineno))
            self.generic_visit(node)

        def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
            if self.stack[-1] == mod.qname and isinstance(node.target, ast.Name):
                mod.assigns.append((f"{mod.qname}.{node.target.id}", node.lineno))
            self.generic_visit(node)

    Visitor().visit(tree)


def statement_count(node: ast.AST) -> int:
    body = getattr(node, "body", None)
    if body is None:
        return 0
    n = 0
    for stmt in body:
        n += 1
        if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        n += _nested_stmts(stmt)
    return n


def _nested_stmts(stmt: ast.stmt) -> int:
    n = 0
    for ch in ast.iter_child_nodes(stmt):
        if isinstance(ch, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(ch, ast.stmt):
            n += 1
            n += _nested_stmts(ch)
    return n


def cognitive_complexity(node: ast.AST) -> int:
    visitor = _Cog(self_names=_defined_functions(node))
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        for child in node.body:
            visitor.visit(child)
    elif isinstance(node, ast.ClassDef):
        return 0
    else:
        visitor.visit(node)
    return visitor.score


def _defined_functions(node: ast.AST) -> set[str]:
    names: set[str] = set()
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        names.add(node.name)
    return names


class _Cog(ast.NodeVisitor):
    def __init__(self, self_names: set[str]) -> None:
        self.score = 0
        self.nesting = 0
        self.self_names = self_names

    def _inc(self, extra_nest: bool = True) -> None:
        self.score += 1 + (self.nesting if extra_nest else 0)

    def visit_If(self, node: ast.If) -> None:
        self._inc()
        self.nesting += 1
        for s in node.body:
            self.visit(s)
        self.nesting -= 1
        orelse = node.orelse
        while orelse and len(orelse) == 1 and isinstance(orelse[0], ast.If):
            self.score += 1
            inner = orelse[0]
            self.nesting += 1
            for s in inner.body:
                self.visit(s)
            self.nesting -= 1
            orelse = inner.orelse
        if orelse:
            self.score += 1
            self.nesting += 1
            for s in orelse:
                self.visit(s)
            self.nesting -= 1

    def visit_For(self, node: ast.For) -> None:
        self._loop(node)

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._loop(node)

    def visit_While(self, node: ast.While) -> None:
        self._loop(node)

    def _loop(self, node) -> None:
        self._inc()
        self.nesting += 1
        for s in node.body:
            self.visit(s)
        self.nesting -= 1
        if node.orelse:
            self.score += 1
            for s in node.orelse:
                self.visit(s)

    def visit_Try(self, node: ast.Try) -> None:
        for s in node.body:
            self.visit(s)
        for h in node.handlers:
            self._inc()
            self.nesting += 1
            for s in h.body:
                self.visit(s)
            self.nesting -= 1
        for s in node.orelse:
            self.visit(s)
        for s in node.finalbody:
            self.visit(s)

    def visit_Match(self, node: ast.Match) -> None:
        self._inc()
        self.nesting += 1
        for case in node.cases:
            self.score += 1
            for s in case.body:
                self.visit(s)
        self.nesting -= 1

    def visit_IfExp(self, node: ast.IfExp) -> None:
        self._inc()
        self.generic_visit(node)

    def visit_comprehension(self, node: ast.comprehension) -> None:
        for iff in node.ifs:
            self._inc()
            self.visit(iff)
        self.visit(node.iter)
        self.visit(node.target)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        extra = len(node.values) - 1
        if extra > 0:
            self.score += extra
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        name = None
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            name = func.attr
        if name and name in self.self_names:
            self.score += 1
        self.generic_visit(node)


def seed_members(mod: Mod) -> set[str]:
    tree = _tree(mod)
    if tree is None:
        return set()
    tokens: set[str] = set()

    class V(ast.NodeVisitor):
        def visit_Expr(self, node: ast.Expr) -> None:
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if node is (tree.body[0] if tree.body else None):
                    return
            self.generic_visit(node)

        def visit_Constant(self, node: ast.Constant) -> None:
            if isinstance(node.value, str) and 2 <= len(node.value) <= 80 and " " not in node.value:
                tokens.add(node.value)
                tokens.add(node.value.lower())

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            bases = [b.id if isinstance(b, ast.Name) else "" for b in node.bases]
            if "Enum" in bases:
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign):
                        for t in stmt.targets:
                            if isinstance(t, ast.Name):
                                tokens.add(t.id)
                self.generic_visit(node)
                return
            tokens.add(node.name)
            self.generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

    V().visit(tree)
    return {t for t in tokens if t and t not in {"return", "self"}}


def token_hits(mod: Mod, members: set[str]) -> list[tuple[int, str, str]]:
    tree = _tree(mod)
    if tree is None:
        return []
    hits: list[tuple[int, str, str]] = []
    lower_members = {m.lower() for m in members}

    class V(ast.NodeVisitor):
        def visit_Constant(self, node: ast.Constant) -> None:
            if isinstance(node.value, str) and node.value.lower() in lower_members:
                hits.append((node.lineno, "string", node.value))

        def visit_Name(self, node: ast.Name) -> None:
            if node.id in members:
                hits.append((node.lineno, "name", node.id))

        def visit_Attribute(self, node: ast.Attribute) -> None:
            if node.attr in members:
                hits.append((node.lineno, "attr", node.attr))
            self.generic_visit(node)

    V().visit(tree)
    return hits


def authority_aliases(corpus: Corpus, auth_qname: str) -> dict[Path, set[str]]:
    aliases: dict[Path, set[str]] = {}
    for mod in corpus.modules:
        if mod.language != LANGUAGE:
            continue
        tree = _tree(mod)
        if tree is None:
            continue
        names: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                modname = abs_import(mod.qname, node)
                if modname == auth_qname or (modname or "").startswith(auth_qname + "."):
                    for alias in node.names:
                        names.add(alias.asname or alias.name)
                if modname and auth_qname.startswith(modname + "."):
                    tail = auth_qname[len(modname) + 1 :].split(".")[0]
                    for alias in node.names:
                        if alias.name == tail:
                            names.add(alias.asname or alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    n = alias.name
                    if n == auth_qname or auth_qname.startswith(n + "."):
                        names.add(alias.asname or n.split(".")[0])
        aliases[mod.path] = names
    return aliases


def abs_import(mod_qname: str, node: ast.ImportFrom) -> str | None:
    if node.level:
        parts = mod_qname.split(".")
        if parts:
            parts = parts[:-1]
        cut = node.level - 1
        if cut:
            parts = parts[:-cut] if cut <= len(parts) else []
        base = ".".join(parts)
        if node.module:
            return f"{base}.{node.module}" if base else node.module
        return base or None
    return node.module


def is_use(mod: Mod, lineno: int, token: str, aliases: dict[Path, set[str]], auth_qname: str) -> bool:
    imported = aliases.get(mod.path, set())
    return token in imported


def attr_is_use(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    imported = aliases.get(mod.path, set())
    tree = _tree(mod)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute) or node.lineno != lineno:
            continue
        base = node.value
        if isinstance(base, ast.Name) and base.id in imported:
            return True
    return False


def string_in_use_context(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    return False


def mentions(mod: Mod, auth_qname: str) -> bool:
    if not auth_qname:
        return False
    tree = _tree(mod)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == auth_qname or node.module.startswith(auth_qname + "."):
                return True
            tail = auth_qname.split(".")[-1]
            if node.module.endswith("." + ".".join(auth_qname.split(".")[:-1]) or "") or any(
                a.name == tail for a in node.names
            ):
                if auth_qname.startswith((node.module or "") + ".") or node.module == ".".join(
                    auth_qname.split(".")[:-1]
                ):
                    return True
        if isinstance(node, ast.Import):
            if any(a.name == auth_qname or auth_qname.startswith(a.name + ".") for a in node.names):
                return True
    return auth_qname.split(".")[-1] in mod.source and any(
        auth_qname.split(".")[-1] == a.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for a in node.names
    )


def reads_authority(mod: Mod, auth_qname: str) -> bool:
    tree = _tree(mod)
    if tree is None:
        return False
    aliases: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == auth_qname or (
                node.module == ".".join(auth_qname.split(".")[:-1])
                and any(a.name == auth_qname.split(".")[-1] for a in node.names)
            ):
                for a in node.names:
                    aliases.add(a.asname or a.name)
        if isinstance(node, ast.Import):
            for a in node.names:
                if a.name == auth_qname:
                    aliases.add(a.asname or a.name.split(".")[-1])
    if not aliases:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in aliases:
            return True
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id in aliases:
                return True
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Name) and node.iter.id in aliases:
            return True
    return False


def fail_loud_matches(corpus: Corpus, auth_qname: str, auth_mod: Mod | None) -> list[tuple[bool, Path]]:
    variant_names: set[str] = set()
    if auth_mod:
        for u in auth_mod.units:
            if u.kind == "class" and u.qname != auth_qname:
                variant_names.add(u.qname.split(".")[-1])
        tree = _tree(auth_mod)
        if tree is not None:
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for t in node.targets:
                        if isinstance(t, ast.Name) and t.id.isupper():
                            variant_names.add(t.id)
    out: list[tuple[bool, Path]] = []
    tail = auth_qname.split(".")[-1]
    for mod in corpus.modules:
        tree = _tree(mod)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Match):
                continue
            has_wild = any(
                isinstance(c.pattern, ast.MatchAs)
                and c.pattern.pattern is None
                and c.pattern.name in {None, "_"}
                for c in node.cases
            )
            mentioned = False
            for c in node.cases:
                for n in ast.walk(c.pattern):
                    if isinstance(n, ast.Name) and (n.id in variant_names or n.id == tail):
                        mentioned = True
            if mentioned or _match_subject_is_auth(node, tail):
                out.append((not has_wild, mod.path))
    return out


def _match_subject_is_auth(node: ast.Match, tail: str) -> bool:
    sub = node.subject
    if isinstance(sub, ast.Name) and sub.id.lower() == tail.lower():
        return True
    if isinstance(sub, ast.Attribute) and sub.attr.lower() == tail.lower():
        return True
    return False


def default_entry_paths(root: Path, skip_dirs: set[str]) -> list[Path]:
    found: list[Path] = []
    names = {"__main__.py", "main.py", "app.py"}
    if root.is_dir():
        for p in root.rglob("*.py"):
            if any(part in skip_dirs for part in p.parts):
                continue
            if p.name in names:
                found.append(p.resolve())
    pyproject = root / "pyproject.toml"
    if pyproject.is_file():
        found.extend(_scripts_from_pyproject(root, pyproject))
    return found


def _scripts_from_pyproject(root: Path, path: Path) -> list[Path]:
    text = path.read_text(encoding="utf-8")
    in_scripts = False
    out: list[Path] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_scripts = stripped in {"[project.scripts]", "[project.gui-scripts]"}
            continue
        if not in_scripts or "=" not in stripped:
            continue
        rhs = stripped.split("=", 1)[1].strip().strip("\"'")
        mod = rhs.split(":")[0].strip()
        rel = Path(*mod.split("."))
        for candidate in (root / "src" / rel.with_suffix(".py"), root / rel.with_suffix(".py")):
            if candidate.is_file():
                out.append(candidate.resolve())
    return out


def first_line_doc(tree: ast.AST) -> str:
    doc = ast.get_docstring(tree) or ""
    return doc.strip().splitlines()[0] if doc.strip() else ""


def symbol_docs(mod: Mod) -> list[tuple[str, str]]:
    tree = _tree(mod)
    if tree is None:
        return []
    out = [(mod.qname, first_line_doc(tree))]
    for unit in mod.units:
        if unit.kind not in {"class", "function"}:
            continue
        node = _unit_node(tree, unit, mod.qname)
        if node is None:
            continue
        d = ast.get_docstring(node) or ""
        out.append((unit.qname, d.strip().splitlines()[0] if d.strip() else ""))
    for aq, _ln in mod.assigns:
        out.append((aq, ""))
    return out


def _tree(mod: Mod) -> ast.Module | None:
    if isinstance(mod.payload, Payload):
        return mod.payload.tree
    return None


def is_stdlib(name: str) -> bool:
    top = name.split(".")[0]
    return top in sys.stdlib_module_names
