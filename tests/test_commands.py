"""verifies: tui-commands — iterate the authority."""

from chat.tui.commands import COMMANDS


def test_commands_are_read_from_authority() -> None:
    assert COMMANDS
    assert all(c.key and c.id for c in COMMANDS)
