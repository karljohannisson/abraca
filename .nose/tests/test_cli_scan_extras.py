"""CLI surfaces floor scan extras and fails closed when a headline k=1 hides them."""

import shutil
import tempfile
import unittest
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

    def test_fail_closed_on_hidden_scan_extra(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        dest = tmp / "dup"
        shutil.copytree(FIX, dest)
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        # Make the headline claim k=1 by removing the confirmed clone.py
        (dest / "src/app/clone.py").unlink()
        # recopy.py remains as an unconfirmed scan extra
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

    def test_fixture_lists_recopy(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        dest = tmp / "dup"
        shutil.copytree(FIX, dest)
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        (dest / "src/app/clone.py").unlink()
        self.assertEqual(main(["--root", str(dest)]), 1)


if __name__ == "__main__":
    unittest.main()
