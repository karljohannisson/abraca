"""The set of LLM API providers may grow (OpenRouter, OpenAI, Anthropic). A new vendor may reuse an existing protocol."""

from dataclasses import dataclass

from chat.api.protocol import Protocol


@dataclass(frozen=True)
class Provider:
    id: str
    protocol: Protocol
    base_url: str


PROVIDERS: tuple[Provider, ...] = (
    Provider(
        id="openrouter",
        protocol=Protocol.OPENAI_COMPAT,
        base_url="https://openrouter.ai/api/v1",
    ),
)
