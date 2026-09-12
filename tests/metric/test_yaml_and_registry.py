"""Load this repo's product yaml."""

from pathlib import Path

from maintainability.registry import load_registry
from maintainability.yaml_lite import load


ROOT = Path(__file__).resolve().parents[2]


def test_axes_yaml_has_locked_providers() -> None:
    text = (ROOT / "product/axes.yaml").read_text(encoding="utf-8")
    data = load(text)
    ids = [a["id"] for a in data["axes"]]
    assert "providers" in ids
    providers = next(a for a in data["axes"] if a["id"] == "providers")
    assert providers["p"] == "high"
    assert providers["authority"]["symbol"] == "chat.api.providers"
    assert "tests/test_providers.py" in providers["verifies"]


def test_registry_skips_dormant_cache() -> None:
    reg = load_registry(ROOT)
    live = {a.id for a in reg.live_axes()}
    assert "providers" in live
    assert "cache" not in live
    assert any(p.name == "chat" for p in reg.code_roots)
