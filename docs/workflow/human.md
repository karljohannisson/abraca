# Tier 0 — Human

You maintain **what the software is** and **which changes it must absorb**. You do not have to name files, list tests, or compute scores.

## You write

1. **Brief** in `product/requirements.md` — what it is, who uses it, current slice.
2. **Frozen** in the same file — decisions that will not change, or that you refuse to design for.
3. **Axes** in `product/axes.yaml` — each live reason: id, short statement, `p`, `shape`, `status`.
4. **Answers** in `product/probes.md` — independence, expectability, shape. Then the agent folds answers into yaml and deletes the resolved probe.

Entry points: confirm the agent’s list (what is the program / public API).

## You confirm (do not author from scratch)

- Clustering of \(r\): one event vs two axes; merge if they cannot change alone.
- Authority when several encodings exist.
- Extra sites the agent found that are not the same tokens.
- Dead vs plugin-live code.

“Scanner found nothing” is not your sign-off on \(k=1\) or \(u=0\).

## You do not

- Fill a requirements-to-code matrix or `uses` map.
- Enumerate every feature as an axis (features are the brief; axes are *independent expectable changes*).
- Pick library folders unless you are overriding an authority.
- Ask the agent to build a framework for a `dormant` or frozen reason.

## When the product changes

Edit the brief and the affected rows (add / split / freeze / change `p` or `shape`). The next agent turn starts at [planning](planning.md) until `product/` matches.
