"""Confirmed and floor representations per axis."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

from maintainability.corpus import Corpus, Mod, enclosing_unit
from maintainability.registry import Axis, Registry

STRENGTH_RANK = {"name": 0, "meaning": 1, "position": 2, "algorithm": 3, "dynamic": 4}


@dataclass(frozen=True)
class Site:
    axis_id: str
    path: Path
    lineno: int
    unit_qname: str
    origin: str  # authority | scan | extra
    strength: str
    is_authority: bool


def sites_for_axis(axis: Axis, registry: Registry, corpus: Corpus, headline: bool) -> list[Site]:
    if not axis.authority_path:
        return []
    auth_path = (registry.root / axis.authority_path).resolve()
    mod = corpus.by_path.get(auth_path)
    if mod is None:
        return []
    # The authority *module* is one representation. Other units in that file
    # are its local shape, not extra sites.
    auth_unit = next(u for u in mod.units if u.kind == "module")
    out = [
        Site(
            axis.id,
            auth_path,
            auth_unit.lineno,
            auth_unit.qname,
            "authority",
            "name",
            True,
        )
    ]
    members = seed_members(mod)
    aliases = _authority_aliases(corpus, mod.qname)
    seen_units = {auth_unit.qname}

    def _in_authority(qname: str) -> bool:
        return qname == mod.qname or qname.startswith(mod.qname + ".")

    for other in corpus.modules:
        for lineno, kind, token in _token_hits(other, members):
            unit = enclosing_unit(other, lineno)
            if _in_authority(unit.qname) or unit.qname in seen_units:
                continue
            if kind == "name" and _is_use(other, lineno, token, aliases, mod.qname):
                continue
            if kind == "attr" and _attr_is_use(other, lineno, aliases):
                continue
            if kind == "string" and _string_in_use_context(other, lineno, aliases):
                continue
            seen_units.add(unit.qname)
            out.append(
                Site(axis.id, other.path, lineno, unit.qname, "scan", "name", False)
            )
    if headline:
        for ex in axis.extra_sites:
            if ex.status != "confirmed":
                continue
            path = (registry.root / ex.path).resolve()
            emod = corpus.by_path.get(path)
            if emod is None:
                continue
            ln = ex.lineno or 1
            unit = enclosing_unit(emod, ln)
            if _in_authority(unit.qname) or unit.qname in seen_units:
                if unit.qname in seen_units and not _in_authority(unit.qname):
                    out = [
                        s
                        if s.unit_qname != unit.qname
                        else Site(s.axis_id, s.path, s.lineno, s.unit_qname, "extra", ex.strength, False)
                        for s in out
                    ]
                continue
            seen_units.add(unit.qname)
            out.append(Site(axis.id, path, ln, unit.qname, "extra", ex.strength, False))
    return out


def seed_members(mod: Mod) -> set[str]:
    tokens: set[str] = set()

    class V(ast.NodeVisitor):
        def visit_Expr(self, node: ast.Expr) -> None:
            # skip docstrings
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                if node is (mod.tree.body[0] if mod.tree.body else None):
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
            # do not harvest strings inside helpers in the authority
            return

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            return

    V().visit(mod.tree)
    return {t for t in tokens if t and t not in {"return", "self"}}


def _token_hits(mod: Mod, members: set[str]) -> list[tuple[int, str, str]]:
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

    V().visit(mod.tree)
    return hits


def _authority_aliases(corpus: Corpus, auth_qname: str) -> dict[Path, set[str]]:
    """Local names that refer to the authority module or its imports."""
    aliases: dict[Path, set[str]] = {}
    for mod in corpus.modules:
        names: set[str] = set()
        for node in ast.walk(mod.tree):
            if isinstance(node, ast.ImportFrom):
                modname = _abs_import(mod.qname, node)
                if modname == auth_qname or (modname or "").startswith(auth_qname + "."):
                    for alias in node.names:
                        names.add(alias.asname or alias.name)
                # from pkg import module
                if modname and auth_qname.startswith(modname + "."):
                    tail = auth_qname[len(modname) + 1 :].split(".")[0]
                    for alias in node.names:
                        if (alias.name) == tail:
                            names.add(alias.asname or alias.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    n = alias.name
                    if n == auth_qname or auth_qname.startswith(n + "."):
                        names.add(alias.asname or n.split(".")[0])
        aliases[mod.path] = names
    return aliases


def _abs_import(mod_qname: str, node: ast.ImportFrom) -> str | None:
    if node.level:
        parts = mod_qname.split(".")
        # relative from this module: drop `level` packages (level 1 = sibling)
        if parts:
            parts = parts[:-1]  # module -> package
        cut = node.level - 1
        if cut:
            parts = parts[:-cut] if cut <= len(parts) else []
        base = ".".join(parts)
        if node.module:
            return f"{base}.{node.module}" if base else node.module
        return base or None
    return node.module


def _is_use(mod: Mod, lineno: int, token: str, aliases: dict[Path, set[str]], auth_qname: str) -> bool:
    imported = aliases.get(mod.path, set())
    if token in imported:
        return True
    # Name is imported member of authority
    return False


def _attr_is_use(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    imported = aliases.get(mod.path, set())
    for node in ast.walk(mod.tree):
        if not isinstance(node, ast.Attribute) or node.lineno != lineno:
            continue
        base = node.value
        if isinstance(base, ast.Name) and base.id in imported:
            return True
    return False


def _string_in_use_context(mod: Mod, lineno: int, aliases: dict[Path, set[str]]) -> bool:
    """f-string / comparison against imported member is still a recopy if the literal is the member."""
    return False


def unit_of_site(corpus: Corpus, site: Site) -> Unit:
    mod = corpus.by_path[site.path]
    return enclosing_unit(mod, site.lineno)
