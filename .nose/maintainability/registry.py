"""Load product/axes.yaml and product/entry-points.yaml."""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path

from maintainability.model import Corpus, Mod, Unit
from maintainability.yaml_lite import load_path

LIVE_STATUS = "locked"
P_LABEL = {"high": 1.0, "medium": 0.5, "low": 0.25}

_AUTH_FORM = (
    "authority must be a block map:\n"
    "authority:\n"
    "  symbol: pkg.mod.fn\n"
    "  path: src/pkg/mod.py"
)


class RegistryError(ValueError):
    pass


class UnresolvedError(RegistryError):
    def __init__(self, axis_id: str, symbol: str, path: str, module_qname: str | None = None):
        self.axis_id = axis_id
        self.symbol = symbol
        self.path = path
        extra = f" (module {module_qname})" if module_qname else ""
        super().__init__(
            f"locked axis {axis_id!r}: authority {symbol!r} at {path} is unresolved{extra}"
        )


@dataclass(frozen=True)
class Authority:
    symbol: str
    path: str


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
    authority: Authority | None
    verifies: tuple[str, ...]
    extra_sites: tuple[ExtraSite, ...] = ()

    @property
    def live(self) -> bool:
        return self.status == LIVE_STATUS and self.authority is not None

    @property
    def authority_symbol(self) -> str | None:
        return None if self.authority is None else self.authority.symbol

    @property
    def authority_path(self) -> str | None:
        return None if self.authority is None else self.authority.path


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


@dataclass(frozen=True)
class BoundAuthority:
    symbol: str
    path: Path
    module: Mod
    unit: Unit


@dataclass(frozen=True)
class BoundAxis:
    id: str
    statement: str
    p: float
    shape: str
    authority: BoundAuthority
    verifies: tuple[Mod, ...]
    extra_sites: tuple[ExtraSite, ...]
    axis: Axis


@dataclass
class BoundRegistry:
    root: Path
    axes: tuple[BoundAxis, ...]
    unbound_locked: tuple[str, ...]
    entry_points: tuple[dict, ...]
    code_roots: tuple[Path, ...]
    exclude: tuple[Path, ...]
    confirmed_live: tuple[Path, ...]
    deployables: tuple[Path, ...]


def load_registry(root: Path) -> Registry:
    root = root.resolve()
    product = root / "product"
    axes_raw = load_path(product / "axes.yaml") or {}
    if not isinstance(axes_raw, dict):
        raise RegistryError("axes.yaml must be a map with an axes block list")
    ep_raw = load_path(product / "entry-points.yaml") or {}
    if not isinstance(ep_raw, dict):
        raise RegistryError("entry-points.yaml must be a map")
    axes = tuple(_parse_axis(item) for item in _block_list(axes_raw.get("axes"), "axes"))
    raw_eps = _block_list(ep_raw.get("entry_points"), "entry_points")
    entry_points = tuple(item for item in raw_eps if isinstance(item, dict))
    code_roots = _paths(root, ep_raw.get("code_roots"), "code_roots")
    if not code_roots:
        defaults = []
        if (root / "src").is_dir():
            defaults.append(root / "src")
        else:
            defaults.append(root)
        if (root / "tests").is_dir():
            defaults.append(root / "tests")
        code_roots = tuple(defaults)
    exclude = list(_paths(root, ep_raw.get("exclude"), "exclude"))
    nose = (root / ".nose").resolve()
    if nose.is_dir() and nose not in exclude:
        exclude.append(nose)
    exclude = tuple(exclude)
    confirmed_live = _paths(root, ep_raw.get("confirmed_live"), "confirmed_live")
    deployables = _paths(root, ep_raw.get("deployables"), "deployables")
    return Registry(
        root=root,
        axes=axes,
        entry_points=entry_points,
        code_roots=code_roots,
        exclude=exclude,
        confirmed_live=confirmed_live,
        deployables=deployables,
    )


def bind_registry(registry: Registry, corpus: Corpus) -> BoundRegistry:
    bound: list[BoundAxis] = []
    unbound: list[str] = []
    for axis in registry.axes:
        if axis.status == LIVE_STATUS and axis.authority is None:
            unbound.append(axis.id)
            continue
        if not axis.live:
            continue
        bound.append(_bind_axis(axis, registry, corpus))
    return BoundRegistry(
        root=registry.root,
        axes=tuple(bound),
        unbound_locked=tuple(unbound),
        entry_points=registry.entry_points,
        code_roots=registry.code_roots,
        exclude=registry.exclude,
        confirmed_live=registry.confirmed_live,
        deployables=registry.deployables,
    )


def _bind_axis(axis: Axis, registry: Registry, corpus: Corpus) -> BoundAxis:
    auth = axis.authority
    if auth is None:
        raise UnresolvedError(axis.id, "", "")
    auth_path = (registry.root / auth.path).resolve()
    mod = corpus.by_path.get(auth_path)
    if mod is None:
        raise UnresolvedError(axis.id, auth.symbol, auth.path)
    unit = _matching_unit(mod, auth.symbol)
    if unit is None:
        raise UnresolvedError(axis.id, auth.symbol, auth.path, mod.qname)
    if not axis.verifies:
        raise UnresolvedError(axis.id, auth.symbol, auth.path, mod.qname)
    vmods: list[Mod] = []
    for rel in axis.verifies:
        vpath = (registry.root / rel).resolve()
        vmod = corpus.by_path.get(vpath)
        if vmod is None:
            raise UnresolvedError(axis.id, auth.symbol, auth.path, mod.qname)
        vmods.append(vmod)
    return BoundAxis(
        id=axis.id,
        statement=axis.statement,
        p=axis.p,
        shape=axis.shape,
        authority=BoundAuthority(symbol=auth.symbol, path=auth_path, module=mod, unit=unit),
        verifies=tuple(vmods),
        extra_sites=axis.extra_sites,
        axis=axis,
    )


def _matching_unit(mod: Mod, symbol: str) -> Unit | None:
    for u in mod.units:
        if u.qname == symbol:
            return u
    if any(q == symbol for q, _ln in mod.assigns):
        return next(u for u in mod.units if u.kind == "module")
    return None


def _parse_axis(item: dict) -> Axis:
    if not isinstance(item, dict):
        raise RegistryError("each axes item must be a block map")
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
    extras = []
    for ex in _block_list(item.get("extra_sites"), "extra_sites", item.get("id")):
        if not isinstance(ex, dict):
            raise RegistryError(f"axis {item.get('id')!r}: extra_sites items must be maps")
        extras.append(
            ExtraSite(
                path=ex["path"],
                status=ex.get("status", "proposed"),
                strength=ex.get("strength", "name"),
                lineno=ex.get("lineno"),
            )
        )
    return Axis(
        id=item["id"],
        statement=str(item.get("statement") or ""),
        p=p,
        shape=str(item.get("shape") or ""),
        status=str(item.get("status") or "proposed"),
        authority=_parse_authority(item),
        verifies=_str_tuple(item.get("verifies"), "verifies", item.get("id")),
        extra_sites=tuple(extras),
    )


def _parse_authority(item: dict) -> Authority | None:
    if "authority" not in item:
        return None
    auth = item["authority"]
    if auth is None:
        return None
    if isinstance(auth, dict):
        symbol = auth.get("symbol")
        path = auth.get("path")
        if not isinstance(symbol, str) or not isinstance(path, str) or not symbol or not path:
            raise RegistryError(f"axis {item.get('id')!r}: {_AUTH_FORM}")
        return Authority(symbol=symbol, path=path)
    raise RegistryError(f"axis {item.get('id')!r}: {_AUTH_FORM}")


def _block_list(value, name: str, axis_id=None) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    where = f"axis {axis_id!r}: " if axis_id is not None else ""
    raise RegistryError(
        f"{where}{name} must be a block list:\n{name}:\n  - src"
    )


def _str_tuple(value, name: str, axis_id=None) -> tuple[str, ...]:
    items = _block_list(value, name, axis_id)
    return tuple(str(v) for v in items)


def _paths(root: Path, values, name: str) -> tuple[Path, ...]:
    return tuple((root / v).resolve() for v in _block_list(values, name))
