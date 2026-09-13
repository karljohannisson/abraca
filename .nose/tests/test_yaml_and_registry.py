"""Load a product registry from the dup fixture (not a live app)."""

import unittest
from pathlib import Path

from maintainability.registry import load_registry
from maintainability.yaml_lite import load

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


class RegistryTests(unittest.TestCase):
    def test_fixture_axes_parse(self) -> None:
        text = (FIX / "product/axes.yaml").read_text(encoding="utf-8")
        data = load(text)
        ids = [a["id"] for a in data["axes"]]
        self.assertIn("countries", ids)
        countries = next(a for a in data["axes"] if a["id"] == "countries")
        self.assertEqual(countries["p"], "high")
        self.assertEqual(countries["authority"]["symbol"], "app.countries")
        self.assertIn("tests/test_countries.py", countries["verifies"])
        self.assertEqual(countries.get("origin"), "brief")

    def test_registry_skips_dormant(self) -> None:
        reg = load_registry(FIX)
        live = {a.id for a in reg.live_axes()}
        self.assertIn("countries", live)
        self.assertNotIn("cache", live)
        self.assertTrue(any(p.name == "src" or p.name == "app" for p in reg.code_roots))
