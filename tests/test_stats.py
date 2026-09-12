"""verifies: tui-stats — iterate the authority."""

from chat.tui.stats import STATS


def test_stats_are_read_from_authority() -> None:
    assert [s.id for s in STATS] == []
