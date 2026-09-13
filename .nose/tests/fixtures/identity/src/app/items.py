"""The set of items may grow."""

__all__ = ["Item", "Mode", "ITEMS"]


class Item:
    def __init__(self, name: str, extra: dict | None = None) -> None:
        self.name = name
        self.extra = extra or {}


class Mode:
    pass


ITEMS = [
    Item("alpha", extra={"path": "string"}),
    Item("beta", extra={"path": "string"}),
]
