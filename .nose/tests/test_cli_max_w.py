"""CLI exits 1 when headline W exceeds --max-w."""

import unittest
from pathlib import Path

from maintainability.__main__ import main

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


class CliMaxWTests(unittest.TestCase):
    def test_max_w_zero_fails_on_fixture(self) -> None:
        code = main(["--root", str(FIX), "--max-w", "0"])
        self.assertEqual(code, 1)

    def test_high_max_w_passes(self) -> None:
        # The raw dup fixture exits 1 (unconfirmed scan extra recopy.py).
        # With the extra confirmed in yaml, only the W gate applies.
        import shutil
        import tempfile

        tmp = Path(tempfile.mkdtemp())
        dest = tmp / "dup"
        shutil.copytree(FIX, dest)
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        ax = dest / "product/axes.yaml"
        ax.write_text(
            ax.read_text().replace(
                "- path: src/app/clone.py",
                "- path: src/app/recopy.py\n        status: confirmed\n        strength: name\n      - path: src/app/clone.py",
            )
        )
        code = main(["--root", str(dest), "--max-w", "5"])
        self.assertEqual(code, 0)

    def test_missing_registry_is_exit_2(self) -> None:
        code = main(["--root", str(FIX.parent)])
        self.assertEqual(code, 2)
