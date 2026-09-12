"""verifies: protocols — exhaustive on the authority."""

from chat.api.protocol import Protocol


def test_every_protocol_variant_is_handled() -> None:
    handled: list[Protocol] = []
    for protocol in Protocol:
        match protocol:
            case Protocol.OPENAI_COMPAT:
                handled.append(protocol)
    assert handled == list(Protocol)
