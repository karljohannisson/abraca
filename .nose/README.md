# `.nose/` — maintainability seed

Clone the repo (or copy this directory plus root `AGENTS.md`). Point an agent at the repo and **talk**. The agent runs five phases until the product exists. You do not drive the workflow.

Start: [docs/README.md](docs/README.md). Orchestration: [docs/workflow/orchestrate.md](docs/workflow/orchestrate.md).

| Here | Product (repo root) |
|---|---|
| `docs/principles/` — ten atoms | `product/` — phase artifacts (**agent-written**) |
| `docs/workflow/` — phases 1–5 | `src/<name>/` — authorities (Phase 4) |
| `docs/metric.md` — combined \(W\) | `tests/` — product `verifies` |
| `maintainability/` — `python -m maintainability` | |
| `tests/` — tests for that metric | |

From the **product root**:

```
PYTHONPATH=.nose python3 -m maintainability
```
