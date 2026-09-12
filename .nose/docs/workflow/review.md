# Tier 4 — Review

Before claiming a slice done. Headline scores use **confirmed** sites ([principle 1](../principles/01-co-change-degree.md)). From the product root run `PYTHONPATH=.nose python3 -m maintainability` and read [metric.md](../metric.md).

The human is not a site classifier. You hunt; you delete.

## Agent

1. Run the metric. Record headline \(W\), floor \(W\), and the ten raw atoms.
2. For each locked \(r\) touched this slice: hunt extra encodings (same tokens, then synonyms). **Delete** extras (rewrite tests to iterate; collapse duplicate tables). Do not ask the human to label `strength`. Leave `extra_sites` empty unless a software collaborator is present and you are keeping a confirmed extra this slice.
3. Check mixing, `verifies` (read, not recopy), fail-loud, findability, reachability, no dormant/frozen code — the metric covers the automatic parts; the hunt covers Meaning+.
4. If something static-dead might still be a live plugin, ask in domain language: “do you still use X?” → `confirmed_live`. That is a product question, not a metrics question.
5. Recap for the human: what this version does now; \(W\) in one sentence if it moved.

If a hunt finds extras, fix them or stop. Do not report \(k=1\) because the floor said so.

## Human

Confirm the product still matches what they meant (behavior, slice, frozen). Confirm inferred bets they have not answered. That is all.

## Claimable (no software reviewer required)

- [handoff.md](handoff.md) still holds; `product/` matches the last accepted recap.
- Slice `verifies` pass.
- No dormant/frozen behavior in code.
- No leftover hunt hits; tests do not recopy authorities.
- Headline \(W\) did not rise, or you explained the rise in one domain sentence and the human still wants the slice.

## Not done if

- `product/` disagrees with the brief or with the code’s authorities.
- Dormant/frozen behavior was implemented.
- Tests recopy a set the authority already holds.
- You are waiting on the human to confirm extra sites.
