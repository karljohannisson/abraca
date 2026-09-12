# Principle 9 — Checkability

**Status:** locked.

**Property.** After an edit to \(r\), how much of “we missed something or broke a dependent” is caught mechanically, without a hunt.

**Direction.** Authority-driven checks and fail-loud uses → cheaper and less risky. Silence → more expensive and more risky.

**Principle.** A codebase is cheaper to maintain when changing the authority either cannot silently go wrong, or a small mechanical check says that it did.

This is **check**, after the edit. Not included: complexity of the unit (CRAP’s other half), extra representations (degree), implicit extras the tests never saw (strength — those remain a \(k\)/`S` miss), or how hard it was to find the authority.

Retest *labor* (how many tests import the module) is a diagnostic, not the headline: it mashes scales and double-counts fan-in. Headline is **miss-risk**.

## Score

\[
\sum_r P(r) \cdot V(r)
\]

Lower is cheaper.

| \(V\) | After editing the authority for this \(r\) |
|---|---|
| 0 | At least one **`verifies`** test **reads** the authority (iterates, parametrizes, imports members — does not recopy). And if the change shape requires per-variant handling, every project `match`/`if-elif` on that type is exhaustive (no `_` / `else` default). |
| 1 | One of those two is missing: authority-driven verifies without fail-loud (where fail-loud applies), or fail-loud without authority-driven verifies. |
| 2 | Some test imports the authority’s module, but it neither reads the authority nor fail-louds the shape (recopy, incidental import, coverage without binding). |
| 3 | No automated test references the authority’s module, and fail-loud does not apply or is absent. |

Change shape (from the registry) decides whether fail-loud applies:

| Shape | Fail-loud means |
|---|---|
| Set grows; uses should pick up members automatically | Fail-loud **does not apply**. \(V=0\) if verifies *read* the authority. Iteration is the correct use. |
| New variant needs handling | Exhaustive match / typed visitor without default. |
| Signature / field rename | Type-checker or attribute errors at uses. |
| Formula / value | No structural fail-loud; verifies that read inputs/authority and assert outputs. |

## How \(V\) is obtained

1. Take `verifies` and the authority from the registry; take change shape.
2. AST: does a verifies test *read* the authority (attribute/iteration/parametrize from it) vs recopy tokens?
3. If fail-loud applies: AST for exhaustive matches / typed uses.
4. Else if any test imports the module → at best \(V=2\).
5. Read \(V\) off the table.

Automatic given registry tags + AST, for the shapes above. Type-level fail-loud assumes a type checker is in the project (declared setup). Headline uses confirmed `verifies` links; untagged tests that actually read the authority may be confirmed into the registry and then count.

Coverage **percentage** is not \(V\). It can *propose* “this unit is untested” (\(V\) at least 2 if no import). CRAP = [principle 5](05-intra-site-complexity.md) × (lack of coverage); do not fold coverage into this ordinal beyond the table.

## What does not count

- Extra clones the suite never touches — still \(k\) and \(S\). A green \(V=0\) does not prove \(k=1\).
- Cognitive complexity.
- How many tests must run (\(R\): count of test modules importing the site’s module). Report \(R\) as a diagnostic if needed; not in \(\sum P\cdot V\).

## What is *not* a violation

- No fail-loud when the shape does not need it (set-grows + iteration).
- Uses that should *not* break when the set grows.

## Aliases (not extra principles)

ISO testability as miss-risk, exhaustiveness, “make illegal states unrepresentable” as fail-loud, proof-of-completeness *of uses*, authority-driven tests. Not CRAP (composite). Not “has unit tests” without binding to the authority.
