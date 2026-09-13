"""Load product/axes.yaml and product/entry-points.yaml."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from maintainability.yaml_lite import load_path


class RegistryError(ValueError):
    pass

P_LABEL = {"high": 1.0, "medium": 0.5, "low": 0.25}

LIVE_STATUS = "locked"


@dataclass(frozen=True)
class ExtraSite:
    path: str
    status: str
    strength: str
    lineno: int | None = None


@dataclass(frozen=True)
class Axis:
    id: str
    statement: str
    p: float
    shape: str
    status: str
    authority_symbol: str | None
    authority_path: str | None
    verifies: tuple[str, ...] = ()
    extra_sites: tuple[ExtraSite, ...] = ()

    @property
    def live(self) -> bool:
        return self.status == LIVE_STATUS and bool(self.authority_path)


@dataclass
class Registry:
    root: Path
    axes: tuple[Axis, ...]
    entry_points: tuple[dict, ...]
    code_roots: tuple[Path, ...]
    exclude: tuple[Path, ...]
    confirmed_live: tuple[Path, ...]
    deployables: tuple[Path, ...]

    def live_axes(self) -> tuple[Axis, ...]:
        return tuple(a for a in self.axes if a.live)


def load_registry(root: Path) -> Registry:
    root = root.resolve()
    product = root / "product"
    axes_raw = load_path(product / "axes.yaml") or {}
    ep_raw = load_path(product / "entry-points.yaml") or {}
    axes = tuple(_parse_axis(item) for item in axes_raw.get("axes") or [])
    raw_eps = ep_raw.get("entry_points") or []
    if not isinstance(raw_eps, list):
        raw_eps = []
    entry_points = tuple(item for item in raw_eps if isinstance(item, dict))
    code_roots = _paths(root, ep_raw.get("code_roots"))
    if not code_roots:
        defaults = []
        if (root / "src").is_dir():
            defaults.append(root / "src")
        else:
            defaults.append(root)
        if (root / "tests").is_dir():
            defaults.append(root / "tests")
        code_roots = tuple(defaults)
    exclude = list(_paths(root, ep_raw.get("exclude")))
    nose = (root / ".nose").resolve()
    if nose.is_dir() and nose not in exclude:
        exclude.append(nose)
    exclude = tuple(exclude)
    confirmed_live = _paths(root, ep_raw.get("confirmed_live"))
    deployables = _paths(root, ep_raw.get("deployables"))
    return Registry(
        root=root,
        axes=axes,
        entry_points=entry_points,
        code_roots=code_roots,
        exclude=exclude,
        confirmed_live=confirmed_live,
        deployables=deployables,
    )


def _parse_axis(item: dict) -> Axis:
    p_raw = item.get("p", "medium")
    if isinstance(p_raw, bool):
        raise RegistryError(f"axis {item.get('id')!r}: p must be a label or a number in [0,1], not {p_raw!r}")
    if isinstance(p_raw, (int, float)):
        p = float(p_raw)
        if not math.isfinite(p) or p < 0.0 or p > 1.0:
            raise RegistryError(f"axis {item.get('id')!r}: p must be finite in [0,1], got {p_raw!r}")
    else:
        label = str(p_raw)
        if label not in P_LABEL:
            raise RegistryError(f"axis {item.get('id')!r}: unknown p {p_raw!r}")
        p = P_LABEL[label]
    auth = item.get("authority") or {}
    extras = []
    for ex in item.get("extra_sites") or []:
        extras.append(
            ExtraSite(
                path=ex["path"],
                status=ex.get("status", "proposed"),
                strength=ex.get("strength", "name"),
                lineno=ex.get("lineno"),
            )
        )
    verifies = item.get("verifies") or []
    return Axis(
        id=item["id"],
        statement=str(item.get("statement") or ""),
        p=p,
        shape=str(item.get("shape") or ""),
        status=str(item.get("status") or "proposed"),
        authority_symbol=(auth.get("symbol") if isinstance(auth, dict) else None),
        authority_path=(auth.get("path") if isinstance(auth, dict) else None),
        verifies=tuple(verifies),
        extra_sites=tuple(extras),
    )


def _paths(root: Path, values) -> tuple[Path, ...]:
    if not values:
        return ()
    return tuple((root / v).resolve() for v in values)
