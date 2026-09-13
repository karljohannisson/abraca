# Phase 2 — Detailed requirements

**Cold agent loads:** this file, `product/status.yaml`, `product/phase-1.md`. Match `human.technical_depth`.

Dig until there are **no surprises** when they open the finished product, and until peripheral gold-plating is a conscious choice. This phase makes the product honest. It does **not** make the codebase cheap — that is Phases 3–4.

MECE for **this version of this product**, not the lifetime of the company. Lifetime wishes go to parked.

## Do

1. From Phase 1 core + “for Phase 2,” probe user stories. Five whys/hows **internally** as far as they change UX or later maintainability. Ask the human only what you cannot infer.
2. Infer and recommend (stack, persistence, where it runs). Label inferences. Human decides.
3. Explode ambiguities. If it is visual, put a **wireframe** (ASCII or mermaid) in the artifact so they can see what they are agreeing to. If it is a backend flow, put a **diagram**. Explain cheaper vs dearer options with the picture (one place vs many), not with metric jargon.
4. If a requirement is not the core idea and adds a lot of implementation and maintenance cost, say that plainly, offer a simpler path, and ask which they want. Record the choice.
5. Write atomic, MECE requirements with stable ids. If a later agent blindly met every non-parked requirement, the product would be good **as a product**.
6. Recap in their language. Wait.

Do not write code. Do not lock change axes yet (note candidates in “hints for Phase 3” if they came up). Do not pick class names.

## Requirement types (use these id prefixes)

| Prefix | What |
|---|---|
| `FR-` | Functional — what it does for a user |
| `TR-` | Technical — stack they chose, constraints, expected load, runtime. Infer and recommend if they have no preference. |
| `DR-` | Design decisions — UX and structure they agreed, with wireframe/diagram |
| `XR-` | Other, if needed (legal, ops) |

Each requirement is one atomic sentence (or a short block with one id). No overlapping ids. Parked items list **why**.

## `product/phase-2.md` must contain

- Functional, technical, design (and other) requirements, MECE for v1
- Wireframes / diagrams for anything visual or flow-heavy
- Requirements that were **parked** and why (including complexity warnings they declined)
- **Hints for Phase 3** — things they said might change later (do not treat as locked axes)

Template: [templates/phase-2.md](templates/phase-2.md).

## Done

- Human accepted the recap.
- Every v1 behavior lives in exactly one requirement id; parked is explicit.
- Visual/flow decisions have a picture in the file.
- No code.

Then `phase: 3`, `phase_name: axes`, `next_instructions: .nose/docs/workflow/phase-3-axes.md`, `artifacts: [product/status.yaml, product/phase-1.md, product/phase-2.md]`, reset, continue.
