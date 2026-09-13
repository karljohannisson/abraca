0. This repo should be a help for a human to go from ideas to finished software together with an AI. The AI should lead the different phases and help achieve high quality maintainable software that meets the need of the human.
1. Find all atomic fundamental principles impacting the maintainability of a code base, either making it less risky and cheaper, or making it riskier and more expensive. The principles must be generally applicable regardless of language, domain, size, project age, etc. They must together cover everything impacting this, but without overlapping each other, and being small enough that they can't be broken down further.

   Locked. Map: [principles/README.md](principles/README.md).

   - Edit: [01 degree](principles/01-co-change-degree.md), [02 locality](principles/02-co-change-locality.md), [03 strength](principles/03-co-change-strength.md)
   - Load: [04 size](principles/04-intra-site-size.md), [05 complexity](principles/05-intra-site-complexity.md), [06 mixing](principles/06-concern-mixing.md), [07 comprehension coupling](principles/07-comprehension-coupling.md)
   - Orient: [08 findability](principles/08-findability.md)
   - Check: [09 checkability](principles/09-checkability.md)
   - Mass: [10 accidental volume](principles/10-accidental-volume.md)
2. Turn the findings into a package of tiered instructions for coding agents and humans.

   Five phases the **agent drives**; the human only talks. Clone, open `AGENTS.md`, talk until handover. Coordination: [workflow/orchestrate.md](workflow/orchestrate.md). Phases: [workflow/README.md](workflow/README.md). Context resets between phases and between Phase 4 tasks; only listed artifacts travel. Phase 4 plan is linted against axes **before code**; each task is gated on \(W\).
3. Define a metric that quantifies these findings and can be applied on any python code base. Lower score means cheaper to maintain.

   Defined: [metric.md](metric.md). Combined \(W \in [0,5]\) from the ten atoms. Lower is cheaper. Phase 4 tasks cannot claim done without the \(W\) gate. Floor is not proof of \(k=1\); the agent hunts and deletes extras.
4. Implement that metric.

   CLI: `PYTHONPATH=.nose python3 -m maintainability` (`.nose/maintainability/`). Stdlib only. Setup is `product/axes.yaml` + `product/entry-points.yaml`.
