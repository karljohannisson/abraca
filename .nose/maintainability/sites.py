"""Confirmed and floor representations per axis."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from maintainability import languages as lang
from maintainability.model import Corpus, Mod, Unit, enclosing_unit
from maintainability.registry import Axis, Registry

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


def sites_for_axis(axis: Axis, registry: Registry, corpus: Corpus, headline: bool) -> list[Site]:
    if not axis.authority_path:
        return []
    auth_path = (registry.root / axis.authority_path).resolve()
    mod = corpus.by_path.get(auth_path)
    if mod is None:
        return []
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
    members = lang.seed_members(mod)
    aliases = lang.authority_aliases(corpus, mod.qname)
    seen_units = {auth_unit.qname}

    def _in_authority(qname: str) -> bool:
        return qname == mod.qname or qname.startswith(mod.qname + ".")

    for other in corpus.modules:
        for lineno, kind, token in lang.token_hits(other, members):
            unit = enclosing_unit(other, lineno)
            if _in_authority(unit.qname) or unit.qname in seen_units:
                continue
            if kind == "name" and lang.is_use(other, lineno, token, aliases, mod.qname):
                continue
            if kind == "attr" and lang.attr_is_use(other, lineno, aliases):
                continue
            if kind == "string" and lang.string_in_use_context(other, lineno, aliases):
                continue
            seen_units.add(unit.qname)
            out.append(Site(axis.id, other.path, lineno, unit.qname, "scan", "name", False))
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


def unit_of_site(corpus: Corpus, site: Site) -> Unit:
    mod = corpus.by_path[site.path]
    return enclosing_unit(mod, site.lineno)
