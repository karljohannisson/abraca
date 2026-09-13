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
from maintainability.registry import ExtraSite, RegistryError, load_registry
from maintainability.sites import sites_for_axis
from maintainability.yaml_lite import load_path


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
    except FileNotFoundError as exc:
        print(f"missing product registry: {exc}", file=sys.stderr)
        return 2
    except RegistryError as exc:
        print(f"invalid registry: {exc}", file=sys.stderr)
        return 2
    corpus = build_corpus(root, registry.code_roots, registry.exclude)
    headline = score_atoms(registry, corpus, headline=True)
    floor = score_atoms(registry, corpus, headline=False)
    wh = combined(headline)
    wf = combined(floor)
    hidden = _hidden_extras(registry, corpus)
    if args.json:
        print(json.dumps(_as_json(headline, floor, wh, wf, hidden), indent=2))
    else:
        print(_as_text(headline, floor, wh, wf, hidden))
    if hidden:
        rel = ", ".join(sorted(str(p.relative_to(root)) for p, _ in hidden))
        print(
            "scan extras found but hidden by a headline k=1 "
            f"(delete the file(s) or confirm them as extra_sites): {rel}",
            file=sys.stderr,
        )
        return 1
    max_w = args.max_w if args.max_w is not None else _status_baseline(root)
    if max_w is not None and wh.W > max_w:
        print(f"W {wh.W:.4f} exceeds max {max_w:.4f}", file=sys.stderr)
        return 1
    return 0


def _hidden_extras(registry, corpus) -> list[tuple[Path, str]]:
    """Unconfirmed floor scan sites, i.e. what a k=1 claim would hide.

    The headline's k=1 claim comes from axes.yaml having no confirmed
    extra_sites for the axis. A scan extra is excused when the path was
    deleted or confirmed as an extra_site in yaml.
    """
    out: list[tuple[Path, str]] = []
    seen: set[Path] = set()
    for ax in registry.live_axes():
        confirmed = {(registry.root / ex.path).resolve() for ex in ax.extra_sites if ex.status == "confirmed"}
        for site in sites_for_axis(ax, registry, corpus, headline=False):
            if (
                site.origin != "scan"
                or site.path in seen
                or site.path in confirmed
                or not site.path.is_file()
            ):
                continue
            seen.add(site.path)
            out.append((site.path, ax.id))
    return out


def _status_baseline(root: Path) -> float | None:
    path = root / "product" / "status.yaml"
    if not path.is_file():
        return None
    try:
        data = load_path(path)
    except OSError:
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


def _as_text(h: AtomTotals, f: AtomTotals, wh: Combined, wf: Combined, hidden=()) -> str:
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
    if hidden:
        lines.append("")
        lines.append("scan extras (floor; confirm or delete):")
        for p, ax_id in hidden:
            lines.append(f"  {p}  (axis: {ax_id})")
    for a in h.per_axis:
        lines.append(
            f"  {a.id:18} P={a.p:.2f} k={a.k} L={a.L} S={a.S} "
            f"Z={a.Z:.1f} C={a.C:.1f} M={a.M:.1f} H={a.H:.1f} F={a.F} V={a.V}"
        )
    return "\n".join(lines)


def _as_json(h, f, wh, wf, hidden=()) -> dict:
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
        "hidden_scan_extras": [str(p) for p, _ in hidden],
    }


if __name__ == "__main__":
    raise SystemExit(main())
