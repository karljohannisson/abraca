"""Registry rejects p outside [0,1]."""

import tempfile
import unittest
from pathlib import Path

from maintainability.registry import RegistryError, load_registry
from project import write_project

ENTRY = """
code_roots:
  - src
entry_points: []
"""


def _axes(p: str) -> str:
    return f"""
version: 1
axes:
  - id: n
    statement: Names may grow.
    p: {p}
    shape: set_grows
    status: locked
    authority:
      symbol: app.n
      path: src/app/n.py
    verifies: []
"""


class PBoundsTests(unittest.TestCase):
    def _load(self, p: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=_axes(p),
                entry=ENTRY,
                files={"src/app/n.py": "NAMES = []\n"},
            )
            load_registry(root)

    def test_p_above_one_is_rejected(self) -> None:
        with self.assertRaises(RegistryError):
            self._load("1.5")

    def test_p_negative_is_rejected(self) -> None:
        with self.assertRaises(RegistryError):
            self._load("-0.1")

    def test_p_nonfinite_is_rejected(self) -> None:
        with self.assertRaises(RegistryError):
            self._load("1.0e400")

    def test_p_zero_and_one_ok(self) -> None:
        self._load("0")
        self._load("1")
        self._load("0.0")
        self._load("1.0")
