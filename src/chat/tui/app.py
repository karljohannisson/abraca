"""TUI composition: uses chat port, commands, stats, presentation. Encodes none of them."""

from chat.api.providers import PROVIDERS
from chat.tui.commands import COMMANDS


def main() -> None:
    providers = ", ".join(p.id for p in PROVIDERS)
    keys = ", ".join(f"{c.key}={c.label}" for c in COMMANDS)
    print(f"providers: {providers}")
    print(f"commands: {keys}")
