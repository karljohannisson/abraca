# Script-driven workflow loop

Status: **parked**. Captured 2026-09-13 from an investigation, not an implementation plan for day 1.

Goal: make phases as automatic and script-driven as possible so the agent spends tokens on the product, not on the process. Verify with a script, then get a clean context. Seed status and templates. Force whatever can be forced.

This is the generalization of Wave 4’s parked “plan-lint executable” and of Wave 2’s fail-closed \(W\) gate.

## What the repo already bets on

Goal 0 (after the planned rewrite): a non-software human plus an **arbitrary** coding agent talk until a product exists. The agent drives five phases. Context is supposed to reset between phases and between Phase 4 tasks. Only listed artifacts travel.

That loop is entirely **prompt-normative** today:

| Process step | Who does it now |
|---|---|
| Create `product/` + `status.yaml` | Agent, from memory / template path in docs |
| Seed `phase-N.md` / `axes.yaml` / `decisions.md` | Agent copies templates if it remembers |
| Know `next_instructions` + `artifacts` lists | Agent rewrites yaml by hand from `orchestrate.md` tables |
| “Done?” | Agent self-attests against markdown checklists |
| Plan lint | Markdown boxes in `phase-4-plan.md` |
| Copy one task into `current-task.md` | Orchestrator agent |
| Run \(W\), compare to `w_baseline` | Agent (Wave 2 will make the CLI fail-closed) |
| Hunt extra encodings | Agent (unavoidable; scanner cannot prove \(k=1\)) |
| Context reset | “If you can spawn an isolated subagent, do that; else say one line and continue” |

Two reviews already named this as the Goal 0 failure mode: the product is instructions, not a harness. See [brainstorming/](../brainstorming/). The fail-closed \(W\) CLI (`--max-w`) has landed. Wave 4’s parked “plan-lint executable” is this item, or the thinner [plan-lint-checker.md](plan-lint-checker.md).

## Split that should stay sacred

Scripts own **process**. Agents own **intent**.

**Process (force through code):** `product/status.yaml`, `product/current-task.md` (derived from the plan), template seeding, artifact lists, `next_instructions` paths, plan-lint, \(W\) vs baseline, “this phase/task is allowed to end.”

**Intent (still the agent + human):** conversation, recaps, MECE requirements, inferred axes, independence/frequency/shape, writing the plan’s *content*, implementing a task, extra-site hunt, Phase 5 complaint classification, justified \(W\) exceptions.

If a script cannot decide it without reading the human’s mind, it is not a gate. It can still be a **shape check** (required headings, stable ids, yaml schema).

Context clearing is a third category: **neither markdown nor a Python script inside the same session can wipe the model’s context.** That requires a host that launches a fresh worker (Grok `agent()` / `spawn_subagent`, Claude Task, etc.). A portable seed can *require* “next work happens in a new worker whose prompt is only AGENTS.md + status + listed artifacts.” It cannot implement that for every editor.

## Where it fits in the tree

Do **not** put this in `.nose/maintainability/`. That package is the scorer. Process ≠ metric.

Recommended new seam, next to the scorer:

```
.nose/workflow/          # NEW package: executable process
  __init__.py
  __main__.py            # PYTHONPATH=.nose python3 -m workflow <cmd>
  seed.py
  check.py
  advance.py
  next_task.py
  status_io.py           # only writer of status.yaml

.nose/docs/workflow/     # stays the judgment playbook (phases 1–5, human.md)
.nose/docs/workflow/templates/   # already exist; scripts copy them
```

Public calls stay the same style as the metric:

```
PYTHONPATH=.nose python3 -m maintainability
PYTHONPATH=.nose python3 -m workflow seed|check|advance|next-task
```

`AGENTS.md` load order becomes: docs README → orchestrate → **run `workflow seed` if no status** → read status → current phase. The agent stops inventing yaml.

Optional, **not** in the portable seed: a Grok (or other host) adapter that is the actual context-clearing harness. That can live later as `.grok/workflows/nose.rhai` or a skill. It must not become the only way to run Nose, or Goal 0’s “arbitrary coding agent” dies.

## Collision

The seed-wave scorer work is on `main`. Archive: [brainstorming/archive/planned-changes.md](../brainstorming/archive/planned-changes.md).

Do not put this in `.nose/maintainability/`. Process ≠ metric. Prefer one plan lint: this package’s `check`, or [plan-lint-checker.md](plan-lint-checker.md), not both.

Sequencing:

1. `check` can already call the metric CLI (`--max-w` / `w_baseline`).
2. Add `.nose/workflow/`. Thin the phase docs to “done means the script exits 0.”
3. Park a host harness until the portable CLI is the real source of truth.

Wave 4’s parked “plan-lint executable” **is this**, not a separate tool.

## Medium effort (do this first)

Keep the agent as orchestrator. Replace “remember the process” with “run these commands.” Fail closed.

Commands:

1. **`seed`** — if `product/status.yaml` missing: create `product/`, copy templates (`status.yaml`, `phase-1.md`). Never let the agent freehand the yaml schema. Idempotent if files exist.
2. **`check`** — phase-aware, exit 0/1:
   - Presence + required headings / id prefixes for phase-1/2/5 markdown.
   - Phase 3: `axes.yaml` parses; `p` in \([0,1]\); no leftover `proposed`; locked rows have shape ≠ unknown; `authority` still null until a task fills it.
   - Phase 4 **plan**: every non-parked Phase 2 id cited; exactly one `encodes` task per locked axis; no dual-encode; depends-on is a DAG; authority tasks before uses; each task has the required fields.
   - Phase 4 **task**: `current-task.md` is exactly one task; metric CLI exit 0 (after Wave 2: \(W\) ≤ baseline unless a decision row names a Phase 2 id — validate the id exists, do not judge the prose).
   - Cannot check: recap quality, hunt quality, whether the human actually agreed. Those stay `status: waiting_human` until the agent sets a small explicit field (e.g. `human_accepted: true`) after the human says yes. The script should refuse `advance` without that bit for phases 1–3 and 5.
3. **`advance`** — the **only** writer of `status.yaml` phase/name/`next_instructions`/`artifacts`. Runs `check` first. Seeds the next template. Sets `in_progress`. Agent never copies the `orchestrate.md` table by hand.
4. **`next-task`** — parses the plan, finds the first undone task, **overwrites** `current-task.md` with that card only, points `next_instructions` at `phase-4-task.md`, sets the task artifact list (status, current-task, axes, decisions, entry-points if present). **Does not** put `phase-4-plan.md` on the task agent. “Undone” should be mechanical: matching `Tnnn:` commit missing, or a small `product/tasks.yaml` the scripts maintain. Do not make the agent tick boxes in the plan file.

Instruction change (the whole medium-effort payload):

- `AGENTS.md` / `orchestrate.md`: when you think the phase is done, run `check`; if green and the human accepted, run `advance` (or `next-task`). Do not edit `status.yaml` except via the script. After advance, start a **new** worker with the canned cold-agent prompt already in `orchestrate.md`. If the host cannot spawn, stop and say the phase is locked on disk — do not continue in the same context as the default.
- Phase docs: delete duplicated “then set phase: N, artifacts: […]” epilogues; point at `advance`.
- Templates stay; agents fill the blanks instead of creating files from scratch.

Prerequisite for plan lint: today’s `phase-4-plan.md` is loose markdown. A linter needs a **parseable task schema** (fenced YAML per task, or `product/phase-4-plan.yaml` plus a human-readable md stub). That is a real `artifacts.md` change — wait for the owned-file waves, or add the yaml **alongside** the md without rewriting the owned phase-4-plan doc until then.

What this buys: the agent spends tokens on the product, not on reconstructing artifact lists. Skipped lints become a failed command, not a missed bullet. What it does **not** buy: actual context isolation, or a hunt that cannot be skipped (the hunt remains an instruction; you can require a `product/hunt.md` log so skipping is visible, you cannot prove completeness).

## High effort (later): harness

The orchestrator stops being an LLM that also does Phase 1.

A host-level runner:

```
seed
loop:
  read status
  if waiting_human: pause for the human (this is the only conversation)
  launch isolated worker with: AGENTS.md + orchestrate + next_instructions + artifacts only
  wait
  check
  if fail: re-launch same phase/task (fresh or resume — prefer fresh after N fails)
  if phase 4 plan just passed: next-task
  elif phase 4 tasks remain: next-task
  else: advance
```

On Grok this is a workflow script (`agent()` per phase/task = real empty context, `await_user` for recaps). On hosts without subagents it cannot exist; the medium CLI is the fallback.

Do **not** start here. A harness that duplicates the yaml tables in prompts will rot the moment `advance`’s mapping is the real one. Build the Python process package first; the harness only shells out to it.

Also out of scope for this harness (already parked in Wave 4): CI, token/correctness benchmark, scoring Nose itself, JS backend. Those are eval, not the loop.

## What not to automate

- Human recap acceptance (record a bit; don’t infer it from file mtime).
- Extra-encoding hunt (log it; don’t pretend grep is \(k=1\)).
- Phase 5 complaint routing (table stays in `phase-5-handover.md`; script can apply a chosen rewind target once the agent/human picks the row).
- Writing `src/` or axes content.
- “Explain this term the first time” / five-whys — that is `human.md`, not code.

## Recommendation when this is picked up

Fit this as a **new `.nose/workflow` process package**, the sibling of `maintainability`, sequenced **after Wave 2**, absorbing the parked Wave 4 plan-lint.

Ship **medium** as the default: scripts as the only writer of process files + fail-closed `check`/`advance`/`next-task`, with phase docs reduced to judgment. Treat a Grok (or similar) harness as an optional adapter that calls those same commands so context reset is real when the host allows it.

Success metric for this layer is not a lower \(W\). It is: a cold agent can complete a phase without editing `status.yaml` by hand, and a skipped lint cannot look like “done.”
