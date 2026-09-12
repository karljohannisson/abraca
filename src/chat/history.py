"""History storage may be added or changed."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class History(Protocol):
    def load(self) -> list[object]: ...
    def append(self, item: object) -> None: ...


class MemoryHistory:
    def __init__(self) -> None:
        self._items: list[object] = []

    def load(self) -> list[object]:
        return list(self._items)

    def append(self, item: object) -> None:
        self._items.append(item)
