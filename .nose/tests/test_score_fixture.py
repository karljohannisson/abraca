"""Score a tiny fixture project."""

import unittest
from pathlib import Path

from maintainability.atoms import score_atoms
from maintainability.combined import combined
from maintainability.corpus import build_corpus
from maintainability.registry import load_registry

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


class FixtureScoreTests(unittest.TestCase):
    def test_dup_fixture_detects_extras_and_positive_W(self) -> None:
        reg = load_registry(FIX)
        corpus = build_corpus(FIX, reg.code_roots, reg.exclude)
        headline = score_atoms(reg, corpus, headline=True)
        floor = score_atoms(reg, corpus, headline=False)
        ax = headline.per_axis[0]
        self.assertEqual(ax.id, "countries")
        self.assertGreaterEqual(ax.k, 3)
        self.assertGreaterEqual(ax.L, 2)
        self.assertGreaterEqual(ax.S, 1)
        self.assertEqual(ax.F, 0)
        self.assertEqual(ax.V, 0)
        self.assertGreaterEqual(floor.per_axis[0].k, 2)
        wh = combined(headline)
        self.assertGreater(wh.W, 0)
        self.assertLessEqual(wh.W, 5)
        self.assertGreaterEqual(wh.mass, 0)
