# Phase 4 — One task

**Cold agent loads:** this file, `product/status.yaml`, `product/current-task.md`, `product/decisions.md`, `product/axes.yaml`, `product/entry-points.yaml` if it exists. Do not read `phase-4-plan.md` or other tasks. Do not read all of Phase 2 — the card copied the ids you need. Human is out.

You implement **this task only**. Then you stop.

Principles: [../principles/README.md](../principles/README.md). Combined \(W\): [../metric.md](../metric.md).

## Code rules

- `encodes: [r]` — that knowledge lives only in this task’s authority path. Docstring first line = `statement` tokens (findability).
- `uses` — iterate / lookup / import members. Do **not** recopy. Do not `if provider == …` outside the providers adapter.
- Different locked axes do not share an enclosing function.
- Dormant / Frozen: no code.
- `verifies` read the authority; never recopy member lists. Append the test path on the axis row in the same change.
- New public functions are entry points only if listed, or reached from listed ones / live authorities.
- If you rename an authority, update `axes.yaml`.

## Ambiguity

Minor judgment calls are allowed. If you decide: append `product/decisions.md` (id, task, decision, why, which requirement/axis ids it may affect). Later tasks read that file. If the call changes a Phase 2 requirement or splits an axis, **stop** — do not silently widen scope; leave the task failed so the orchestrator can rewind to Phase 2 or 3.

## Verify (required)

1. Acceptance criteria on the card.
2. Hunt extra encodings of every locked axis you touched (same tokens, then synonyms). **Delete** them. Do not ask a human to classify sites.
3. From the product root:

   ```
   PYTHONPATH=.nose python3 -m maintainability
   ```

4. Headline \(W\) must not exceed `status.w_baseline`. If `w_baseline` is null, set it to this headline in `status.yaml`. If the CLI exits 1, \(W\) rose: fix, or append a decision that names the Phase 2 id that forced it and rerun with `--max-w` equal to the new headline. Do not claim \(k=1\) from the floor.
5. Commit: message `Tnnn: <what>` referencing the task id. One task, one commit.

## Report to the orchestrator (end of context)

- Task id, commit, headline \(W\), floor \(W\), whether hunt found extras (must be none left).
- Decisions appended, if any.
- Failed: why, and whether Phase 2/3 must reopen.

Do not start the next task.

## Orchestrator after this task

If failed or extras remain or unexplained \(W\) rise: fix or replan; do not advance. If ok: overwrite `product/current-task.md` with the next undone task, keep `next_instructions` on this file, reset. When no tasks remain: Phase 5 (`phase-5-handover.md`; artifacts include plan, decisions, entry-points, phase-1, phase-2, axes — not current-task).
