"""Confirmed and floor representations per axis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from maintainability import languages as lang
from maintainability.languages import Hit
from maintainability.model import Corpus, Mod, Unit, enclosing_unit
from maintainability.registry import BoundAxis, BoundRegistry

STRENGTH_RANK = {"name": 0, "meaning": 1, "position": 2, "algorithm": 3, "dynamic": 4}


@dataclass(frozen=True)
class Site:
    axis_id: str
    path: Path
    lineno: int
    unit_qname: str
    origin: str
    strength: str
    is_authority: bool


@dataclass(frozen=True)
class ExtraHit:
    axis: str
    path: Path
    lineno: int
    unit: str
    token: str
    kind: str


def _in_authority(mod_qname: str, qname: str) -> bool:
    return qname == mod_qname or qname.startswith(mod_qname + ".")


def _scan_recopy_hits(axis: BoundAxis, corpus: Corpus) -> list[tuple[Mod, Hit, Unit]]:
    auth_unit = axis.authority.unit
    mod = axis.authority.module
    members = lang.seed_members(mod)
    aliases = lang.authority_aliases(corpus, axis.authority)
    seen_units = {auth_unit.qname}
    out: list[tuple[Mod, Hit, Unit]] = []
    for other in corpus.modules:
        for hit in lang.token_hits(other, members):
            unit = enclosing_unit(other, hit.lineno)
            if _in_authority(mod.qname, unit.qname) or unit.qname in seen_units:
                continue
            if lang.hit_is_use(other, hit, aliases):
                continue
            seen_units.add(unit.qname)
            out.append((other, hit, unit))
    return out


def extra_hits_for_axis(axis: BoundAxis, registry: BoundRegistry, corpus: Corpus) -> list[ExtraHit]:
    confirmed = {(registry.root / ex.path).resolve() for ex in axis.extra_sites if ex.status == "confirmed"}
    out: list[ExtraHit] = []
    for other, hit, unit in _scan_recopy_hits(axis, corpus):
        if other.path in confirmed or not other.path.is_file():
            continue
        out.append(ExtraHit(axis.id, other.path, hit.lineno, unit.qname, hit.token, hit.kind))
    return out


def sites_for_axis(axis: BoundAxis, registry: BoundRegistry, corpus: Corpus, headline: bool) -> list[Site]:
    auth_unit = axis.authority.unit
    auth_path = axis.authority.path
    mod = axis.authority.module
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
    seen_units = {auth_unit.qname}
    for other, hit, unit in _scan_recopy_hits(axis, corpus):
        seen_units.add(unit.qname)
        out.append(Site(axis.id, other.path, hit.lineno, unit.qname, "scan", "name", False))
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
            if _in_authority(mod.qname, unit.qname) or unit.qname in seen_units:
                if unit.qname in seen_units and not _in_authority(mod.qname, unit.qname):
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


def unit_of_site(corpus: Corpus, site: Site) -> Unit:
    mod = corpus.by_path[site.path]
    return enclosing_unit(mod, site.lineno)
