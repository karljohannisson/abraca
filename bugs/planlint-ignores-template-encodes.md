# Planlint ignores template and example `encodes:` bullets

**Status:** open.

**Where.** `.nose/planlint/__init__.py` `_task_blocks`.

**What is wrong.** Task encodes are taken only from a fenced `yaml task` block. The plan template (`.nose/docs/workflow/templates/plan.md`) and the recorded example (`.nose/example/product/phase-4-plan.md`) put `encodes:` on markdown bullets. After unwrapping example axes, `lint()` reports `locked axis 'regions' has 0 encodes tasks` even though T001 encodes `regions`.

**Why it matters.** The checker cannot pass the only finished plan in the tree. Agents who copy the template always fail or skip the tool.

**Fix.** Parse `encodes:` from the existing task-card bullets. Keep the `yaml task` fence as an extra form so current fixtures still pass. One format agents already write, not a second convention.
