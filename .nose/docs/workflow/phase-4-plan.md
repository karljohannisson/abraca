# Phase 4 — Implementation plan (no code)

**Cold agent loads:** this file, `product/status.yaml`, `product/phase-1.md`, `product/phase-2.md`, `product/axes.yaml`. Human is **out**. If the lint fails because an axis is missing, go back to Phase 3 (update status); do not invent axes in the plan.

You produce a MECE task list such that when every task is done, v1 meets every non-parked Phase 2 requirement **and** the codebase is measured against the axes. Tasks are ordered so every dependency is above: sequential top to bottom.

This is **not** a class-design essay. The architecture **is** one authority per locked axis. Layers/services that encode an axis outside that authority fail the lint.

## Build the plan

1. One **authority task** per `status: locked` axis: create the module whose name and first docstring line use tokens from `statement`; first member/variant only if Phase 2 says so; `verifies` that **read** the authority (no recopied lists). Set `encodes: [that-id]` and proposed `authority.symbol` / `path`. Fill those fields in `axes.yaml` in that task, not before.
2. **Use tasks** for composition (port, app, UI). `encodes: []`. They may `uses: [axis-ids]` (read/iterate only).
3. No task for `dormant` or Frozen. No task encodes two axes. No task recopies members.
4. Cover every non-parked `FR`/`TR`/`DR`/`XR`. If a requirement is not reachable from the task list, add a task or park the requirement (that is a Phase 2 defect — rewind if you cannot map it without a human).
5. Order: layout / `entry-points.yaml` (exclude `.nose`) → **all authority tasks** → composition → UI → glue. Never UI before the authorities it would have to recopy.
6. **Slice checkpoint is part of the plan**: after the first few authority tasks and before the first composition task, the plan must place a thin runnable vertical — the smallest set of tasks that yields one screen the human can run with one command. The orchestrator stops there for human try/accept before continuing (see [phase-4-task.md](phase-4-task.md), "Orchestrator after this task").
7. Each task stands alone in a new context: acceptance criteria, W gate, **only** the artifact paths it needs, requirement ids, axis ids.

Template: [templates/plan.md](templates/plan.md). Decision log starts empty: [templates/decisions.md](templates/decisions.md).

## Plan lint (must all pass before any task runs)

From the repo root, run `PYTHONPATH=.nose python3 -m planlint` against `product/phase-4-plan.md` and `product/axes.yaml`. Exit 0 is the gate. See [plan-lint.md](plan-lint.md). The boxes below are the rest of the checklist. They are not a substitute for the command.

- [ ] Every non-parked Phase 2 id is cited by at least one task.
- [ ] Every locked axis has **exactly one** task with `encodes: [that id]`.
- [ ] No task `encodes` two ids; no task `encodes` a dormant/frozen reason.
- [ ] Authority tasks appear before any task that `uses` that axis.
- [ ] Each task has: id, depends-on, requirement ids, encodes/uses, acceptance, `artifacts_to_load`, verify steps, commit message pattern `Tnnn: …`.
- [ ] Acceptance includes: tests; hunt extras of every locked axis touched and delete them; `PYTHONPATH=.nose python3 -m maintainability` (exit 0); headline \(W\) ≤ `w_baseline` (or first run sets baseline) unless `decisions.md` records why and that it is required by a Phase 2 id.
- [ ] Tasks do not include the whole of `phase-2.md` in `artifacts_to_load` — only cited ids (copy those sections into the task card so the task agent need not read the rest).
- [ ] A slice checkpoint exists: the first few authority tasks, then a thin runnable vertical (one screen, one command), then the rest.

If lint fails, fix the plan. Do not start tasks.

## Done (plan only)

- `product/phase-4-plan.md` exists and lint passes.
- `product/decisions.md` exists (may be empty).

Then do **not** jump to Phase 5. Copy the first task (including `copied_requirements`) into `product/current-task.md`. Set `next_instructions: .nose/docs/workflow/phase-4-task.md`, `artifacts` to status, current-task, axes, decisions, entry-points if any. Reset into that task. Do not list `phase-4-plan.md` on the task agent — it would leak later tasks.
