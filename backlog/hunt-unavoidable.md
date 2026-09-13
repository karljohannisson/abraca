# Make the extra-encoding hunt unavoidable

Status: **done** (landed 2026-09-13 as one commit on `main`; see `git log --oneline -- .nose/maintainability/__main__.py`).

**Why.** Floor extras are computed and then shown only as `k=`. Agents skip the synonym hunt and claim \(k=1\).

**Do (as specified).** Print scan extra paths from the CLI. Fail (exit 1) if headline \(k=1\) while the floor found copies, unless those paths were deleted or confirmed in yaml. That is the cheapest way to stop “scanner found nothing, ship it.”

**Do (as landed).** A literal “headline k==1 while floor found copies” gate is dead code here: floor scan extras flow *into* the headline (they are not hidden), so the condition is always false. The claim of k=1 actually lives in `axes.yaml` (no confirmed extras), so the gate keys on that instead: the CLI lists scan-extra paths and exits 1 when any exist that are neither deleted nor confirmed as `extra_sites`. Same escape hatches (delete or confirm), fail-closed by default.

**Still open (deliberately).** The synonym hunt — paraphrases the token scanner cannot match — remains agent instruction. Candidate cheap hardening: require a `product/hunt.md` log and have `workflow check` (if it ships) refuse its absence; visibility, not proof. See [script-driven-workflow-loop.md](script-driven-workflow-loop.md), “What not to automate.”

**Not.** A full synonym hunter. That stays agent work.

**Check.** Fixture `dup` already has scan extras. CLI on that tree must list `recopy.py` (or equivalent) and refuse a headline that hides it.

Related: [script-driven-workflow-loop.md](script-driven-workflow-loop.md) wants this inside a broader `workflow check`. This item can land as a `maintainability` CLI flag without that package.
