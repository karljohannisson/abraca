"""CLI names floor scan extras and fails before the W cap."""

import io
import json
import shutil
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from maintainability.__main__ import main

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


class CliScanExtrasTests(unittest.TestCase):
    def _copy(self) -> Path:
        tmp = Path(tempfile.mkdtemp())
        dest = tmp / "dup"
        shutil.copytree(FIX, dest)
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        return dest

    def test_fail_closed_on_unconfirmed_scan_extra(self) -> None:
        dest = self._copy()
        (dest / "src/app/clone.py").unlink()
        self.assertEqual(main(["--root", str(dest)]), 1)

    def test_passes_when_extra_confirmed_in_yaml(self) -> None:
        dest = self._copy()
        ax = dest / "product/axes.yaml"
        ax.write_text(
            ax.read_text().replace(
                "- path: src/app/clone.py",
                "- path: src/app/recopy.py\n        status: confirmed\n        strength: name\n      - path: src/app/clone.py",
            )
        )
        self.assertEqual(main(["--root", str(dest)]), 0)

    def test_passes_when_extra_deleted(self) -> None:
        dest = self._copy()
        (dest / "src/app/recopy.py").unlink()
        self.assertEqual(main(["--root", str(dest)]), 0)

    def test_fixture_lists_recopy_token_us(self) -> None:
        dest = self._copy()
        (dest / "src/app/clone.py").unlink()
        out = io.StringIO()
        err = io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["--root", str(dest)])
        self.assertEqual(code, 1)
        text = out.getvalue()
        self.assertIn("scan extras (floor; delete the listed token recopy):", text)
        self.assertIn("  countries  src/app/recopy.py:2  app.recopy  string  US", text)
        self.assertIn(
            "scan extras found: delete the listed token recopy (do not confirm a use)",
            err.getvalue(),
        )
        self.assertNotIn("W ", err.getvalue())

    def test_json_scan_extras_names_token(self) -> None:
        dest = self._copy()
        (dest / "src/app/clone.py").unlink()
        out = io.StringIO()
        with redirect_stdout(out), redirect_stderr(io.StringIO()):
            code = main(["--root", str(dest), "--json"])
        self.assertEqual(code, 1)
        data = json.loads(out.getvalue())
        self.assertNotIn("hidden_scan_extras", data)
        recopy = next(row for row in data["scan_extras"] if row["path"] == "src/app/recopy.py")
        self.assertEqual(recopy["axis"], "countries")
        self.assertEqual(recopy["lineno"], 2)
        self.assertEqual(recopy["unit"], "app.recopy")
        self.assertEqual(recopy["token"], "US")
        self.assertEqual(recopy["kind"], "string")


if __name__ == "__main__":
    unittest.main()
