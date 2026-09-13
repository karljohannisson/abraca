# Nose Review

**Scope:** Read-only assessment of Nose against its own stated goals in `.nose/docs/goals.md`. This review evaluates the reusable Nose seed, not a product created with it.

## Overall Assessment

Nose is a thoughtful research/prototyping framework with a coherent maintainability model, a real stdlib Python CLI, and unusually clear workflow artifacts. It is not yet reliable enough to present its score or workflow gates as production-grade, autonomous evidence of maintainability.

The strongest parts are the ten-atom conceptual model, explicit phase artifacts, and the distinction between a scanner-derived floor and a confirmed headline score. The largest risks are semantic gaps in three implemented metric atoms, unvalidated input, workflow controls that rely on agent compliance, and a lack of empirical calibration.

## Findings

### 1. Critical: Checkability can report a falsely low score

The registry supports `signature_rename`, and the documented checkability rule requires fail-loud evidence for it, such as type or attribute errors. The implementation only applies fail-loud logic to `new_variant` axes.

Further, `_match_subject_is_auth()` returns `True` even when a `match` statement does not operate on the authority. An unrelated exhaustive `match` can therefore be counted as evidence that a variant axis is exhaustively handled.

**Evidence**

- `.nose/docs/workflow/artifacts.md`: declares `signature_rename`.
- `.nose/docs/principles/09-checkability.md`: defines fail-loud behavior for variants and signature/field changes.
- `.nose/maintainability/atoms.py`: `checkability()` only sets `fail_applies` for `new_variant`.
- `.nose/maintainability/atoms.py`: `_match_subject_is_auth()` ends with an unconditional `return True`.
- `.nose/tests/test_score_fixture.py`: only exercises a `set_grows` axis.

**Impact**

The metric can understate miss-risk and produce an artificially low headline `W`, even though the Phase 4 and Phase 5 workflow treats that score as a gate for agent-only implementation work.

**Recommendation**

Implement and separately test the documented fail-loud behavior for all supported shapes. Fix authority matching so unrelated `match` statements cannot count. Add fixtures for `new_variant`, `signature_rename`, positive and negative exhaustive-match cases, and intermediate `V` values.

### 2. Critical: Accidental-volume implementation is weaker than its specification

The documentation says accidental volume is the fraction of unreachable statements, discovered from declared and default entry points by following imports, names, and attributes. The implementation requires explicit entry-point paths, follows imports at module level, and marks an entire imported module reachable.

As a result, dead functions within a live module do not add to volume, despite being unreachable statements under the documented model. The promised default discovery of `__main__.py`, project scripts, `main.py`, and `app.py` is also absent.

**Evidence**

- `.nose/docs/principles/10-accidental-volume.md`: specifies statement-level reachability and default root discovery.
- `.nose/maintainability/atoms.py`: `volume()` constructs roots only from registry paths, live authorities, and verifies files, then tracks `reachable_paths` at file granularity.
- `.nose/maintainability/registry.py`: loads `entry_points` without supplying documented defaults.

**Impact**

A project can receive a lower mass score than the published definition warrants. This makes the result especially unreliable for repositories that collect obsolete code inside otherwise live modules.

**Recommendation**

Either implement symbol/statement-level static reachability plus documented root discovery, or narrow the documentation and output language to describe the current module-level import-closure approximation.

### 3. High: Fan-out can count third-party dependencies despite the definition excluding them

The coupling definition excludes stdlib and third-party code. In `_fanout()`, non-stdlib imports are recorded, and attribute uses of those imports are counted without proving they refer to same-repository code. For example, `import requests; requests.get(...)` can increase `H`.

**Evidence**

- `.nose/docs/principles/07-comprehension-coupling.md`: explicitly excludes third-party APIs.
- `.nose/maintainability/atoms.py`: `_fanout()` adds every non-stdlib `ast.Import` and counts matching attribute usage.

**Impact**

Projects can be penalized for dependency use that the principle says is outside the maintainability property being measured. This undermines comparability across codebases with different library choices.

**Recommendation**

Resolve imports against the indexed project-module set before counting them, and add regressions for stdlib, third-party, and local-package imports.

### 4. High: Invalid likelihood input can violate the advertised bound for `W`

The documentation permits numeric `p` only in `[0,1]`. The registry loader accepts arbitrary numeric values without validation. Negative, infinite, or greater-than-one weights can invalidate the weighted means and the claim that `W` lies in `[0,5]`.

**Evidence**

- `.nose/docs/metric.md`: states that numeric `P` must be in `[0,1]`.
- `.nose/docs/workflow/artifacts.md`: repeats the input contract.
- `.nose/maintainability/registry.py`: casts any integer or float to `float` with no bounds or finite-value validation.

**Impact**

Malformed but parseable registry input can make the headline score mathematically meaningless while still appearing to be a valid metric result.

**Recommendation**

Reject non-finite values and values outside `[0,1]` with a clear registry error. Add boundary and invalid-input tests.

### 5. High: Major workflow gates are procedural rather than enforced

Nose describes plan linting, isolated task context, extra-encoding hunts, and non-increasing `W` as gates. In the seed, they are instructions and Markdown checklists, not executable controls. A rising `W` may be accepted by adding a decision that names a requirement, without independent validation of the claimed necessity.

**Evidence**

- `.nose/docs/workflow/phase-4-plan.md`: plan lint is a checklist.
- `.nose/docs/workflow/phase-4-task.md`: requires a synonym hunt and permits a documented exception for a rising `W`.
- `.nose/docs/workflow/orchestrate.md`: context isolation is prompt/process guidance rather than sandboxed enforcement.

**Impact**

The workflow can be effective with a disciplined agent, but it cannot claim mechanical assurance. The result is vulnerable to missed requirements, incomplete hunts, context leakage, and rationalized metric regressions.

**Recommendation**

Create executable linting for the task plan and registry coverage, validate `W` exceptions against actual requirement IDs, record hunt strategies and outcomes, and make context isolation an explicit operational assumption unless it is technically enforced.

### 6. Medium: The metric is not calibrated or reproducibly validated

The project has a real CLI and a small fixture, but no declared test dependency or CI workflow. The fixture covers one live `set_grows` axis and does not establish that lower `W` corresponds to lower real maintenance cost across different projects.

**Evidence**

- `.nose/pyproject.toml`: contains no testing configuration or dependencies.
- `.nose/tests`: contains five test functions across three test modules.
- `.nose/tests/fixtures/dup/product/axes.yaml`: includes one locked `set_grows` axis.
- `.nose/docs/metric.md`: defines caps and equal group weights but provides no calibration evidence.

**Impact**

`W` is currently best viewed as a diagnostic heuristic. Its thresholds, directionality, and group weights have not been shown to predict maintenance effort or defect risk reliably.

**Recommendation**

Add an explicit test command and CI, expand regression fixtures around every atom and shape, then evaluate the metric against several real codebases with independent maintenance indicators before making stronger claims.

## Strengths

- The ten principles are organized around a recognizable maintenance task: orient, load, edit, check, and mass. This makes the framework easier to reason about than an undifferentiated quality score.
- The phase workflow makes intent, requirements, axes, task planning, decisions, and handover explicit artifacts rather than relying solely on chat context.
- The metric’s floor-versus-headline distinction correctly acknowledges that static scanning cannot prove the absence of semantic duplication.
- The maintainability CLI is implemented with the Python standard library and has a clear registry-oriented interface.
- Core metric modules have no editor-reported static diagnostics.

## Goal Assessment

| Stated goal | Assessment |
| --- | --- |
| Help humans and AI reach high-quality maintainable software | Promising but unproven; success relies heavily on procedural compliance. |
| Define ten atomic, general, non-overlapping principles | Substantially achieved as a coherent model; universal completeness and non-overlap remain hypotheses requiring external validation. |
| Define a Python metric where lower means cheaper to maintain | Not yet reliable enough for that claim because of defects and uncalibrated assumptions. |
| Implement the metric | Partially achieved: the CLI and scanner exist, but important documented semantics are missing or incorrect. |

## Priority Order

1. Correct and regression-test checkability, coupling, and accidental-volume behavior.
2. Validate all registry input needed to preserve score invariants, especially `p`.
3. Add a reproducible test command and CI with coverage for every atom and supported shape.
4. Automate the workflow gates that currently depend on agent self-attestation.
5. Calibrate `W` using real projects and independent maintenance evidence.

## Review Limits

This was a static, read-only review. No repository source or workflow files were changed. Test execution was not available in the reviewing environment, so the assessment is based on source, documentation, fixtures, and editor diagnostics rather than runtime results.
