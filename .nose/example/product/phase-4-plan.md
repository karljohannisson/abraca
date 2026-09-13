# Phase 4 plan

Lint: [phase-4-plan.md](../docs/workflow/phase-4-plan.md). All boxes ticked below.

## T001 — regions authority

- depends: []
- requirements: [FR-1]
- encodes: [regions]
- uses: []
- authority: { symbol: world.regions, path: src/world/regions.py }
- artifacts_to_load:
    - product/status.yaml
    - product/axes.yaml
    - product/decisions.md
- copied_requirements: |
    FR-1: Running the program prints the countries of a region, one per line.
    TR-1: Data is hardcoded in the program.
- acceptance:
    - `src/world/regions.py` exists; name and first docstring line use tokens from
      "The set of world regions may grow."
    - first member only: `REGIONS = {"Europe": [...]}` (Phase 2 shows Europe only)
    - `verifies` test reads the authority (no recopied list)
    - hunt extras of `regions`; none found
    - `PYTHONPATH=.nose python3 -m maintainability --root .nose/example` (exit 0);
      first run sets baseline `w_baseline: 0.75`
- verify: `.nose/docs/workflow/phase-4-task.md`
- commit: `T001: regions authority`

## T002 — command-line program

- depends: [T001]
- requirements: [FR-1, FR-2, DR-1]
- encodes: []
- uses: [regions]
- artifacts_to_load:
    - product/status.yaml
    - product/axes.yaml
    - product/decisions.md
    - product/entry-points.yaml
- copied_requirements: |
    FR-1: print countries of a region, one per line.
    FR-2: unknown region → error message, exit 1.
    DR-1: plain command line, region name as the only argument.
- acceptance:
    - `src/world/__main__.py` reads only via `world.regions`
    - `product/entry-points.yaml` lists the program start
    - tests cover known and unknown region
    - hunt extras; none found; W gate exit 0, W ≤ baseline
- verify: `.nose/docs/workflow/phase-4-task.md`
- commit: `T002: world command`

## Plan lint

- [x] FR-1, FR-2, TR-1, DR-1 each cited by a task (TR-1 by T001).
- [x] `regions` locked → exactly one encodes task (T001); `greetings` dormant → none.
- [x] No task encodes two ids.
- [x] T001 before T002 which `uses` regions.
- [x] Every task has id, depends, requirements, encodes/uses, acceptance, artifacts, verify, commit pattern.
- [x] Acceptance includes tests, hunt, W gate.
- [x] Only cited requirement ids copied into task cards.
