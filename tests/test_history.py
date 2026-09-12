"""verifies: history — in-memory backend implements the port."""

from chat.history import History, MemoryHistory


def test_memory_history_roundtrip() -> None:
    h: History = MemoryHistory()
    h.append("a")
    assert h.load() == ["a"]
