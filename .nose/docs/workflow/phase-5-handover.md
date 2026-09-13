# Phase 5 — Handover

**Cold agent loads:** this file, `product/status.yaml`, `product/phase-1.md`, `product/phase-2.md`, `product/axes.yaml`, `product/phase-4-plan.md`, `product/decisions.md`, `product/entry-points.yaml`. Run the metric. You may inspect `src/` and `tests/` against the plan.

Hand the **finished v1** to the human in their language. They do not read yaml.

## Do

1. Run `PYTHONPATH=.nose python3 -m maintainability`. Hunt extras; delete if any slipped through. Claimable: verifies pass, no dormant/frozen code, no leftover hunt hits, headline \(W\) understood vs baseline ([metric.md](../metric.md) “What \(W\) can claim”).
2. Write `product/phase-5.md`: how to start the program; what it does (Phase 2 ids, in their words); what was parked; inferred axes you designed for, in their words; \(W\) in **one sentence** if it is not ~0 (“there is still one awkward name to find the chat entry point”); decisions that affect them.
3. Ask them to try it. **Accept** or **complain**.

## If they accept

Set `phase: maintenance`, `phase_name: maintenance`, `next_instructions: .nose/docs/workflow/orchestrate.md`. In maintenance: small changes are Phase 4 tasks under the same \(W\) gate. If they change what the product is or what can change, you go to Phase 2 or 3 yourself — they still do not pick the phase.

## If they complain

Do not argue. Classify:

| Complaint | Rewind to |
|---|---|
| Wrong behavior, missing UX, “not what I meant” | Phase 2 (amend `phase-2.md`, then 3 if axes move, then 4 for new/changed tasks) |
| “We’ll also need another vendor / widget / kind of thing later” | Phase 3 (then 4) |
| It crashed / a bug in agreed behavior | Phase 4 task(s) to fix, still under \(W\) |

Update `status.yaml` to that phase, list the artifacts that phase needs, reset, continue. Keep what you already know on disk.
