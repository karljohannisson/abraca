"""The set of in-process consumers of the chat interface may grow (TUI now; other Python UIs later)."""

from collections.abc import Iterator
from typing import Protocol


class ChatPort(Protocol):
    def send(self, text: str) -> Iterator[str]:
        """Always streaming token/text chunks."""
