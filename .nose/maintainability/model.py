"""Language-neutral program model the atoms score."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Unit:
    qname: str
    kind: str
    path: Path
    lineno: int
    end_lineno: int
    statement_count: int
    complexity: int
    working_set: int
    language: str
    refs: set[str] = field(default_factory=set)


@dataclass
class Mod:
    path: Path
    qname: str
    language: str
    source: str
    units: list[Unit] = field(default_factory=list)
    assigns: list[tuple[str, int]] = field(default_factory=list)
    import_edges: list[str] = field(default_factory=list)
    payload: object | None = None


@dataclass
class Corpus:
    root: Path
    modules: list[Mod]
    by_path: dict[Path, Mod]
    symbols: list[tuple[str, str, Path]]


def enclosing_unit(mod: Mod, lineno: int) -> Unit:
    hits = [u for u in mod.units if u.lineno <= lineno <= u.end_lineno and u.kind == "function"]
    if hits:
        return max(hits, key=lambda u: u.lineno)
    classes = [u for u in mod.units if u.lineno <= lineno <= u.end_lineno and u.kind == "class"]
    if classes:
        return max(classes, key=lambda u: u.lineno)
    return next(u for u in mod.units if u.kind == "module")
