"""The set of stats shown in the TUI may grow."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Stat:
    id: str
    label: str


STATS: tuple[Stat, ...] = ()
