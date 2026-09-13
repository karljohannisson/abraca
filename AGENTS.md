# Agents

You run this repo. The human only talks. You drive the workflow to a finished product.

`.nose/` is a **dot directory** — open it even if a listing hides it.

Read, in this order, and then **stop reading extra seed files** until the current phase doc says to:

1. [`.nose/docs/README.md`](.nose/docs/README.md)
2. [`.nose/docs/workflow/orchestrate.md`](.nose/docs/workflow/orchestrate.md)
3. `product/status.yaml` if it exists (if missing: Phase 1, `not_started`)
4. The instruction file in `status.next_instructions` (Phase 1 if status is missing)
5. **Only** the artifact files listed in `status.artifacts`

Do not ask the human which phase you are in. Do not ask permission to advance a phase whose done-criteria are met.
