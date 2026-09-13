"""signature_rename: reading verifies cannot certify V=0 (fail-loud unmeasured)."""

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
  - id: rename-id
    statement: Renaming the id field must break loudly at uses.
    p: 1.0
    shape: signature_rename
    status: locked
    authority:
      symbol: app.acct
      path: src/app/acct.py
    verifies:
      - tests/test_acct.py
"""

SET_GROWS_AXES = """
version: 1
axes:
  - id: rename-id
    statement: Renaming the id field must break loudly at uses.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.acct
      path: src/app/acct.py
    verifies:
      - tests/test_acct.py
"""

ENTRY = """
code_roots:
  - src
  - tests
entry_points:
  - id: main
    path: src/app/acct.py
    kind: program_start
"""

ACCT = """
class Acct:
    id: str
"""

READS_VERIFY = """
from app import acct

def test_acct():
    a = acct.Acct()
    assert hasattr(a, "id")
"""


def _score(tmp: str, axes: str) -> int:
    root = write_project(
        Path(tmp),
        axes=axes,
        entry=ENTRY,
        files={
            "src/app/__init__.py": "",
            "src/app/acct.py": ACCT,
            "tests/test_acct.py": READS_VERIFY,
        },
    )
    reg = load_registry(root)
    corpus = build_corpus(root, reg.code_roots, reg.exclude)
    bound = bind_registry(reg, corpus)
    return score_atoms(bound, corpus, headline=True).per_axis[0].V


class SignatureRenameCheckabilityTests(unittest.TestCase):
    def test_reads_gives_1_not_0(self) -> None:
        # Fail-loud is unmeasured for signature_rename, so the same
        # reading verifies that certifies set_grows at V=0 lands at V=1.
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(_score(tmp, AXES), 1)

    def test_set_grows_same_project_gets_0(self) -> None:
        # Same project, shape set_grows: reading alone certifies V=0,
        # proving the two shapes are distinguishable.
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(_score(tmp, SET_GROWS_AXES), 0)

    def test_import_only_gives_2(self) -> None:
        verify = "import app.acct\n\ndef test_x():\n    assert True\n"
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=AXES,
                entry=ENTRY,
                files={
                    "src/app/__init__.py": "",
                    "src/app/acct.py": ACCT,
                    "tests/test_acct.py": verify,
                },
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            bound = bind_registry(reg, corpus)
            self.assertEqual(score_atoms(bound, corpus, headline=True).per_axis[0].V, 2)


if __name__ == "__main__":
    unittest.main()
