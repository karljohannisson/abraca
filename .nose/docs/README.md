# Maintainability seed — start here

You are a coding agent. This tree is **how to work**. The rest of the repo is **the product**.

Hand this seed (the parent `.nose/` directory, plus a root `AGENTS.md`) to an agent together with a human who knows the product. The human does **not** need software experience. They know what the software is for and what might change in their world. You infer the rest.

## Load order

1. This file.
2. If `product/` is missing, empty, or disagrees with the human’s last message: [workflow/bootstrap.md](workflow/bootstrap.md), then [workflow/planning.md](workflow/planning.md). **Do not write product code** until the human has accepted a recap in ordinary language and you have written `product/`.
3. Always: [workflow/agent.md](workflow/agent.md).
4. Human (so you know how to talk to them): [workflow/human.md](workflow/human.md).
5. After planning: [workflow/handoff.md](workflow/handoff.md) → [workflow/implementing.md](workflow/implementing.md) → [workflow/review.md](workflow/review.md).

Principles (do not copy formulas into the workflow): [principles/README.md](principles/README.md). Combined score \(W\): [metric.md](metric.md). Schema of `product/`: [workflow/artifacts.md](workflow/artifacts.md).

## Three layers

| Layer | Where | Who writes it |
|---|---|---|
| Seed | `.nose/` (this docs tree, the metric package, metric tests) and root `AGENTS.md` | Copied. Do not fork per product. |
| Intent | `product/` at the **product root** | **You.** The human talks; you write every file. |
| Code | `src/`, `tests/` at the product root | You, after the handoff. |

`.nose/` is a dot directory — open it even if a listing hides it.

## Non-negotiable

- The human **talks**. They do not edit yaml, name modules, or confirm extra sites.
- You **infer** independent change reasons the brief never named (a non-software person will not say “API protocols”). Propose them as bets, in domain language, with a because. Wait for yes / no / later. Do not build a framework because “this often changes.”
- Agreement that lives only in chat is not locked. Planning is unfinished until `product/` matches what the human accepted.
- Score after a slice: from the product root, `PYTHONPATH=.nose python3 -m maintainability`. Lower \(W\) is cheaper. The human does not interpret atoms; you hunt extras and **delete** them.
