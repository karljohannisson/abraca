# Product intent files

Per-repo planning surface. Not a requirements-to-code matrix. No `uses` links.

| File | Holds | Source of truth for |
|---|---|---|
| `product/requirements.md` | Product brief, frozen decisions, **current slice** | What to build now; what must not be designed for |
| `product/axes.yaml` | Live and dormant change axes | \(r\), \(P\), shape, authority, `verifies` |
| `product/entry-points.yaml` | Program starts and public API; optional `code_roots`, `exclude`, `confirmed_live`, `deployables` | Accidental-volume roots (with live authorities); which trees the metric parses |
| `product/probes.md` | Open questions that would split, merge, or set shape | Unresolved planning only |

`docs/principles/` is not product intent.

## Field ownership (`axes.yaml`)

| Field | Who authors | Who confirms |
|---|---|---|
| `id`, `statement`, `p`, `shape`, `status` | Human (agent may **draft** from a brief) | Human |
| `authority.symbol`, `authority.path` | Agent proposes | Human, when it matters (competing encodings) |
| `verifies` | Agent writes tests and lists them | Human on review if a test recopies |
| `extra_sites` | Agent hunts (path, `strength`, `status`) | Human; only `status: confirmed` enter headline \(k\). Scanner floor is not headline \(k=1\) |

`status`: `proposed` (drafted, not agreed) · `locked` (design for it) · `dormant` (declared, do **not** implement until shape is known).

`p`: `high` · `medium` · `low`. Omit \(P \approx 0\) and unexpectable reasons; put those under **Frozen** in `requirements.md`, not as rows.

`shape` (must match [principle 9](../principles/09-checkability.md)):

| Value | Meaning |
|---|---|
| `set_grows` | Members added; uses should pick them up. Fail-loud does not apply. |
| `new_variant` | New arm needs handling. Exhaustive match / typed visitor. |
| `signature_rename` | Name/arity/field change. Types should break uses. |
| `formula_value` | Presentation, formula, stored value. Verifies read the authority. |
| `unknown` | Only with `status: dormant`. |

Exactly one `authority` per locked row. Do not hand-maintain member lists in yaml; members live in the authority in code.

`extra_sites` (optional, on a locked row):

```yaml
extra_sites:
  - path: src/foo.py          # file containing a confirmed extra encoding
    status: confirmed         # proposed | confirmed
    strength: meaning         # name | meaning | position | algorithm | dynamic
```

Token-scan Name extras are detected in code and need not be listed. List Meaning and stronger, and any extra the scanner missed.

`entry-points.yaml` optional keys: `code_roots` (path prefixes to parse), `exclude` (subtract), `confirmed_live` (static-dead but actually live), `deployables` (prefixes; default one deployable). Combined score: [metric.md](../metric.md).

## Generated repo layout

```
AGENTS.md                 # points here
docs/principles/          # atoms
docs/workflow/            # this package
product/                  # intent (human + agent)
  requirements.md
  axes.yaml
  entry-points.yaml
  probes.md
src/                      # one package; authority paths in axes.yaml
tests/                    # verifies listed in axes.yaml
```
