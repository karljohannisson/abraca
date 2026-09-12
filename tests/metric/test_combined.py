"""W composition (docs/metric.md v1)."""

from maintainability.atoms import AtomTotals, AxisScore
from maintainability.combined import combined


def test_empty_axes_W_is_volume() -> None:
    t = AtomTotals(0, 0, 0, 0, 0, 0, 0, 0, 0, 0.25, [], "headline")
    c = combined(t)
    assert abs(c.W - 0.25) < 1e-9
    assert c.mass == 0.25
    assert c.edit == 0


def test_saturated_degree_is_one_third_edit() -> None:
    ax = AxisScore("r", 1.0, k=5, extras=4, L=0, S=0, Z=0, C=0, M=0, H=0, F=0, V=0)
    t = AtomTotals(4, 0, 0, 0, 0, 0, 0, 0, 0, 0, [ax], "headline")
    c = combined(t)
    assert abs(c.means["degree"] - 1.0) < 1e-9
    assert abs(c.edit - 1.0 / 3.0) < 1e-9
    assert abs(c.W - 1.0 / 3.0) < 1e-9
