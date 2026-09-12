"""verifies: providers — iterate the authority."""

from chat.api.protocol import Protocol
from chat.api.providers import PROVIDERS


def test_providers_are_read_from_authority() -> None:
    ids = [p.id for p in PROVIDERS]
    assert "openrouter" in ids
    assert all(p.protocol is Protocol.OPENAI_COMPAT for p in PROVIDERS)
