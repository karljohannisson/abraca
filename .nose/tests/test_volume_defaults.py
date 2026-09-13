"""Empty entry_points still find main.py as a root."""

import tempfile
import unittest
from pathlib import Path

from maintainability.atoms import volume
from maintainability.corpus import build_corpus
from maintainability.registry import bind_registry, load_registry
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
    verifies:
      - tests/test_n.py
"""

ENTRY_EMPTY = """
code_roots:
  - src
  - tests
"""


class VolumeDefaultTests(unittest.TestCase):
    def test_main_py_is_a_root_when_entry_points_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=AXES,
                entry=ENTRY_EMPTY,
                files={
                    "src/app/n.py": "NAMES = ['x']\n",
                    "src/main.py": "from app import n\nprint(n.NAMES)\n",
                    "src/dead.py": "X = 1\nY = 2\n",
                    "tests/test_n.py": "from app.n import NAMES\nassert NAMES\n",
                },
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            bound = bind_registry(reg, corpus)
            u = volume(bound, corpus, headline=True)
            dead = next(m for m in corpus.modules if m.path.name == "dead.py")
            main = next(m for m in corpus.modules if m.path.name == "main.py")
            self.assertGreater(u, 0.0)
            self.assertIn(str(dead.path), {str(m.path) for m in corpus.modules})
            reachable_via_default = any("main.py" == p.name for p in [main.path])
            self.assertTrue(reachable_via_default)
            self.assertLess(u, 1.0)
