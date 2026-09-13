"""Tests for planlint (fixtures under tests/fixtures)."""

import tempfile
import unittest
from pathlib import Path

from planlint import lint, main

HERE = Path(__file__).parent
AXES = HERE / "fixtures" / "axes.yaml"
NOSE = HERE.parents[1]

from maintainability.yaml_lite import load as yaml_load


class PlanLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.axes = yaml_load(AXES.read_text(encoding="utf-8"))

    def test_passing_plan_exits_zero(self):
        plan = (HERE / "fixtures" / "plan_pass.md").read_text(encoding="utf-8")
        self.assertEqual(lint(plan, self.axes), [])

    def test_failing_plan_reports_problems(self):
        plan = (HERE / "fixtures" / "plan_fail.md").read_text(encoding="utf-8")
        errors = lint(plan, self.axes)
        self.assertTrue(any("locked axis 'other'" in e for e in errors), errors)
        self.assertTrue(any("T001: encodes 2 axes" in e for e in errors), errors)
        self.assertTrue(any("T001: encodes dormant axis 'dormant-thing'" in e for e in errors), errors)

    def test_missing_encode_for_locked_axis(self):
        plan = "## T001 — a\n\n```yaml task\nencodes: [example]\n```\n"
        errors = lint(plan, self.axes)
        self.assertEqual(
            sorted(errors),
            ["locked axis 'other' has 0 encodes tasks; exactly one required"],
        )

    def test_exactly_two_encodes_for_one_axis_fails(self):
        plan = (
            "## T001 — a\n\n```yaml task\nencodes: [example]\n```\n\n"
            "## T002 — b\n\n```yaml task\nencodes: [example]\n```\n"
        )
        errors = lint(plan, self.axes)
        self.assertIn("locked axis 'example' has 2 encodes tasks; exactly one required", errors)

    def test_unknown_axis_id_fails(self):
        plan = "## T001 — a\n\n```yaml task\nencodes: [nope]\n```\n"
        errors = lint(plan, self.axes)
        self.assertIn("T001: encodes unknown axis id 'nope'", errors)

    def test_block_list_encodes_form_also_parses(self):
        plan = (
            "## T001 — a\n\n```yaml task\nencodes:\n  - example\n```\n\n"
            "## T002 — b\n\n```yaml task\nencodes: [other]\n```\n"
        )
        self.assertEqual(lint(plan, self.axes), [])

    def test_no_tasks_at_all_fails_for_locked_axes(self):
        errors = lint("# empty plan\n", self.axes)
        self.assertEqual(len(errors), 2)

    def test_bullet_encodes_from_template_shape(self):
        plan = (
            "## T001 — a\n\n- encodes: [example]\n- uses: []\n\n"
            "## T002 — b\n\n- encodes: [other]\n"
        )
        self.assertEqual(lint(plan, self.axes), [])

    def test_main_accepts_registry_axes_map(self):
        axes_text = (
            "version: 1\n"
            "axes:\n"
            "  - id: example\n    status: locked\n"
            "  - id: other\n    status: locked\n"
            "  - id: dormant-thing\n    status: dormant\n"
        )
        with tempfile.TemporaryDirectory() as d:
            axes_path = Path(d) / "axes.yaml"
            axes_path.write_text(axes_text, encoding="utf-8")
            plan = HERE / "fixtures" / "plan_pass.md"
            self.assertEqual(main([str(plan), "--axes", str(axes_path)]), 0)

    def test_main_lints_the_recorded_example(self):
        plan = NOSE / "example" / "product" / "phase-4-plan.md"
        axes = NOSE / "example" / "product" / "axes.yaml"
        self.assertEqual(main([str(plan), "--axes", str(axes)]), 0)


if __name__ == "__main__":
    unittest.main()
