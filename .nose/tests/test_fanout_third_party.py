"""Third-party imports must not raise coupling H."""

import tempfile
import unittest
from pathlib import Path

from maintainability.atoms import score_atoms
from maintainability.corpus import build_corpus
from maintainability.registry import load_registry
from project import write_project

AXES = """
version: 1
axes:
  - id: n
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.n
      path: src/app/n.py
    verifies: []
"""

ENTRY = """
code_roots:
  - src
entry_points:
  - id: n
    path: src/app/n.py
    kind: program_start
"""


class FanoutTests(unittest.TestCase):
    def _H(self, root: Path) -> float:
        reg = load_registry(root)
        corpus = build_corpus(root, reg.code_roots, reg.exclude)
        return score_atoms(reg, corpus, headline=True).per_axis[0].H

    def test_requests_import_does_not_increase_H(self) -> None:
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            clean = write_project(
                Path(a),
                axes=AXES,
                entry=ENTRY,
                files={"src/app/n.py": "NAMES = ['x']\n"},
            )
            dirty = write_project(
                Path(b),
                axes=AXES,
                entry=ENTRY,
                files={"src/app/n.py": "import requests\nNAMES = ['x']\nrequests.get\n"},
            )
            self.assertEqual(self._H(clean), self._H(dirty))
            self.assertEqual(self._H(dirty), 0.0)
