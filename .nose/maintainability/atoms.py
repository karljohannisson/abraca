"""Ten raw atoms. Formulas: docs/principles. Combined uses these."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from maintainability import languages as lang
from maintainability.model import Corpus, Mod
from maintainability.registry import Axis, Registry
from maintainability.sites import STRENGTH_RANK, Site, sites_for_axis, unit_of_site

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
        H = mean_fanout(corpus, sites)
        F = findability(ax, corpus)
        V = checkability(ax, registry, corpus)
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
        xs.append(max(unit.statement_count - unit.working_set, 0))
    return sum(xs) / len(xs)


def mean_complexity(corpus: Corpus, sites: list[Site]) -> float:
    if not sites:
        return 0.0
    xs = [unit_of_site(corpus, s).complexity for s in sites]
    return sum(xs) / len(xs)


def mean_mixing(sites: list[Site], mixing_units: dict[str, set[str]], axis_id: str) -> float:
    if not sites:
        return 0.0
    xs = [max(len(mixing_units.get(s.unit_qname, {axis_id})) - 1, 0) for s in sites]
    return sum(xs) / len(xs)


def mean_fanout(corpus: Corpus, sites: list[Site]) -> float:
    if not sites:
        return 0.0
    this_units = {s.unit_qname for s in sites}
    xs = []
    for s in sites:
        unit = unit_of_site(corpus, s)
        refs = {r for r in unit.refs if not any(r == u or r.startswith(u + ".") or u.startswith(r + ".") for u in this_units)}
        xs.append(len(refs))
    return sum(xs) / len(xs)


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
        if qname == target:
            return min(i - 1, 50)
    for i, (_sc, qname) in enumerate(scored, start=1):
        if qname == target or qname.startswith(target + "."):
            return min(i - 1, 50)
    return 50


def query_tokens(axis: Axis) -> list[str]:
    text = f"{axis.statement} {axis.id.replace('-', ' ')}"
    raw = re.findall(r"[a-z][a-z0-9]+", text.lower())
    return [t for t in raw if t not in STOPWORDS and len(t) > 1]


def checkability(axis: Axis, registry: Registry, corpus: Corpus) -> int:
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
        if lang.mentions(vmod, auth_qname):
            imports_mod = True
        if lang.reads_authority(vmod, auth_qname):
            reads = True
    fail_applies = axis.shape == "new_variant"
    exhaustive = True
    if fail_applies:
        matches = lang.fail_loud_matches(corpus, auth_qname, auth_mod)
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
    # shape == "signature_rename": fail-loud (type/attribute errors at uses)
    # is NOT implemented (bugs/signature-rename-fail-loud.md), so a verifies
    # test that reads the authority cannot certify V=0 — the shape's
    # fail-loud half is unmeasured. Score it as V=1 (authority-driven
    # verifies without fail-loud), which stays honest and stays below
    # plain module-import (V=2), and is distinguishable from set_grows,
    # where iteration IS the correct use and reads alone give V=0.
    if axis.shape == "signature_rename":
        if reads:
            return 1
        if imports_mod:
            return 2
        return 3
    if reads:
        return 0
    if imports_mod:
        return 2
    return 3


def volume(registry: Registry, corpus: Corpus, headline: bool) -> float:
    roots: list[Path] = []
    for ep in registry.entry_points:
        if not isinstance(ep, dict):
            continue
        p = ep.get("path")
        if p:
            roots.append((registry.root / p).resolve())
    if not any(isinstance(ep, dict) and ep.get("path") for ep in registry.entry_points):
        roots.extend(lang.default_entry_paths(registry.root))
    for ax in registry.live_axes():
        roots.append((registry.root / ax.authority_path).resolve())
        for v in ax.verifies:
            roots.append((registry.root / v).resolve())
    qname_to_mod = {m.qname: m for m in corpus.modules}
    work = [p for p in roots if p in corpus.by_path]
    seen: set[Path] = set()
    reachable_paths: set[Path] = set()
    while work:
        path = work.pop()
        if path in seen:
            continue
        seen.add(path)
        reachable_paths.add(path)
        mod = corpus.by_path[path]
        for t in mod.import_edges:
            if t in qname_to_mod:
                work.append(qname_to_mod[t].path)
            parent = ".".join(t.split(".")[:-1])
            if parent in qname_to_mod:
                work.append(qname_to_mod[parent].path)
    if headline:
        reachable_paths.update(registry.confirmed_live)
    reached_stmts = 0
    total = 0
    for mod in corpus.modules:
        n = _module_statement_count(mod)
        total += n
        if mod.path in reachable_paths:
            reached_stmts += n
    if total == 0:
        return 0.0
    return (total - reached_stmts) / total


def _module_statement_count(mod: Mod) -> int:
    unit = next((u for u in mod.units if u.kind == "module"), None)
    if unit is None:
        return 0
    return unit.statement_count
