# Principle 9 — Checkability

**Status:** locked.

**Group.** Check — cost/risk of knowing the edit worked. Map: [README](README.md).

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

| Symbol | Meaning |
|---|---|
| \(r\), \(P(r)\), authority | Same registry as principle 1 |
| \(V(r)\) | Miss-risk ordinal in \(\{0,1,2,3\}\) |

| \(V\) | After editing the authority for this \(r\) |
|---|---|
| 0 | Fail-loud does not apply to the shape (set grows, formula/value), and a **`verifies`** test **reads** the authority (iterates, parametrizes, imports members — does not recopy). Or, for shapes where fail-loud applies and is implemented: reads the authority **and** the fail-loud check is exhaustive (no `_` / `else` default on every project `match`/`if-elif` on that type). |
| 1 | Authority-driven verifies exist but the fail-loud half is missing **or unmeasured**: reads without exhaustive fail-loud (where fail-loud applies and is implemented), exhaustive fail-loud without authority-driven verifies, or — for `signature_rename` — reads without any implemented fail-loud (a reading verifies can never certify 0 there; see below). |
| 2 | Some test imports the authority’s module, but it neither reads the authority nor fail-louds the shape (recopy, incidental import, coverage without binding). |
| 3 | No automated test references the authority’s module, and fail-loud does not apply or is absent. |

Change shape (from the registry) decides whether fail-loud applies:

| Shape | Fail-loud means |
|---|---|
| Set grows; uses should pick up members automatically | Fail-loud **does not apply**. \(V=0\) if verifies *read* the authority. Iteration is the correct use. |
| New variant needs handling | Exhaustive match / typed visitor without default. Python implements exhaustive `match` on the authority subject. |
| Signature / field rename | Type-checker or attribute errors at uses. **Not implemented** for Python: the backend cannot observe this fail-loud, so a verifies test that reads the authority scores \(V=1\), never \(V=0\). [bugs/signature-rename-fail-loud.md](../../../bugs/signature-rename-fail-loud.md). |
| Formula / value | No structural fail-loud; verifies that read inputs/authority and assert outputs. |

## How \(V\) is obtained

1. Take `verifies` and the authority from the registry; take change shape.
2. Language backend: does a verifies test *read* the authority (attribute/iteration/parametrize from it) vs recopy tokens?
3. If fail-loud applies and the backend implements that shape: exhaustive matches or typed uses.
4. Else if any test imports the module → at best \(V=2\).
5. Read \(V\) off the table.

Automatic given registry tags plus a language backend, for the shapes that backend implements. Type-level fail-loud assumes a type checker is in the project (declared setup) and is not implemented for Python yet. Headline uses confirmed `verifies` links; untagged tests that actually read the authority may be confirmed into the registry and then count. Python details: [measure/python.md](../measure/python.md).

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
