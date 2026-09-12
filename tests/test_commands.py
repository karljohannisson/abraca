"""verifies: tui-commands — iterate the authority."""

from chat.tui.commands import COMMANDS


def test_commands_are_read_from_authority() -> None:
    keys = [c.key for c in COMMANDS]
    assert "q" in keys
