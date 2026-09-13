# Phase 4 plan

Lint: [phase-4-plan.md](../phase-4-plan.md). Do not run tasks until every box there is ticked.

## T001 — …

- depends: []
- requirements: [FR-1]
- encodes: [example]
- uses: []
- authority: { symbol: pkg.example, path: src/pkg/example.py }
- artifacts_to_load:
    - product/status.yaml
    - product/axes.yaml
    - product/decisions.md
- copied_requirements: |
    FR-1: …
- acceptance:
    - …
    - verifies iterate the authority
    - CLI extras none
    - W gate
- verify: `.nose/docs/workflow/phase-4-task.md`
- commit: `T001: …`

## T002 — …

- depends: [T001]
- encodes: []
- uses: [example]
- …
