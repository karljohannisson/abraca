"""Identity harvest and imported-authority reads are uses, not extras."""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from maintainability.__main__ import main
from maintainability.atoms import score_atoms
from maintainability.corpus import build_corpus
from maintainability.languages.python import seed_members
from maintainability.registry import bind_registry, load_registry
from maintainability.sites import extra_hits_for_axis, sites_for_axis
from project import write_project

FIX = Path(__file__).resolve().parent / "fixtures" / "identity"


class IdentityFixtureTests(unittest.TestCase):
    def _bound(self):
        reg = load_registry(FIX)
        corpus = build_corpus(FIX, reg.code_roots, reg.exclude)
        bound = bind_registry(reg, corpus)
        ax = next(a for a in bound.axes if a.id == "items")
        return bound, corpus, ax

    def test_schema_and_type_names_are_not_members(self) -> None:
        bound, corpus, ax = self._bound()
        members = seed_members(ax.authority.module)
        self.assertIn("alpha", members.strings)
        self.assertIn("beta", members.strings)
        self.assertNotIn("path", members.strings)
        self.assertNotIn("string", members.strings)
        self.assertNotIn("path", members.names)
        self.assertNotIn("Mode", members.names)
        self.assertNotIn("Item", members.names)
        self.assertNotIn("ITEMS", members.names)

    def test_compose_and_iterate_verifies_are_not_scan_extras(self) -> None:
        bound, corpus, ax = self._bound()
        extras = extra_hits_for_axis(ax, bound, corpus)
        extra_names = {hit.path.name for hit in extras}
        self.assertNotIn("compose.py", extra_names)
        self.assertNotIn("test_items.py", extra_names)
        self.assertIn("recopy.py", extra_names)
        self.assertIn("test_recopy_assert.py", extra_names)
        recopy = next(hit for hit in extras if hit.path.name == "recopy.py")
        self.assertEqual(recopy.token, "alpha")
        self.assertEqual(recopy.kind, "string")
        sites = sites_for_axis(ax, bound, corpus, headline=False)
        site_names = {s.path.name for s in sites}
        self.assertNotIn("compose.py", site_names)
        self.assertNotIn("test_items.py", site_names)

    def test_cli_lists_alpha_recopy_and_json_scan_extras(self) -> None:
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--root", str(FIX)])
        self.assertEqual(code, 1)
        text = out.getvalue()
        self.assertIn("scan extras (floor; delete the listed token recopy):", text)
        self.assertIn("  items  src/app/recopy.py:", text)
        self.assertIn("  string  alpha", text)
        self.assertNotIn("compose.py", text)
        self.assertNotIn("test_items.py", text)
        self.assertIn(
            "scan extras found: delete the listed token recopy (do not confirm a use)",
            err.getvalue(),
        )
        jout = io.StringIO()
        with redirect_stdout(jout), redirect_stderr(io.StringIO()):
            jcode = main(["--root", str(FIX), "--json"])
        self.assertEqual(jcode, 1)
        data = json.loads(jout.getvalue())
        self.assertNotIn("hidden_scan_extras", data)
        paths = {row["path"] for row in data["scan_extras"]}
        self.assertIn("src/app/recopy.py", paths)
        self.assertTrue(any(row["token"] == "alpha" for row in data["scan_extras"]))
        self.assertNotIn("src/app/compose.py", paths)


class ReadsAuthorityTests(unittest.TestCase):
    def test_import_package_then_attribute_is_a_read(self) -> None:
        axes = """
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
        entry = """
code_roots:
  - src
  - tests
entry_points:
  - id: n
    path: src/app/n.py
    kind: program_start
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=entry,
                files={
                    "src/app/__init__.py": "",
                    "src/app/n.py": 'NAMES = {"x": 1}\n',
                    "tests/test_n.py": "import app\n\ndef test_n():\n    assert app.n.NAMES\n",
                },
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            bound = bind_registry(reg, corpus)
            headline = score_atoms(bound, corpus, headline=True)
            self.assertEqual(headline.per_axis[0].V, 0)
