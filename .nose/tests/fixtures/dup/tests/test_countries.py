from app.countries import COUNTRIES


def test_iterates() -> None:
    assert list(COUNTRIES)
