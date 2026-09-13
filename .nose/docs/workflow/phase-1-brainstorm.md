# Phase 1 — Brainstorm

**Cold agent loads:** this file, `product/status.yaml` (create if missing), [human.md](human.md), [orchestrate.md](orchestrate.md) already read. No other `product/` files unless listed in status.

Help the human turn dumps and half-thoughts into a **small invariant core**. You use software-engineering judgment. They do not need it.

## Do

1. Listen. Market research only if they are **not** building purely to learn: what exists, how this is different. If they are learning, skip research and say so.
2. Infer what they did not say (UI: terminal / web / HTTP API / in-process library; who runs it; what “done” means). State each inference as a bet and ask for confirmation. Explain the term the first time (`terminal` = a text window in their computer, not a website).
3. Five whys **to yourself** on every fuzzy goal. If an unanswered why would bite later, ask **one** question in their language. Do not dump a why-chain on them.
4. Shape **stable** core requirements — few, invariant for the rest of this workflow. Details belong in “for Phase 2,” not in the core.
5. Write `product/phase-1.md` as you go (template: [templates/phase-1.md](templates/phase-1.md)). Update `product/status.yaml`. Record `human.technical_depth` and `domains` from their words.
6. Recap the core, what this is not, and parked ideas in ordinary language. Wait for agreement.

Do not write code. Do not write `axes.yaml`. Do not explode every user story yet.

## `product/phase-1.md` must contain

- **Core invariant requirements** (`IR-1` …) — the product still is this if details change
- **What this is not** — refused product shapes, out of scope, never
- **For Phase 2** — richer requirements, user stories, ideas, confirmed inferences, open questions you already know Phase 2 must explode
- **Parked ideas** — split-out products or later projects, with why they are not this product
- **Internal five-whys that changed the core** — short, so Phase 2 does not re-ask

## Done (you advance; you do not ask to advance)

- Human agreed the recap of core + what this is not + parked.
- `phase-1.md` has all four sections; IDs stable.
- `status.yaml` has `human.technical_depth`.
- No product code.

Then set `phase: 2`, `phase_name: requirements`, `next_instructions: .nose/docs/workflow/phase-2-requirements.md`, `artifacts: [product/status.yaml, product/phase-1.md]`, reset, continue.
