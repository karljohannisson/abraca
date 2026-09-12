"""W from raw atoms. .nose/docs/metric.md version 1."""

from __future__ import annotations

from dataclasses import dataclass

from maintainability.atoms import AtomTotals, AxisScore

CAPS = {
    "degree": 4.0,
    "locality": 5.0,
    "strength": 4.0,
    "size": 30.0,
    "complexity": 25.0,
    "mixing": 4.0,
    "coupling": 10.0,
    "findability": 50.0,
    "checkability": 3.0,
}


@dataclass
class Combined:
    W: float
    edit: float
    load: float
    orient: float
    check: float
    mass: float
    means: dict[str, float]


def combined(atoms: AtomTotals) -> Combined:
    axes = atoms.per_axis
    psum = sum(a.p for a in axes)
    means = {
        "degree": _mean(axes, lambda a: min(a.extras / CAPS["degree"], 1.0), psum),
        "locality": _mean(axes, lambda a: a.L / CAPS["locality"], psum),
        "strength": _mean(axes, lambda a: a.S / CAPS["strength"], psum),
        "size": _mean(axes, lambda a: min(a.Z / CAPS["size"], 1.0), psum),
        "complexity": _mean(axes, lambda a: min(a.C / CAPS["complexity"], 1.0), psum),
        "mixing": _mean(axes, lambda a: min(a.M / CAPS["mixing"], 1.0), psum),
        "coupling": _mean(axes, lambda a: min(a.H / CAPS["coupling"], 1.0), psum),
        "findability": _mean(axes, lambda a: a.F / CAPS["findability"], psum),
        "checkability": _mean(axes, lambda a: a.V / CAPS["checkability"], psum),
    }
    edit = (means["degree"] + means["locality"] + means["strength"]) / 3.0
    load = (means["size"] + means["complexity"] + means["mixing"] + means["coupling"]) / 4.0
    orient = means["findability"]
    check = means["checkability"]
    mass = atoms.volume
    w = edit + load + orient + check + mass
    return Combined(w, edit, load, orient, check, mass, means)


def _mean(axes: list[AxisScore], intensity, psum: float) -> float:
    if psum <= 0:
        return 0.0
    return sum(a.p * intensity(a) for a in axes) / psum
