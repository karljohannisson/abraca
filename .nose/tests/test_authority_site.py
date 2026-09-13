"""The authority site lands on the enclosing unit of authority.symbol."""

import unittest
from pathlib import Path

from maintainability.corpus import build_corpus
from maintainability.registry import bind_registry, load_registry
from maintainability.sites import sites_for_axis

FIX = Path(__file__).resolve().parent / "fixtures" / "dup"


class AuthoritySiteTests(unittest.TestCase):
    def _sites(self, axis_id: str, headline: bool = True):
        reg = load_registry(FIX)
        corpus = build_corpus(FIX, reg.code_roots, reg.exclude)
        bound = bind_registry(reg, corpus)
        ax = next(a for a in bound.axes if a.id == axis_id)
        return sites_for_axis(ax, bound, corpus, headline)

    def test_authority_site_is_function_when_symbol_is_a_function(self) -> None:
        site = self._sites("report-formats")[0]
        self.assertEqual(site.unit_qname, "app.reports.build_report_format_registry")

    def test_authority_site_scores_the_function_not_the_file(self) -> None:
        reg = load_registry(FIX)
        corpus = build_corpus(FIX, reg.code_roots, reg.exclude)
        bound = bind_registry(reg, corpus)
        ax = next(a for a in bound.axes if a.id == "report-formats")
        site = sites_for_axis(ax, bound, corpus, True)[0]
        unit = next(u for u in corpus.by_path[site.path].units if u.qname == site.unit_qname)
        self.assertEqual(unit.kind, "function")
        self.assertEqual(unit.statement_count, 6)
        self.assertEqual(unit.complexity, 2)

    def test_authority_site_is_module_when_symbol_is_the_module(self) -> None:
        site = self._sites("countries")[0]
        self.assertEqual(site.unit_qname, "app.countries")

    def test_floor_authority_site_is_also_the_function(self) -> None:
        site = self._sites("report-formats", headline=False)[0]
        self.assertEqual(site.unit_qname, "app.reports.build_report_format_registry")


if __name__ == "__main__":
    unittest.main()
