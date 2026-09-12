"""verifies: providers — iterate the authority."""

from chat.api.protocol import Protocol
from chat.api.providers import PROVIDERS


def test_providers_are_read_from_authority() -> None:
    assert PROVIDERS
    assert all(p.id and p.protocol is Protocol.OPENAI_COMPAT for p in PROVIDERS)
