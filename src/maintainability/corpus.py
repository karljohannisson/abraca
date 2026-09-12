"""Parse project Python into modules, units, and a symbol index."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path

SKIP_DIRS = {".git", "__pycache__", ".venv", "venv", "build", "dist", ".pytest_cache"}


@dataclass
class Unit:
    qname: str
    kind: str  # module | class | function
    path: Path
    lineno: int
    end_lineno: int
    node: ast.AST


@dataclass
class Mod:
    path: Path
    qname: str
    tree: ast.Module
    source: str
    units: list[Unit] = field(default_factory=list)
    assigns: list[tuple[str, int]] = field(default_factory=list)  # qname, lineno


@dataclass
class Corpus:
    root: Path
    modules: list[Mod]
    by_path: dict[Path, Mod]
    symbols: list[tuple[str, str, Path]]  # qname, docstring_first, path


def build_corpus(root: Path, code_roots: tuple[Path, ...], exclude: tuple[Path, ...]) -> Corpus:
    files: list[Path] = []
    for base in code_roots:
        if not base.exists():
            continue
        if base.is_file() and base.suffix == ".py":
            files.append(base.resolve())
            continue
        for p in base.rglob("*.py"):
            if any(part in SKIP_DIRS for part in p.parts):
                continue
            rp = p.resolve()
            if _excluded(rp, exclude):
                continue
            files.append(rp)
    files = sorted(set(files))
    modules: list[Mod] = []
    by_path: dict[Path, Mod] = {}
    symbols: list[tuple[str, str, Path]] = []
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(path))
        except (SyntaxError, UnicodeDecodeError):
            continue
        qname = _module_qname(root, path)
        mod = Mod(path=path, qname=qname, tree=tree, source=source)
        _collect_units(mod)
        modules.append(mod)
        by_path[path] = mod
        doc = ast.get_docstring(tree) or ""
        symbols.append((qname, _first_line(doc), path))
        for unit in mod.units:
            if unit.kind in {"class", "function"}:
                d = ast.get_docstring(unit.node) or ""
                symbols.append((unit.qname, _first_line(d), path))
        for aq, _ln in mod.assigns:
            symbols.append((aq, "", path))
    return Corpus(root=root, modules=modules, by_path=by_path, symbols=symbols)


def enclosing_unit(mod: Mod, lineno: int) -> Unit:
    hits = [u for u in mod.units if u.lineno <= lineno <= u.end_lineno and u.kind == "function"]
    if hits:
        return max(hits, key=lambda u: u.lineno)
    classes = [u for u in mod.units if u.lineno <= lineno <= u.end_lineno and u.kind == "class"]
    if classes:
        return max(classes, key=lambda u: u.lineno)
    return next(u for u in mod.units if u.kind == "module")


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


def _collect_units(mod: Mod) -> None:
    end = max(getattr(mod.tree, "end_lineno", 1) or 1, 1)
    mod.units.append(Unit(mod.qname, "module", mod.path, 1, end, mod.tree))

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.stack = [mod.qname]

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            q = f"{self.stack[-1]}.{node.name}"
            mod.units.append(
                Unit(q, "class", mod.path, node.lineno, node.end_lineno or node.lineno, node)
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
                Unit(q, "function", mod.path, node.lineno, node.end_lineno or node.lineno, node)
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

    Visitor().visit(mod.tree)


def _module_qname(root: Path, path: Path) -> str:
    rel = path.resolve().relative_to(root)
    parts = list(rel.with_suffix("").parts)
    if parts and parts[0] == "src":
        parts = parts[1:]
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) or path.stem


def _first_line(doc: str) -> str:
    return doc.strip().splitlines()[0] if doc.strip() else ""


def _excluded(path: Path, exclude: tuple[Path, ...]) -> bool:
    for ex in exclude:
        try:
            path.relative_to(ex)
            return True
        except ValueError:
            continue
    return False


def is_stdlib(name: str) -> bool:
    top = name.split(".")[0]
    return top in sys.stdlib_module_names
