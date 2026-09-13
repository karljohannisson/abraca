# Combined maintainability metric

One number \(W\) from the [ten atoms](principles/README.md). Lower is cheaper. Version **1**. Language-neutral. Python fills the atoms in [measure/python.md](measure/python.md).

The atoms stay the diagnosis. This file only says how they become one score \(W\), and what the scanner may claim.

## Setup

Required for atoms 1–9 and for \(W\) (paths are at the **product root**, not inside `.nose/`):

- `product/axes.yaml` — locked axes with \(P\), shape, authority path, optional `verifies` and `extra_sites`
- `product/entry-points.yaml` — program starts / public API; optional `code_roots`, `exclude`, `confirmed_live`

CLI (from the product root): `PYTHONPATH=.nose python3 -m maintainability`. Optional `--max-w` fails the process if headline \(W\) is above the cap (see [measure/python.md](measure/python.md)).

Without `product/axes.yaml`, the CLI exits 2. Atoms 1–9 are undefined. Volume is not scored on its own.

## \(P(r)\)

| Label | Value |
|---|---|
| high | \(1.0\) |
| medium | \(0.5\) |
| low | \(0.25\) |

Numeric \(P \in [0,1]\) in yaml is allowed and used as-is. Non-finite values and values outside that interval are a registry error. Phase 3 stores human frequency 1–5 and writes `p` from that table ([workflow/phase-3-axes.md](workflow/phase-3-axes.md)). Dormant and proposed rows are omitted from every sum. Frozen reasons are not rows.

## Atoms (unchanged)

Raw scores, same formulas as the principle files:

| Atom | Raw |
|---|---|
| degree \(D\) | \(\sum_r P(r)\cdot\max(k(r)-1,0)\) |
| locality \(L_\Sigma\) | \(\sum_r P(r)\cdot L(r)\) |
| strength \(S_\Sigma\) | \(\sum_r P(r)\cdot S(r)\) |
| size \(Z_\Sigma\) | \(\sum_r P(r)\cdot Z(r)\) |
| complexity \(C_\Sigma\) | \(\sum_r P(r)\cdot C(r)\) |
| mixing \(M_\Sigma\) | \(\sum_r P(r)\cdot M(r)\) |
| coupling \(H_\Sigma\) | \(\sum_r P(r)\cdot H(r)\) |
| findability \(F_\Sigma\) | \(\sum_r P(r)\cdot F(r)\) |
| checkability \(V_\Sigma\) | \(\sum_r P(r)\cdot V(r)\) |
| volume \(u\) | unreachable statements / total statements |

Always report these ten. Do not drop them in favor of \(W\).

## Floor vs headline

| | Sites in \(k\) | \(S\) labels | Unreachable |
|---|---|---|---|
| **Floor** | Authority + token-scan extras | Name only (so extras contribute \(S=0\)) | Static closure |
| **Headline** | Floor + yaml `extra_sites` with `status: confirmed` | Confirmed labels on those extras; scan extras stay Name | Static, minus `confirmed_live` paths |

Headline is what \(W\) uses. Floor is a lower bound. Printing floor \(k=1\) is not proof that \(k=1\).

Token-scan extras: string literals (or names that are not imports of the authority) equal to a seeded member token, in an enclosing unit that is not the authority. Attribute access of an imported authority is a **use**, not a site.

## Combined \(W\)

Raw atoms are on different scales and grow with \(\sum P\). \(W\) is a **P-weighted mean of capped per-axis intensities**, then an equal-weight sum of the five maintenance groups. Caps exist only to put intensities in \([0,1]\); they are not quality gates and do not change the raw atoms.

Per-axis intensity \(\hat{x}(r)\):

| Atom | \(x(r)\) | Cap | \(\hat{x}(r)\) |
|---|---|---|---|
| degree | \(\max(k-1,0)\) | 4 extras | \(\min(x/4,1)\) |
| locality | \(L\) | 5 | \(L/5\) |
| strength | \(S\) | 4 | \(S/4\) |
| size | \(Z\) | 30 excess stmts | \(\min(Z/30,1)\) |
| complexity | \(C\) | 25 cog | \(\min(C/25,1)\) |
| mixing | \(M\) | 4 extra reasons | \(\min(M/4,1)\) |
| coupling | \(H\) | 10 fan-out | \(\min(H/10,1)\) |
| findability | \(F\) | 50 | \(F/50\) |
| checkability | \(V\) | 3 | \(V/3\) |

P-weighted mean over locked axes that have an authority path:

\[
\bar{x} = \frac{\sum_r P(r)\,\hat{x}(r)}{\sum_r P(r)}
\]

If there are no such axes, \(\bar{x}=0\) for atoms 1–9.

Groups (each in \([0,1]\)):

\[
\begin{align*}
\mathrm{Edit} &= (\bar{D}+\bar{L}+\bar{S})/3 \\
\mathrm{Load} &= (\bar{Z}+\bar{C}+\bar{M}+\bar{H})/4 \\
\mathrm{Orient} &= \bar{F} \\
\mathrm{Check} &= \bar{V} \\
\mathrm{Mass} &= u
\end{align*}
\]

\[
W = \mathrm{Edit}+\mathrm{Load}+\mathrm{Orient}+\mathrm{Check}+\mathrm{Mass} \in [0,5]
\]

\(W=0\) is the ideal. Mass is **additive**: dead code costs even when the live graph is cheap. (It also taxes future orient/load; we do not multiply, to avoid double-counting in \(W\).)

Equal group weight so Load’s four atoms do not outvote Orient’s one.

## Application notes

Language-specific grains live in [measure/python.md](measure/python.md). `origin`, `plain`, `because`, `frequency`, `requirements` on an axis are ignored. They are Phase 3 fields ([workflow/artifacts.md](workflow/artifacts.md)).

## What \(W\) can claim without a software human

The \(W\) gate is the backstop for [workflow/phase-4-task.md](workflow/phase-4-task.md) and [workflow/phase-5-handover.md](workflow/phase-5-handover.md). The human does not drive phases or classify sites.

A Phase 4 **plan** is not scored. Lint it against `axes.yaml` ([workflow/phase-4-plan.md](workflow/phase-4-plan.md)) before any task. Architecture is one authority per locked axis — not class diagrams that skip the registry.

- The registry may be **entirely agent-authored**. Scoring does not care who typed the yaml.
- **Floor** is automatic (authority + token-scan Name extras). The agent must not claim \(k=1\) or “no extras” from the floor.
- **Headline** extras of Meaning+ need a hunt. The human is **not** a site classifier. Treat hunt hits as **defects to delete**, not as yaml for the human to confirm. `extra_sites` with `status: confirmed` is only for a software collaborator who is keeping an extra this slice.
- `confirmed_live` is the one metric field that may need a **product** question (“do you still use the extra-commands plugin?”), never a metrics question.
- Translate \(W\) for the human in one sentence if it moved. Do not ask them to interpret atoms, caps, or groups.
- A Phase 4 **task** (and then handover) is **claimable** without a software reviewer when verifies pass, hunt hits are gone, dormant/frozen code is absent, and headline \(W\) did not rise (or the rise is logged against a Phase 2 id). That is how 3 makes the agent-only implement phase trustable without someone looking at sites.

## Not \(W\)

CRAP, coverage %, LOC, and any weighted mash that skips the atoms. If a later version changes caps or group weights, bump the version here and in the CLI.
