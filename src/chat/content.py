"""Message content may include non-text parts."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TextPart:
    text: str


ContentPart = TextPart
