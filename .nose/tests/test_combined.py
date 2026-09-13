"""W composition (.nose/docs/metric.md v1)."""

import unittest

from maintainability.atoms import AtomTotals, AxisScore
from maintainability.combined import combined


class CombinedTests(unittest.TestCase):
    def test_empty_axes_W_is_volume(self) -> None:
        t = AtomTotals(0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, [], "headline")
        c = combined(t)
        self.assertAlmostEqual(c.W, 0.25)
        self.assertEqual(c.mass, 0.25)
        self.assertEqual(c.edit, 0)

    def test_saturated_degree_is_one_third_edit(self) -> None:
        ax = AxisScore("r", 1.0, k=5, extras=4, L=0, S=0, Z=0, C=0, M=0, H=0, F=0, V=0)
        t = AtomTotals(4, 0, 0, 0, 0, 0, 0, 0, 0, 0, [ax], "headline")
        c = combined(t)
        self.assertAlmostEqual(c.means["degree"], 1.0)
        self.assertAlmostEqual(c.edit, 1.0 / 3.0)
        self.assertAlmostEqual(c.W, 1.0 / 3.0)
