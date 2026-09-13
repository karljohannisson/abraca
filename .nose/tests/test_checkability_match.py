"""Unrelated match must not count as fail-loud for new_variant."""

import tempfile
import unittest
from pathlib import Path

from maintainability.atoms import score_atoms
from maintainability.corpus import build_corpus
from maintainability.registry import bind_registry, load_registry
from project import write_project

AXES = """
version: 1
axes:
  - id: kinds
    statement: New kinds of widget need their own handling.
    p: 1.0
    shape: new_variant
    status: locked
    authority:
      symbol: app.kinds
      path: src/app/kinds.py
    verifies:
      - tests/test_kinds.py
"""

ENTRY = """
code_roots:
  - src
  - tests
entry_points:
  - id: main
    path: src/app/kinds.py
    kind: program_start
"""

KINDS = """
class Circle:
    pass

class Square:
    pass
"""

VERIFY = """
from app import kinds

def test_kinds():
    assert kinds.Circle is kinds.Circle
"""

UNRELATED_MATCH = """
def handle(foo):
    match foo:
        case _:
            return foo
"""


class MatchFailLoudTests(unittest.TestCase):
    def test_unrelated_wildcard_match_does_not_raise_V(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=AXES,
                entry=ENTRY,
                files={
                    "src/app/__init__.py": "",
                    "src/app/kinds.py": KINDS,
                    "src/app/other.py": UNRELATED_MATCH,
                    "tests/test_kinds.py": VERIFY,
                },
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            bound = bind_registry(reg, corpus)
            headline = score_atoms(bound, corpus, headline=True)
            self.assertEqual(headline.per_axis[0].V, 0)
