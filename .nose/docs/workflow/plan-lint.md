# Plan lint

A small checker for the phase-4 plan, against `product/axes.yaml`. Stdlib only.

Run:

```
cd <repo root> && PYTHONPATH=.nose python3 -m planlint
```

Exit 0 = pass, exit 1 = any failure, with one `FAIL …` line per problem.

## What it checks

- Every `status: locked` axis id has **exactly one** task with `encodes: [that id]`.
- No task `encodes` two ids.
- No task `encodes` a dormant axis or an unknown id (frozen reasons are never rows, so unknown = fail too).

Optional extras from [phase-4-plan.md](phase-4-plan.md) (authority-before-uses, requirement coverage, artifacts, W gate) are **not** enforced here — this is the minimum. If `python3 -m workflow check` from the full workflow package ships, prefer that and delete this.

## Plan convention

Task heading pattern: `## Tnnn`. `encodes` is the markdown bullet the phase-4 plan template already uses:

```markdown
## T001 — example authority

- encodes: [example]
- uses: []
```

A fenced `yaml task` block is also accepted (same `encodes` field). If both are present, the fence wins.

`product/axes.yaml` may be a `{version, axes: [...]}` map (the registry shape) or a bare list of rows.

Paths default to `product/phase-4-plan.md` and `product/axes.yaml`. Override with a positional plan path and `--axes PATH`.
