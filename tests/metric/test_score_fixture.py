"""Score a tiny fixture project."""

from pathlib import Path

from maintainability.atoms import score_atoms
from maintainability.combined import combined
from maintainability.corpus import build_corpus
from maintainability.registry import load_registry

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


def test_dup_fixture_detects_extras_and_positive_W() -> None:
    reg = load_registry(FIX)
    corpus = build_corpus(FIX, reg.code_roots, reg.exclude)
    headline = score_atoms(reg, corpus, headline=True)
    floor = score_atoms(reg, corpus, headline=False)
    ax = headline.per_axis[0]
    assert ax.id == "countries"
    assert ax.k >= 3  # authority + recopy.py scan + clone extra
    assert ax.L >= 2
    assert ax.S >= 1  # confirmed meaning on clone
    assert ax.F == 0
    assert ax.V == 0
    assert floor.per_axis[0].k >= 2  # scan sees recopy, not necessarily clone (USA)
    wh = combined(headline)
    assert 0 < wh.W <= 5
    assert wh.mass >= 0
