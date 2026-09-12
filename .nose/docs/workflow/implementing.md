# Tier 3 — Implementing

Input: [handoff.md](handoff.md) must already be true. If a locked row lacks authority path or shape, or Frozen disagrees with the last recap, return to [planning.md](planning.md). Do not invent axes.

Code against **locked** axes, including `origin: inferred`. Principles: [map](../principles/README.md).

## Edit (1–3)

- New member of a `set_grows` axis: one row in the authority. Call sites lookup/iterate.
- New `new_variant` arm: one variant on the ADT plus its adapter; update exhaustive matches (they should fail until you do).
- Extra sites of one \(r\) live as close as the language allows. Different live \(r\) do not share an enclosing function.

## Load (4–7)

- Keep the authority’s enclosing unit small and straight.
- Composition modules *use* other authorities; they do not encode them.
- Same-repo fan-out: call a port, not a pile of internals.

## Orient (8)

- If you rename an authority, update `axes.yaml` and keep statement tokens in the new name.

## Check (9)

- Every locked axis in the slice has at least one `verifies` that reads the authority.
- Tests that recopy tokens are extra sites; rewrite them to iterate.

## Mass (10)

- New public functions are entry points only if listed, or they are reached from listed ones / live authorities.
- Delete code the slice no longer reaches.

## Slice discipline

Implement the current slice in `requirements.md`. A locked low-\(P\) port may exist as a trivial first member (e.g. in-memory history). A `dormant` axis has **no** code. Frozen is not a secret second slice.

After the slice compiles and `verifies` pass, run `PYTHONPATH=.nose python3 -m maintainability`. Prefer not to raise headline \(W\). Recopying tokens in tests raises degree (and usually locality).
