"""verifies: credentials — env backend looks up by provider id."""

import os

from chat.api.providers import PROVIDERS
from chat.credentials import EnvCredentials


def test_env_credentials_use_provider_id() -> None:
    provider = PROVIDERS[0]
    key = f"{provider.id.upper()}_API_KEY"
    previous = os.environ.get(key)
    os.environ[key] = "secret"
    try:
        assert EnvCredentials().secret(provider.id) == "secret"
    finally:
        if previous is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = previous
