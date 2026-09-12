"""The set of TUI commands and keybindings may grow."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Command:
    id: str
    key: str
    label: str


COMMANDS: tuple[Command, ...] = (
    Command(id="quit", key="q", label="Quit"),
)
