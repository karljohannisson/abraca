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

## Plan convention: one fenced YAML block per task

The plan is loose markdown, so each task carries a small fenced block tagged `yaml task`:

```markdown
## T001 — example authority

```yaml task
encodes: [example]
uses: []
```
```

Rules:

- Task heading pattern: `## Tnnn — …` (`T` + digits).
- The block sits inside its task's section (before the next task heading or top-level `# ` heading).
- `encodes:` is a list of axis ids (inline `[a, b]` or block list both parse). Omit or `[]` for use tasks.
- Any other fenced block, and prose before the first task, is ignored.

Paths default to `product/phase-4-plan.md` and `product/axes.yaml`; override with positional plan path and `--axes PATH`.
