# Tier 4 — Review

Before claiming a slice done. Headline scores use **confirmed** sites ([principle 1](../principles/01-co-change-degree.md)).

## Agent

1. For each locked \(r\) touched this slice: hunt extra encodings (same tokens, then synonyms). List hits under `extra_sites` as `proposed`.
2. Check mixing: one enclosing unit, one live \(r\) encoded.
3. Check `verifies` bind the authority (read, not recopy) and fail-loud where `shape` requires it. Yaml `verifies` lists match the tests.
4. Check names vs statements (findability).
5. Check reachability from `entry-points.yaml` + live authorities.
6. Confirm no code for dormant/frozen reasons.

If a hunt finds extras, fix them (move knowledge to the authority) or stop and ask; do not report \(k=1\) with known extras.

## Human

Confirm or reject `extra_sites` that are not obvious token clones. Confirm new axes the agent added as `proposed`. Confirm entry points still match the public surface.

## Not done if

- `product/` disagrees with the brief or with the code’s authorities.
- Dormant/frozen behavior was implemented.
- Tests recopy a set the authority already holds.
