from app.items import ITEMS


def test_iterates() -> None:
    assert list(ITEMS)
