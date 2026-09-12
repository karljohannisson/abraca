# Tier 4 — Review

Before claiming a slice done. Headline scores use **confirmed** sites ([principle 1](../principles/01-co-change-degree.md)). Run `python -m maintainability` and read [metric.md](../metric.md).

## Agent

1. Run the metric. Record headline \(W\), floor \(W\), and the ten raw atoms.
2. For each locked \(r\) touched this slice: hunt extra encodings (same tokens, then synonyms). List hits under `extra_sites` as `proposed`. Promote to `confirmed` after the human agrees, or delete the extra in code.
3. Check mixing, `verifies` (read, not recopy), fail-loud, findability, reachability, no dormant/frozen code — the metric covers the automatic parts; the hunt covers Meaning+.

If a hunt finds extras, fix them or stop and ask. Do not report \(k=1\) because the floor said so.

## Human

Confirm or reject `extra_sites` that are not obvious token clones. Confirm new axes the agent added as `proposed`. Confirm entry points still match the public surface.

## Not done if

- `product/` disagrees with the brief or with the code’s authorities.
- Dormant/frozen behavior was implemented.
- Tests recopy a set the authority already holds.
