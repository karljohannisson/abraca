# Maintainability workflow

Goal 2: tiered instructions so a human can maintain **requirements** and **change axes**, and a coding agent can implement as cheaply as the locked [principles](../principles/README.md) allow.

Do not copy principle metric formulas here. Those stay in `docs/principles/`. Combined \(W\): [../metric.md](../metric.md). This package says **who does what, in which file, in which order**.

## Two kinds of files

The **seed** is [`.nose/`](../../README.md) plus the root `AGENTS.md`. Everything else at the product root is the software being built.

| Kind | Where | Role |
|---|---|---|
| **Seed** | `.nose/` (`docs/`, `maintainability/`, metric `tests/`) and root `AGENTS.md` | How to work. Copy into every repo that uses this workflow. |
| **Product intent** | `product/` at the **product root** | What *this* software is, and which reasons it is designed to absorb. |
| **Product code** | `src/`, `tests/` at the product root | Authorities named in the axes file; `verifies` tests. |

This mothership also has [docs/goals.md](../goals.md) (how the seed itself was built). A generated product repo copies `.nose/` + `AGENTS.md`, then has its own `product/` + `src/`.

Schema of `product/*`: [artifacts.md](artifacts.md).

## Tiers

| Tier | Who | When | File |
|---|---|---|---|
| 0 | Human | Always | [human.md](human.md) |
| 1 | Agent | Every turn | [agent.md](agent.md) |
| 2 | Agent + human | Brief changed, new slice, new/split/freeze \(r\) | [planning.md](planning.md) |
| 3 | Agent | Writing or editing code | [implementing.md](implementing.md) |
| 4 | Agent + human confirm | Before claiming the slice is done | [review.md](review.md) |

Start at tier 2 until `product/` matches the latest human brief. Then 3, then 4. Tier 1 never turns off.

## Collaboration rule

Agreement that lives only in chat is not locked. A planning turn is unfinished until `product/requirements.md`, `product/axes.yaml`, `product/entry-points.yaml`, and `product/probes.md` match what was agreed.
