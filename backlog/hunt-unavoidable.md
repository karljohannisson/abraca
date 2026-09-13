# Make the extra-encoding hunt unavoidable

Status: **parked**. High Goal 0 impact, low effort.

**Why.** Floor extras are computed and then shown only as `k=`. Agents skip the synonym hunt and claim \(k=1\).

**Do.** Print scan extra paths from the CLI. Fail (exit 1) if headline \(k=1\) while the floor found copies, unless those paths were deleted or confirmed in yaml. That is the cheapest way to stop “scanner found nothing, ship it.”

**Not.** A full synonym hunter. That stays agent work.

**Check.** Fixture `dup` already has scan extras. CLI on that tree must list `recopy.py` (or equivalent) and refuse a headline that hides it.

Related: [script-driven-workflow-loop.md](script-driven-workflow-loop.md) wants this inside a broader `workflow check`. This item can land as a `maintainability` CLI flag without that package.
