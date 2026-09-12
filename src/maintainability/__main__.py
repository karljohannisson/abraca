"""CLI: python -m maintainability [--root DIR] [--json]."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from maintainability import VERSION
from maintainability.atoms import AtomTotals, score_atoms
from maintainability.combined import Combined, combined
from maintainability.corpus import build_corpus
from maintainability.registry import load_registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maintainability score W (lower is cheaper).")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root (contains product/)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        registry = load_registry(root)
    except FileNotFoundError as exc:
        print(f"missing product registry: {exc}", file=sys.stderr)
        return 2
    corpus = build_corpus(root, registry.code_roots, registry.exclude)
    headline = score_atoms(registry, corpus, headline=True)
    floor = score_atoms(registry, corpus, headline=False)
    wh = combined(headline)
    wf = combined(floor)
    if args.json:
        print(json.dumps(_as_json(headline, floor, wh, wf), indent=2))
    else:
        print(_as_text(headline, floor, wh, wf))
    return 0


def _as_text(h: AtomTotals, f: AtomTotals, wh: Combined, wf: Combined) -> str:
    lines = [
        f"maintainability metric v{VERSION}",
        f"W (headline) {wh.W:.4f}   [0,5] lower=cheaper",
        f"W (floor)    {wf.W:.4f}   scanner only; not proof of zero extras",
        "",
        "groups (headline):",
        f"  edit    {wh.edit:.4f}",
        f"  load    {wh.load:.4f}",
        f"  orient  {wh.orient:.4f}",
        f"  check   {wh.check:.4f}",
        f"  mass    {wh.mass:.4f}",
        "",
        "raw atoms (headline):",
        f"  degree        {h.degree:.4f}",
        f"  locality      {h.locality:.4f}",
        f"  strength      {h.strength:.4f}",
        f"  size          {h.size:.4f}",
        f"  complexity    {h.complexity:.4f}",
        f"  mixing        {h.mixing:.4f}",
        f"  coupling      {h.coupling:.4f}",
        f"  findability   {h.findability:.4f}",
        f"  checkability  {h.checkability:.4f}",
        f"  volume        {h.volume:.4f}",
        "",
        "per-axis:",
    ]
    for a in h.per_axis:
        lines.append(
            f"  {a.id:18} P={a.p:.2f} k={a.k} L={a.L} S={a.S} "
            f"Z={a.Z:.1f} C={a.C:.1f} M={a.M:.1f} H={a.H:.1f} F={a.F} V={a.V}"
        )
    return "\n".join(lines)


def _as_json(h: AtomTotals, f: AtomTotals, wh: Combined, wf: Combined) -> dict:
    def atoms(t: AtomTotals) -> dict:
        return {
            "degree": t.degree,
            "locality": t.locality,
            "strength": t.strength,
            "size": t.size,
            "complexity": t.complexity,
            "mixing": t.mixing,
            "coupling": t.coupling,
            "findability": t.findability,
            "checkability": t.checkability,
            "volume": t.volume,
            "per_axis": [a.__dict__ for a in t.per_axis],
        }

    def comb(c: Combined) -> dict:
        return {
            "W": c.W,
            "edit": c.edit,
            "load": c.load,
            "orient": c.orient,
            "check": c.check,
            "mass": c.mass,
            "means": c.means,
        }

    return {"version": VERSION, "headline": {**atoms(h), "combined": comb(wh)}, "floor": {**atoms(f), "combined": comb(wf)}}


if __name__ == "__main__":
    raise SystemExit(main())
