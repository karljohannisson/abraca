# `.nose/` — maintainability seed

This directory is the **workflow seed**, not the product. Copy it (plus the root `AGENTS.md`) into a repo; the rest of that repo is the software you are building.

A non-software human talks. The agent infers unnamed change axes, writes `product/`, and implements. Start: [docs/README.md](docs/README.md).

| Here | Product (repo root) |
|---|---|
| `docs/principles/` — ten atoms | `product/` — requirements and change axes (**agent-written**) |
| `docs/workflow/` — human talks; agent plans/implements | `src/<name>/` — authorities |
| `docs/metric.md` — combined \(W\) | `tests/` — product `verifies` |
| `maintainability/` — `python -m maintainability` | |
| `tests/` — tests for that metric | |

From the **product root** (this repo’s root):

```
PYTHONPATH=.nose python3 -m maintainability
```

`--root` defaults to the working directory, which must contain `product/`.
