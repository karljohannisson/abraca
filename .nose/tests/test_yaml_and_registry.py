"""Load a product registry from the dup fixture (not a live app)."""

from pathlib import Path

from maintainability.registry import load_registry
from maintainability.yaml_lite import load


FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


def test_fixture_axes_parse() -> None:
    text = (FIX / "product/axes.yaml").read_text(encoding="utf-8")
    data = load(text)
    ids = [a["id"] for a in data["axes"]]
    assert "countries" in ids
    countries = next(a for a in data["axes"] if a["id"] == "countries")
    assert countries["p"] == "high"
    assert countries["authority"]["symbol"] == "app.countries"
    assert "tests/test_countries.py" in countries["verifies"]
    assert countries.get("origin") == "brief"


def test_registry_skips_dormant() -> None:
    reg = load_registry(FIX)
    live = {a.id for a in reg.live_axes()}
    assert "countries" in live
    assert "cache" not in live
    assert any(p.name == "src" or p.name == "app" for p in reg.code_roots)
