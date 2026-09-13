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
        code = main(["--root", str(FIX), "--max-w", "5"])
        self.assertEqual(code, 0)

    def test_missing_registry_is_exit_2(self) -> None:
        code = main(["--root", str(FIX.parent)])
        self.assertEqual(code, 2)
