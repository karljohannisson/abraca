"""Ten raw atoms. Formulas: docs/principles. Combined uses these."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

from maintainability.complexity import cognitive_complexity
from maintainability.corpus import Corpus, Mod, statement_count, is_stdlib
from maintainability.registry import Axis, Registry
from maintainability.sites import (
    STRENGTH_RANK,
    Site,
    sites_for_axis,
    unit_of_site,
)

T_SIZE = 15
STOPWORDS = frozenset(
    """
    a an the of to for and or in on at by from with without that this these those
    be is are was were been being it its as if then than but not no nor so do does
    did doing may can will would should must now later first other others same such
    into over per via also even only own than too very just than them they we you
    i me my our your their how what when where which who why whom whose any all
    each few more most some than too until while about after before between
    """.split()
)


@dataclass
class AxisScore:
    id: str
    p: float
    k: int
    extras: int
    L: int
    S: int
    Z: float
    C: float
    M: float
    H: float
    F: int
    V: int


@dataclass
class AtomTotals:
    degree: float
    locality: float
    strength: float
    size: float
    complexity: float
    mixing: float
    coupling: float
    findability: float
    checkability: float
    volume: float
    per_axis: list[AxisScore] = field(default_factory=list)
    label: str = "headline"


def score_atoms(registry: Registry, corpus: Corpus, headline: bool) -> AtomTotals:
    site_map: dict[str, list[Site]] = {
        ax.id: sites_for_axis(ax, registry, corpus, headline) for ax in registry.live_axes()
    }
    mixing_units: dict[str, set[str]] = {}
    for ax_id, slist in site_map.items():
        for s in slist:
            mixing_units.setdefault(s.unit_qname, set()).add(ax_id)

    per: list[AxisScore] = []
    D = Lsum = Ssum = Zsum = Csum = Msum = Hsum = Fsum = Vsum = 0.0
    for ax in registry.live_axes():
        sites = site_map[ax.id]
        k = len(sites)
        extras = max(k - 1, 0)
        L = locality(registry, corpus, sites)
        S = strength(sites)
        Z = mean_excess_size(corpus, sites)
        C = mean_complexity(corpus, sites)
        M = mean_mixing(sites, mixing_units, ax.id)
        H = mean_fanout(corpus, sites, registry)
        F = findability(ax, corpus)
        V = checkability(ax, registry, corpus, sites)
        p = ax.p
        per.append(AxisScore(ax.id, p, k, extras, L, S, Z, C, M, H, F, V))
        D += p * extras
        Lsum += p * L
        Ssum += p * S
        Zsum += p * Z
        Csum += p * C
        Msum += p * M
        Hsum += p * H
        Fsum += p * F
        Vsum += p * V
    u = volume(registry, corpus, headline)
    return AtomTotals(D, Lsum, Ssum, Zsum, Csum, Msum, Hsum, Fsum, Vsum, u, per, "headline" if headline else "floor")


def locality(registry: Registry, corpus: Corpus, sites: list[Site]) -> int:
    if len(sites) <= 1:
        return 0
    paths = [_containment(registry, corpus, s) for s in sites]
    if all(p == paths[0] for p in paths):
        return 0
    # same class, different methods
    if (
        all(p[3] is not None and p[:4] == paths[0][:4] for p in paths)
        and len({p[4] for p in paths}) > 1
    ):
        return 1
    if all(p[:3] == paths[0][:3] for p in paths):
        return 2
    pkgs = [p[1] for p in paths]
    prefix = _common_prefix(pkgs)
    if prefix and all(p[0] == paths[0][0] for p in paths):
        return 3
    if all(p[0] == paths[0][0] for p in paths):
        return 4
    return 5


def _containment(registry: Registry, corpus: Corpus, site: Site) -> tuple:
    rel = site.path.resolve().relative_to(registry.root)
    parts = list(rel.with_suffix("").parts)
    if parts[:1] == ["src"]:
        parts = parts[1:]
    dep = 0
    if registry.deployables:
        rp = site.path.resolve()
        dep = next(
            (i for i, d in enumerate(registry.deployables) if _is_rel(rp, d)),
            len(registry.deployables),
        )
    pkg = tuple(parts[:-1]) if parts else ()
    module = parts[-1] if parts else site.path.stem
    unit = unit_of_site(corpus, site)
    class_name = None
    func_name = None
    if unit.kind == "function":
        bits = unit.qname.split(".")
        func_name = bits[-1]
        # class if parent unit is class
        parent = ".".join(bits[:-1])
        if any(u.qname == parent and u.kind == "class" for u in corpus.by_path[site.path].units):
            class_name = bits[-2] if len(bits) >= 2 else None
    elif unit.kind == "class":
        class_name = unit.qname.split(".")[-1]
    return (dep, pkg, module, class_name, func_name)


def _common_prefix(pkgs: list[tuple]) -> tuple:
    if not pkgs or not all(pkgs):
        return ()
    shortest = min(pkgs, key=len)
    i = 0
    for i, name in enumerate(shortest):
        if any(p[i] != name if i < len(p) else True for p in pkgs):
            return shortest[:i]
    return shortest


def _is_rel(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def strength(sites: list[Site]) -> int:
    extras = [s for s in sites if not s.is_authority]
    if not extras:
        return 0
    return max(STRENGTH_RANK.get(s.strength, 0) for s in extras)


def mean_excess_size(corpus: Corpus, sites: list[Site]) -> float:
    if not sites:
        return 0.0
    xs = []
    for s in sites:
        unit = unit_of_site(corpus, s)
        n = statement_count(unit.node)
        xs.append(max(n - T_SIZE, 0))
    return sum(xs) / len(xs)


def mean_complexity(corpus: Corpus, sites: list[Site]) -> float:
    if not sites:
        return 0.0
    xs = [cognitive_complexity(unit_of_site(corpus, s).node) for s in sites]
    return sum(xs) / len(xs)


def mean_mixing(sites: list[Site], mixing_units: dict[str, set[str]], axis_id: str) -> float:
    if not sites:
        return 0.0
    xs = [max(len(mixing_units.get(s.unit_qname, {axis_id})) - 1, 0) for s in sites]
    return sum(xs) / len(xs)


def mean_fanout(corpus: Corpus, sites: list[Site], registry: Registry) -> float:
    if not sites:
        return 0.0
    this_units = {s.unit_qname for s in sites}
    project_mods = {m.qname: m for m in corpus.modules}
    xs = []
    for s in sites:
        unit = unit_of_site(corpus, s)
        xs.append(_fanout(unit.node, unit, project_mods, this_units, corpus))
    return sum(xs) / len(xs)


def _fanout(node: ast.AST, unit, project_mods: dict, this_units: set[str], corpus: Corpus) -> int:
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
            if ch.module.split(".")[0] in {q.split(".")[0] for q in project_mods}:
                for alias in ch.names:
                    imported_project[alias.asname or alias.name] = (
                        f"{ch.module}.{alias.name}" if alias.name != "*" else ch.module
                    )
        elif isinstance(ch, ast.Import):
            for alias in ch.names:
                if not is_stdlib(alias.name):
                    imported_project[alias.asname or alias.name.split(".")[0]] = alias.name
    refs: set[str] = set()
    for ch in ast.walk(node):
        if isinstance(ch, ast.Name) and isinstance(ch.ctx, ast.Load):
            if ch.id in local:
                continue
            if ch.id in imported_project:
                target = imported_project[ch.id]
                if is_stdlib(target):
                    continue
                if any(target == u or u.startswith(target + ".") for u in this_units):
                    continue
                if target.split(".")[0] in {q.split(".")[0] for q in project_mods}:
                    refs.add(target)
        elif isinstance(ch, ast.Attribute) and isinstance(ch.ctx, ast.Load):
            if isinstance(ch.value, ast.Name) and ch.value.id in imported_project:
                target = f"{imported_project[ch.value.id]}.{ch.attr}"
                if any(target == u or u.startswith(imported_project[ch.value.id]) for u in this_units):
                    continue
                refs.add(imported_project[ch.value.id])
    return len(refs)


def findability(axis: Axis, corpus: Corpus) -> int:
    tokens = query_tokens(axis)
    scored: list[tuple[tuple[int, int], str]] = []
    for qname, doc, _path in corpus.symbols:
        n = sum(1 for t in tokens if t in qname.lower())
        m = sum(1 for t in tokens if t in doc.lower())
        scored.append(((-n, -m), qname))
    scored.sort(key=lambda x: (x[0], x[1]))
    target = axis.authority_symbol or ""
    if not target:
        return 50
    for i, (_sc, qname) in enumerate(scored, start=1):
        if qname == target or qname.startswith(target + "."):
            # prefer exact module match: first exact else first prefix
            if qname == target:
                return min(i - 1, 50)
    # second pass prefix
    for i, (_sc, qname) in enumerate(scored, start=1):
        if qname == target or qname.startswith(target + "."):
            return min(i - 1, 50)
    return 50


def query_tokens(axis: Axis) -> list[str]:
    text = f"{axis.statement} {axis.id.replace('-', ' ')}"
    raw = re.findall(r"[a-z][a-z0-9]+", text.lower())
    return [t for t in raw if t not in STOPWORDS and len(t) > 1]


def checkability(axis: Axis, registry: Registry, corpus: Corpus, sites: list[Site]) -> int:
    auth_path = (registry.root / axis.authority_path).resolve() if axis.authority_path else None
    auth_mod = corpus.by_path.get(auth_path) if auth_path else None
    auth_qname = auth_mod.qname if auth_mod else ""
    reads = False
    imports_mod = False
    for rel in axis.verifies:
        path = (registry.root / rel).resolve()
        vmod = corpus.by_path.get(path)
        if vmod is None:
            continue
        if _module_mentions(vmod, auth_qname):
            imports_mod = True
        if _reads_authority(vmod, auth_qname):
            reads = True
    fail_applies = axis.shape == "new_variant"
    exhaustive = True
    if fail_applies:
        matches = list(_matches_on_authority(corpus, auth_qname, auth_mod))
        if not matches:
            fail_applies = False
        else:
            exhaustive = all(exh for exh, _ in matches)
    if fail_applies:
        if reads and exhaustive:
            return 0
        if reads or exhaustive:
            return 1
        if imports_mod:
            return 2
        return 3
    if reads:
        return 0
    if imports_mod:
        return 2
    return 3


def _module_mentions(mod: Mod, auth_qname: str) -> bool:
    if not auth_qname:
        return False
    for node in ast.walk(mod.tree):
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
    src = mod.source
    return auth_qname.split(".")[-1] in src and any(
        auth_qname.split(".")[-1] == a.name
        for node in ast.walk(mod.tree)
        if isinstance(node, ast.ImportFrom)
        for a in node.names
    )


def _reads_authority(mod: Mod, auth_qname: str) -> bool:
    """Import of authority plus load of imported names (iterate/attr), not mere string recopy."""
    aliases: set[str] = set()
    for node in ast.walk(mod.tree):
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
    for node in ast.walk(mod.tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load) and node.id in aliases:
            return True
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id in aliases:
                return True
        if isinstance(node, ast.For) and isinstance(node.iter, ast.Name) and node.iter.id in aliases:
            return True
    return False


def _matches_on_authority(corpus: Corpus, auth_qname: str, auth_mod: Mod | None):
    variant_names: set[str] = set()
    if auth_mod:
        for u in auth_mod.units:
            if u.kind == "class" and u.qname != auth_qname:
                variant_names.add(u.qname.split(".")[-1])
        for node in ast.walk(auth_mod.tree):
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    if isinstance(t, ast.Name) and t.id.isupper():
                        variant_names.add(t.id)
    for mod in corpus.modules:
        for node in ast.walk(mod.tree):
            if isinstance(node, ast.Match):
                cases = node.cases
                has_wild = any(
                    isinstance(c.pattern, ast.MatchAs) and c.pattern.pattern is None and c.pattern.name is None
                    for c in cases
                )
                # also MatchAs with name _ 
                has_wild = has_wild or any(
                    isinstance(c.pattern, ast.MatchAs) and (c.pattern.name in {None, "_"} and c.pattern.pattern is None)
                    for c in cases
                )
                mentioned = False
                for c in cases:
                    for n in ast.walk(c.pattern):
                        if isinstance(n, ast.Name) and (n.id in variant_names or n.id == auth_qname.split(".")[-1]):
                            mentioned = True
                        if isinstance(n, ast.MatchClass) and n.cls:
                            pass
                if mentioned or _match_subject_is_auth(node, auth_qname.split(".")[-1]):
                    yield (not has_wild, mod.path)


def _match_subject_is_auth(node: ast.Match, tail: str) -> bool:
    sub = node.subject
    if isinstance(sub, ast.Name) and sub.id.lower() == tail.lower():
        return True
    return True  # conservative: if we yielded from mentioned variants


def volume(registry: Registry, corpus: Corpus, headline: bool) -> float:
    total = 0
    reachable_paths: set[Path] = set()
    roots: list[Path] = []
    for ep in registry.entry_points:
        p = ep.get("path")
        if p:
            roots.append((registry.root / p).resolve())
    for ax in registry.live_axes():
        roots.append((registry.root / ax.authority_path).resolve())
        for v in ax.verifies:
            roots.append((registry.root / v).resolve())
    qname_to_mod = {m.qname: m for m in corpus.modules}
    work = [p for p in roots if p in corpus.by_path]
    seen: set[Path] = set()
    while work:
        path = work.pop()
        if path in seen:
            continue
        seen.add(path)
        reachable_paths.add(path)
        mod = corpus.by_path[path]
        for node in ast.walk(mod.tree):
            targets: list[str] = []
            if isinstance(node, ast.ImportFrom):
                from maintainability.sites import _abs_import

                base = _abs_import(mod.qname, node)
                if base:
                    targets.append(base)
                    for a in node.names:
                        targets.append(f"{base}.{a.name}")
            elif isinstance(node, ast.Import):
                targets.extend(a.name for a in node.names)
            for t in targets:
                if t in qname_to_mod:
                    work.append(qname_to_mod[t].path)
                parent = ".".join(t.split(".")[:-1])
                if parent in qname_to_mod:
                    work.append(qname_to_mod[parent].path)
    if headline:
        reachable_paths.update(registry.confirmed_live)
    reached_stmts = 0
    for mod in corpus.modules:
        n = statement_count(mod.tree)
        total += n
        if mod.path in reachable_paths:
            reached_stmts += n
    if total == 0:
        return 0.0
    return (total - reached_stmts) / total
