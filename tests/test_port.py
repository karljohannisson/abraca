"""verifies: chat-contract — consumers import the port."""

import chat.port as port
from chat.port import ChatPort


def test_chat_port_is_the_consumer_contract() -> None:
    assert issubclass(ChatPort, object)
    assert "in-process consumers of the chat interface" in port.__doc__
