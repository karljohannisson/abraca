"""How the user finds a model id may change (type a string now; later fetch-and-search from the provider)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRef:
    """Open string; not a closed catalog."""

    id: str
