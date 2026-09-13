"""CLI: PYTHONPATH=.nose python3 -m maintainability [--root DIR] [--json] [--max-w W]."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from maintainability import VERSION
from maintainability.atoms import AtomTotals, score_atoms
from maintainability.combined import Combined, combined
from maintainability.corpus import build_corpus
from maintainability.registry import RegistryError, UnresolvedError, bind_registry, load_registry
from maintainability.sites import ExtraHit, extra_hits_for_axis
from maintainability.yaml_lite import YamlError, load_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maintainability score W (lower is cheaper).")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root (contains product/)")
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--max-w",
        type=float,
        default=None,
        help="Fail with exit 1 if headline W exceeds this. Default: product/status.yaml w_baseline when set.",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        registry = load_registry(root)
        corpus = build_corpus(root, registry.code_roots, registry.exclude)
        bound = bind_registry(registry, corpus)
    except FileNotFoundError as exc:
        print(f"missing product registry: {exc}", file=sys.stderr)
        return 2
    except (RegistryError, UnresolvedError, YamlError) as exc:
        print(f"invalid registry: {exc}", file=sys.stderr)
        return 2
    max_w = args.max_w if args.max_w is not None else _status_baseline(root)
    if max_w is not None and bound.unbound_locked:
        ids = ", ".join(bound.unbound_locked)
        print(
            "invalid registry: locked rows need authority {symbol, path} "
            f"and a verifies path that exists: {ids}",
            file=sys.stderr,
        )
        return 2
    headline = score_atoms(bound, corpus, headline=True)
    floor = score_atoms(bound, corpus, headline=False)
    wh = combined(headline)
    wf = combined(floor)
    extras = _scan_extras(bound, corpus)
    if args.json:
        print(json.dumps(_as_json(headline, floor, wh, wf, extras, root), indent=2))
    else:
        print(_as_text(headline, floor, wh, wf, extras, root))
    if extras:
        print(
            "scan extras found: delete the listed token recopy (do not confirm a use)",
            file=sys.stderr,
        )
        return 1
    if max_w is not None and wh.W > max_w:
        print(f"W {wh.W:.4f} exceeds max {max_w:.4f}", file=sys.stderr)
        return 1
    return 0


def _scan_extras(registry, corpus) -> list[ExtraHit]:
    out: list[ExtraHit] = []
    for ax in registry.axes:
        out.extend(extra_hits_for_axis(ax, registry, corpus))
    return out


def _rel(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _status_baseline(root: Path) -> float | None:
    path = root / "product" / "status.yaml"
    if not path.is_file():
        return None
    try:
        data = load_path(path)
    except (OSError, YamlError):
        return None
    if not isinstance(data, dict):
        return None
    raw = data.get("w_baseline")
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _as_text(h: AtomTotals, f: AtomTotals, wh: Combined, wf: Combined, extras=(), root: Path | None = None) -> str:
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
    if extras:
        lines.append("")
        lines.append("scan extras (floor; delete the listed token recopy):")
        for hit in extras:
            rel = _rel(hit.path, root) if root is not None else str(hit.path)
            lines.append(f"  {hit.axis}  {rel}:{hit.lineno}  {hit.unit}  {hit.kind}  {hit.token}")
    return "\n".join(lines)


def _as_json(h, f, wh, wf, extras=(), root: Path | None = None) -> dict:
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

    return {
        "version": VERSION,
        "headline": {**atoms(h), "combined": comb(wh)},
        "floor": {**atoms(f), "combined": comb(wf)},
        "scan_extras": [
            {
                "axis": hit.axis,
                "path": _rel(hit.path, root) if root is not None else str(hit.path),
                "lineno": hit.lineno,
                "unit": hit.unit,
                "token": hit.token,
                "kind": hit.kind,
            }
            for hit in extras
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main())
