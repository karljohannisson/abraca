"""dormant cache — no module until shape is known."""

import importlib


def test_cache_module_is_absent() -> None:
    try:
        importlib.import_module("chat.cache")
    except ModuleNotFoundError:
        return
    raise AssertionError("chat.cache must not exist while cache is dormant")
