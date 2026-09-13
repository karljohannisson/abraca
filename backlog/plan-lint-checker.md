# Plan lint as a small checker

Status: **partial**. `.nose/planlint/` landed 2026-09-13. Open: [bugs/planlint-axes-must-be-a-list.md](../bugs/planlint-axes-must-be-a-list.md), [bugs/planlint-ignores-template-encodes.md](../bugs/planlint-ignores-template-encodes.md).

**Why.** Architecture is one encode task per locked axis. That rule is seven markdown checkboxes. Agents skip them.

**Do.** A ~50-line check: every locked axis id has exactly one `encodes` task in `product/phase-4-plan.md`. Exit nonzero on fail. Optional extras: no dual-encode, authority tasks before uses.

**Not.** A second linter if [script-driven-workflow-loop.md](script-driven-workflow-loop.md) already ships `python3 -m workflow check`. Prefer one command. This item is the minimum if the full workflow package is not started.

**Check.** A plan missing an encode task fails. A plan with one encode per locked axis exits 0.
