# Tier 1 — Agent, always on

Read [../README.md](../README.md) once. Read [artifacts.md](artifacts.md) once per repo. If `product/` is missing or stale vs the human’s last message: [bootstrap.md](bootstrap.md) / [planning.md](planning.md) **before code**.

## How you talk

- Domain language. Explain inferred bets as ordinary sentences with a because.
- Never ask the human to edit yaml, name modules, classify extra sites, or interpret \(W\).
- After any agreement, update `product/` in the same turn ([README](README.md) collaboration rule).

## Intent lives in `product/`

- Implement the **current slice** in `requirements.md`.
- Design only for **locked** rows in `axes.yaml`. Inferred locked rows are first-class; do not skip them because the human did not name them.
- Do not encode a reason that is frozen, dormant, proposed, or missing.
- `origin` / `because` / `plain` are for you and the recap. The scorer ignores them.

## One authority per locked \(r\)

- Put new knowledge in that row’s `authority.path` only.
- A *use* reads the authority (iterate, lookup, import members). A *representation* recopies it. Do not add representations.
- Do not switch on another axis’s members outside that axis’s adapter (`if provider == …` in the TUI is an extra site of `providers`).
- Do not create a module for a `dormant` row.

## Names

The authority’s qualified name and first docstring line must use tokens from the row’s `statement` (findability). Do not put the file path into the statement.

## Checks

- `set_grows`: `verifies` iterate/parametrize from the authority; do not recopy members in tests.
- `new_variant`: exhaustive match / typed visitor; no `_` / `else` default that swallows new arms.
- `formula_value` / `signature_rename`: tests read the authority.

When you add a test that verifies an axis, append it to that row’s `verifies` in the same change.

## Score

After a slice, from the product root run `PYTHONPATH=.nose python3 -m maintainability` (see [metric.md](../metric.md)). Report headline \(W\) and the ten raw atoms. Translate for the human: one sentence if \(W\) moved (“we copied a list into two places; I will fix that”). Do not claim \(k=1\) from the floor. If headline \(W\) rose, fix or ask a **product** question, not a metrics question.

## Mass

No code that is not reachable from `product/entry-points.yaml` plus live authorities. No speculative helpers “for later.”

## Scope

If the human asks for behavior that needs a new axis, **stop and plan** (tier 2). Do not smuggle the axis into code first.
