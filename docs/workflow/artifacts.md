# Product intent files

Per-repo planning surface. Not a requirements-to-code matrix. No `uses` links.

| File | Holds | Source of truth for |
|---|---|---|
| `product/requirements.md` | Product brief, frozen decisions, **current slice** | What to build now; what must not be designed for |
| `product/axes.yaml` | Live and dormant change axes | \(r\), \(P\), shape, authority, `verifies` |
| `product/entry-points.yaml` | Program starts and public API | Accidental-volume roots (with live authorities) |
| `product/probes.md` | Open questions that would split, merge, or set shape | Unresolved planning only |

`docs/principles/` is not product intent.

## Field ownership (`axes.yaml`)

| Field | Who authors | Who confirms |
|---|---|---|
| `id`, `statement`, `p`, `shape`, `status` | Human (agent may **draft** from a brief) | Human |
| `authority.symbol`, `authority.path` | Agent proposes | Human, when it matters (competing encodings) |
| `verifies` | Agent writes tests and lists them | Human on review if a test recopies |
| `extra_sites` | Agent hunts | Human; scanner floor is not headline \(k=1\) |

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
