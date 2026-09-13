import contextlib
import io
import os
import subprocess
import sys
import unittest
from pathlib import Path

from world.__main__ import main
from world.regions import REGIONS

EXAMPLE = Path(__file__).resolve().parents[1]


class CliTest(unittest.TestCase):
    def test_known_region_prints_countries(self) -> None:
        first_region = next(iter(REGIONS))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = main([first_region])
        self.assertEqual(code, 0)
        self.assertEqual(buf.getvalue().splitlines(), REGIONS[first_region])

    def test_unknown_region_fails(self) -> None:
        self.assertEqual(main(["Definitely-Not-A-Region"]), 1)

    def test_no_args_fails(self) -> None:
        self.assertEqual(main([]), 1)

    def test_module_entrypoint_prints_europe(self) -> None:
        r = subprocess.run(
            [sys.executable, "-m", "world", "Europe"],
            cwd=EXAMPLE,
            env={**os.environ, "PYTHONPATH": "src"},
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.splitlines(), ["Germany", "France"])

    def test_module_entrypoint_unknown_region_exits_1(self) -> None:
        r = subprocess.run(
            [sys.executable, "-m", "world", "Atlantis"],
            cwd=EXAMPLE,
            env={**os.environ, "PYTHONPATH": "src"},
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 1)
        self.assertIn("unknown region: Atlantis", r.stderr)
