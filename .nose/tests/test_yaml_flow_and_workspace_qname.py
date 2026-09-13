"""Block-only product yaml, packaging qnames, and unresolved live axes."""

from __future__ import annotations

import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from maintainability.__main__ import main
from maintainability.corpus import build_corpus
from maintainability.languages.python import (
    discover_import_roots,
    module_qname,
    reads_authority,
)
from maintainability.registry import UnresolvedError, bind_registry, load_registry
from maintainability.yaml_lite import YamlError, load
from project import write_project

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
UV = FIX / "uv_workspace"
SIMPLE = FIX / "simple_src"
NESTED = FIX / "nested_pkg"

ENTRY = """
code_roots:
  - src
  - tests
entry_points:
  - id: main
    path: src/app/n.py
    kind: program_start
"""


class FlowYamlTests(unittest.TestCase):
    def _raises_with_block_form(self, text: str) -> None:
        with self.assertRaises(YamlError) as ctx:
            load(text)
        msg = str(ctx.exception)
        self.assertIn("code_roots:", msg)
        self.assertIn("- src", msg)
        self.assertIn("verifies:", msg)
        self.assertIn("authority:", msg)

    def test_flow_code_roots_raises(self) -> None:
        self._raises_with_block_form("code_roots: [src]\n")

    def test_flow_verifies_empty_list_raises(self) -> None:
        self._raises_with_block_form("verifies: []\n")

    def test_flow_authority_map_raises(self) -> None:
        self._raises_with_block_form("authority: {symbol: a, path: b}\n")

    def test_quoted_brackets_stay_strings(self) -> None:
        self.assertEqual(load('k: "[src]"\n'), {"k": "[src]"})
        self.assertEqual(load("k: '{x}'\n"), {"k": "{x}"})


class AuthoritySchemaTests(unittest.TestCase):
    def test_authority_string_is_registry_error_naming_block_map(self) -> None:
        axes = """
version: 1
axes:
  - id: n
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority: pkg.mod
    verifies:
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(Path(tmp), axes=axes, entry=ENTRY, files={})
            from maintainability.registry import RegistryError

            with self.assertRaises(RegistryError) as ctx:
                load_registry(root)
            msg = str(ctx.exception)
            self.assertIn("authority:", msg)
            self.assertIn("symbol:", msg)
            self.assertIn("path:", msg)

    def test_authority_null_is_none(self) -> None:
        axes = """
version: 1
axes:
  - id: n
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority: null
    verifies:
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=ENTRY,
                files={"src/app/n.py": "N = 1\n"},
            )
            reg = load_registry(root)
            self.assertIsNone(reg.axes[0].authority)


class QnameTests(unittest.TestCase):
    def test_uv_workspace_tools_qname(self) -> None:
        roots = discover_import_roots(UV)
        q = module_qname(
            UV / "src/harness_engine/harness_engine/tools.py",
            repo_root=UV,
            import_roots=roots,
        )
        self.assertEqual(q, "harness_engine.tools")

    def test_simple_src_app_qname(self) -> None:
        roots = discover_import_roots(SIMPLE)
        q = module_qname(SIMPLE / "src/app/foo.py", repo_root=SIMPLE, import_roots=roots)
        self.assertEqual(q, "app.foo")

    def test_nested_package_without_workspace_is_not_collapsed(self) -> None:
        roots = discover_import_roots(NESTED)
        q = module_qname(
            NESTED / "src/pkg/pkg/foo.py",
            repo_root=NESTED,
            import_roots=roots,
        )
        self.assertEqual(q, "pkg.pkg.foo")

    def test_uv_workspace_authority_binds_and_verifies_import_is_a_read(self) -> None:
        reg = load_registry(UV)
        corpus = build_corpus(UV, reg.code_roots, reg.exclude)
        bound = bind_registry(reg, corpus)
        ax = next(a for a in bound.axes if a.id == "tools")
        self.assertEqual(ax.authority.symbol, "harness_engine.tools")
        self.assertEqual(ax.authority.unit.qname, "harness_engine.tools")
        self.assertEqual(ax.authority.module.qname, "harness_engine.tools")
        self.assertTrue(reads_authority(ax.verifies[0], ax.authority))


class UnresolvedBindTests(unittest.TestCase):
    def test_typo_symbol_is_unresolved(self) -> None:
        axes = """
version: 1
axes:
  - id: names
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.missing
      path: src/app/n.py
    verifies:
      - tests/test_n.py
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=ENTRY,
                files={
                    "src/app/n.py": "NAMES = ['x']\n",
                    "tests/test_n.py": "from app.n import NAMES\nassert NAMES\n",
                },
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            with self.assertRaises(UnresolvedError) as ctx:
                bind_registry(reg, corpus)
            self.assertIn("names", str(ctx.exception))
            self.assertIn("app.missing", str(ctx.exception))

    def test_empty_verifies_on_live_axis_is_unresolved(self) -> None:
        axes = """
version: 1
axes:
  - id: names
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.n
      path: src/app/n.py
    verifies:
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=ENTRY,
                files={"src/app/n.py": "NAMES = ['x']\n"},
            )
            reg = load_registry(root)
            corpus = build_corpus(root, reg.code_roots, reg.exclude)
            with self.assertRaises(UnresolvedError) as ctx:
                bind_registry(reg, corpus)
            self.assertIn("names", str(ctx.exception))

    def test_typo_symbol_cli_exit_2_prints_no_w(self) -> None:
        axes = """
version: 1
axes:
  - id: names
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.missing
      path: src/app/n.py
    verifies:
      - tests/test_n.py
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=ENTRY,
                files={
                    "src/app/n.py": "NAMES = ['x']\n",
                    "tests/test_n.py": "from app.n import NAMES\nassert NAMES\n",
                },
            )
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = main(["--root", str(root)])
            self.assertEqual(code, 2)
            self.assertNotIn("W (headline)", out.getvalue())
            self.assertIn("names", err.getvalue())

    def test_empty_verifies_cli_exit_2_even_when_w_baseline_null(self) -> None:
        axes = """
version: 1
axes:
  - id: names
    statement: Names may grow.
    p: 1.0
    shape: set_grows
    status: locked
    authority:
      symbol: app.n
      path: src/app/n.py
    verifies:
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = write_project(
                Path(tmp),
                axes=axes,
                entry=ENTRY,
                files={
                    "src/app/n.py": "NAMES = ['x']\n",
                    "product/status.yaml": "w_baseline: null\n",
                },
            )
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                code = main(["--root", str(root)])
            self.assertEqual(code, 2)
            self.assertNotIn("W (headline)", out.getvalue())
            self.assertIn("names", err.getvalue())


if __name__ == "__main__":
    unittest.main()
