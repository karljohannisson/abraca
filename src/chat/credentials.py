"""How API keys are stored may change."""

import os
from typing import Protocol, runtime_checkable


@runtime_checkable
class Credentials(Protocol):
    def secret(self, provider_id: str) -> str | None: ...


class EnvCredentials:
    def secret(self, provider_id: str) -> str | None:
        specific = os.environ.get(f"{provider_id.upper()}_API_KEY")
        if specific:
            return specific
        return os.environ.get("API_KEY")
