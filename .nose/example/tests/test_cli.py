import contextlib
import io
import unittest

from world.__main__ import main
from world.regions import REGIONS


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
