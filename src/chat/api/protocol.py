"""The set of chatbot API protocols may grow (OpenAI-style, others)."""

from enum import Enum


class Protocol(Enum):
    OPENAI_COMPAT = "openai_compat"
