1. Find all atomic fundamental principles impacting the maintainability of a code base, either making it less risky and cheaper, or making it riskier and more expensive. The principles must be generally applicable regardless of language, domain, size, project age, etc. They must together cover everything impacting this, but without overlapping each other, and being small enough that they can't be broken down further.

   Locked. Map: [principles/README.md](principles/README.md).

   - Edit: [01 degree](principles/01-co-change-degree.md), [02 locality](principles/02-co-change-locality.md), [03 strength](principles/03-co-change-strength.md)
   - Load: [04 size](principles/04-intra-site-size.md), [05 complexity](principles/05-intra-site-complexity.md), [06 mixing](principles/06-concern-mixing.md), [07 comprehension coupling](principles/07-comprehension-coupling.md)
   - Orient: [08 findability](principles/08-findability.md)
   - Check: [09 checkability](principles/09-checkability.md)
   - Mass: [10 accidental volume](principles/10-accidental-volume.md)
2. Turn the findings into a package of tiered instructions for coding agents and humans.

   Seed a non-software human can drive: they talk ([workflow/human.md](workflow/human.md)); the agent infers unnamed axes, writes `product/`, and implements. Entry: [README.md](README.md). Bootstrap: [workflow/bootstrap.md](workflow/bootstrap.md). Planning must finish at [workflow/handoff.md](workflow/handoff.md). Worked example: this repo’s chat app (`protocols` was inferred).
3. Define a metric that quantifies these findings and can be applied on any python code base. Lower score means cheaper to maintain.

   Defined: [metric.md](metric.md). Combined \(W \in [0,5]\) from the ten atoms. Lower is cheaper. **Claimable without a software reviewer:** floor is not proof of \(k=1\); the agent hunts and deletes extras; \(W\) is the backstop ([metric.md](metric.md) “What \(W\) can claim”).
4. Implement that metric.

   CLI: `PYTHONPATH=.nose python3 -m maintainability` (`.nose/maintainability/`). Stdlib only. Setup is the product’s `product/`.
