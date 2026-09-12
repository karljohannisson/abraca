# Product intent files

Per-repo planning surface. The **agent writes every file**. The human talks ([human.md](human.md)). Not a requirements-to-code matrix. No `uses` links.

| File | Holds | Source of truth for |
|---|---|---|
| `product/requirements.md` | Product brief, frozen decisions, **current slice** (language the human accepted) | What to build now; what must not be designed for |
| `product/axes.yaml` | Live and dormant change axes | \(r\), \(P\), shape, authority, `verifies`, origin |
| `product/entry-points.yaml` | Program starts and public API; optional `code_roots`, `exclude`, `confirmed_live`, `deployables` | Accidental-volume roots; which trees the metric parses |
| `product/probes.md` | Open questions that would split, merge, or set shape/likelihood | Unresolved planning only |

`.nose/docs/principles/` is not product intent. It is part of the seed.

## Field ownership (`axes.yaml`)

| Field | Who authors | Who confirms |
|---|---|---|
| `id`, `statement`, `plain`, `because`, `origin`, `p`, `shape`, `status` | Agent (from talk + inference) | Human confirms the **plain recap**, not the yaml |
| `authority.symbol`, `authority.path` | Agent | Nobody, unless two encodings compete and a software person is present |
| `verifies` | Agent writes tests and lists them | — |
| `extra_sites` | Agent hunts | **Not the human.** Delete the extra, or stop. `status: confirmed` is only if a software collaborator exists; see [metric.md](../metric.md) |

`origin`: `brief` (they described it) · `human` (they said “this should be an axis because …”) · `inferred` (you proposed it).

`because`: one line. For `inferred`, the bet. For `human`, their xyz. For `brief`, the clustering why.

`plain`: one sentence they would recognize. Used in recaps. `statement` is the design sentence (findability tokens).

`status`: `proposed` (drafted, not agreed) · `locked` (design for it) · `dormant` (declared, do **not** implement until shape is known). After an accepted recap, no `proposed` rows remain.

`p`: `high` · `medium` · `low` from expect / maybe / basically never. Omit \(P \approx 0\) and unexpectable reasons; those are **Frozen** in `requirements.md`, not rows.

`shape` (must match [principle 9](../principles/09-checkability.md)):

| Value | Meaning | Domain cue |
|---|---|---|
| `set_grows` | Members added; uses should pick them up. Fail-loud does not apply. | “another one of the same kind” |
| `new_variant` | New arm needs handling. Exhaustive match / typed visitor. | “a different kind that needs its own handling” |
| `signature_rename` | Name/arity/field change. Types should break uses. | “we might rename or change the fields” |
| `formula_value` | Presentation, formula, stored value. Verifies read the authority. | “wording, layout, or the number we show” |
| `unknown` | Only with `status: dormant`. | “we don’t know what it looks like yet” |

Exactly one `authority` per locked row. Do not hand-maintain member lists in yaml; members live in the authority in code.

`extra_sites` (optional, on a locked row) — agent-owned hunt, not a human form:

```yaml
extra_sites:
  - path: src/foo.py          # file containing a confirmed extra encoding
    status: confirmed         # proposed | confirmed
    strength: meaning         # name | meaning | position | algorithm | dynamic
```

Token-scan Name extras are detected in code and need not be listed. List Meaning and stronger only when a software collaborator confirmed them **and** you are not deleting them this slice. Prefer delete.

`entry-points.yaml` optional keys: `code_roots` (path prefixes to parse), `exclude` (subtract), `confirmed_live` (static-dead but actually live — ask in domain language: “do you still use this?”), `deployables` (prefixes; default one deployable). Combined score: [metric.md](../metric.md). Run from the product root: `PYTHONPATH=.nose python3 -m maintainability`.

## Generated repo layout

```
AGENTS.md                 # thin; points at .nose/
.nose/                    # seed (copy this)
  README.md
  docs/                   # start: docs/README.md
  maintainability/        # python -m maintainability
  tests/                  # tests for the metric, not the product
product/                  # THIS software (agent-written)
  requirements.md
  axes.yaml
  entry-points.yaml
  probes.md
src/<name>/               # authorities
tests/                    # product verifies
```
