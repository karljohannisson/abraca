# Maintainability principles

Ten atoms. Jointly they cover the cost of maintaining a codebase. They do not overlap. Lower score is cheaper.

They split along a maintenance task:

1. **Orient** — land on the intended site.
2. **Load** — hold what you must understand to edit it.
3. **Edit** — change the representations of one reason.
4. **Check** — learn whether you missed something or broke a dependent.

Standing tax on orient and load: **Mass** that should not exist.

| Group | Principles |
|---|---|
| Edit | [1 degree](01-co-change-degree.md), [2 locality](02-co-change-locality.md), [3 strength](03-co-change-strength.md) |
| Load | [4 size](04-intra-site-size.md), [5 complexity](05-intra-site-complexity.md), [6 mixing](06-concern-mixing.md), [7 comprehension coupling](07-comprehension-coupling.md) |
| Orient | [8 findability](08-findability.md) |
| Check | [9 checkability](09-checkability.md) |
| Mass | [10 accidental volume](10-accidental-volume.md) |

Setup for 1–9: a **registry of change axes** (not a full requirements matrix). Each live axis has an id, a short statement, a likelihood \(P(r)\), a change shape, exactly one **authority** (`encodes`), and optional **`verifies`** tests. No `uses` links.

**Headline scores use confirmed sites and labels.** A scanner floor is a lower bound. “Scanner found nothing” is not proof of zero.

A single combined Python number (goal 3) is not defined here. These remain separate scores on different scales.

---

Shared terms show up in row 1 the first time they are needed; later rows reuse them.

| # | Principle | Group | What it is | How we measure it |
|---|---|---|---|---|
| 1 | [Co-change degree](01-co-change-degree.md) | **Edit** — cost of actually changing the representations of one reason | For one **change axis** \(r\) (an independent, expectable reason the code was designed to absorb, e.g. “the set of countries may grow”), how many distinct **representations** must be edited. A representation (also **site**) is a place that *encodes* that knowledge, not a place that only *reads* it. The **authority** is the one site allowed to know it. Extra copies (a second list, a recopied test) raise the cost; a loop over the authority does not. | \(\sum_r P(r)\cdot\max(k(r)-1,0)\). \(P(r)\) is the likelihood that reason occurs over the life of the system, in \([0,1]\). \(k(r)\) is the number of confirmed representations of \(r\). \(k-1\) is the extra sites after the one unavoidable edit. Frozen axes (\(P\approx 0\)) are omitted. Automatic token-scan of the authority’s members is a **floor**; headline \(k\) needs a hunt plus confirm. |
| 2 | [Co-change locality](02-co-change-locality.md) | **Edit** | How far apart those sites sit in the program’s **containment tree** (function inside type inside module inside package inside deployable — the nested scopes the language gives you). Same count of copies can be cheap if they share a function, or expensive if they live in two services. | \(\sum_r P(r)\cdot L(r)\). \(L(r)\) is the size of the smallest box that contains every confirmed site: 0 = one site or same innermost scope; 1 = same class; 2 = same module; 3 = same package; 4 = same deployable; 5 = crosses deployable. \(L=0\) when \(k\le 1\). Automatic once sites exist. |
| 3 | [Co-change strength](03-co-change-strength.md) | **Edit** | How *implicit* the agreement is among extra sites and the authority — grepable names vs synonyms vs lockstep order vs a second algorithm. **Name** means the extra site reuses the authority’s tokens (`"US"`). **Meaning** is the same knowledge in other words (`"USA"`, `is_domestic()`). **Position** is index/arity alignment without those names. **Algorithm** is a second procedure that must stay equivalent. **Dynamic** is timing, execution order, identity, or a multi-value constraint. | \(\sum_r P(r)\cdot S(r)\). \(S(r)\) is the worst extra site vs the authority: 0 = no extras, or extras are Name only; 1 = Meaning; 2 = Position; 3 = Algorithm; 4 = Dynamic. Name-level extras cost 0 *here* (they already cost in #1). Name is automatic; anything stronger needs confirm. |
| 4 | [Intra-site size](04-intra-site-size.md) | **Load** — cost of holding the local edit in mind | How large the **enclosing unit** is: the innermost function/method that contains the site, or the module body if the encoding is not in a function. This is bulk of that unit, not how branchy it is. | \(\sum_r P(r)\cdot Z(r)\). \(n(s)\) = AST **statement** count of the enclosing unit of site \(s\) (an AST is the parsed tree of the program; a statement is a node such as an assignment or `if`, not a physical line). \(T=15\) is the Python working-set bound. \(Z(r)\) is the **mean** of \(\max(n(s)-T,0)\) over confirmed sites — mean so we do not recount extra sites already in \(k\). A whole country table in one assignment is one statement. Automatic. |
| 5 | [Intra-site complexity](05-intra-site-complexity.md) | **Load** | How gnarly that same enclosing unit’s **control flow** is (branches, nesting, tangled state) — independent of how many statements it has. A long straight script is large (#4) and simple; a tiny state machine is small and complex. | \(\sum_r P(r)\cdot C(r)\). \(C(r)\) is the mean **cognitive complexity** (Sonar/Campbell: extra cost for nesting and breaks in linear flow, not raw path count) of those units. Straight-line code is 0. Automatic. CRAP’s complexity input is this; test coverage is not. |
| 6 | [Concern mixing](06-concern-mixing.md) | **Load** | How many *other* live change axes also have a representation in that same unit. Dual of locality: copies of *this* \(r\) should sit together; *different* reasons should not share a unit. | \(\sum_r P(r)\cdot M(r)\). For a unit \(u\), \(R(u)\) is the set of live axes that have a confirmed site in \(u\). \(M(r)\) is the mean over sites of \(\max(\lvert R(u)\rvert-1,0)\) — extra *other* reasons in the unit. Automatic given the site map. |
| 7 | [Comprehension coupling](07-comprehension-coupling.md) | **Load** | How much *other* same-repo code you must **understand but not edit** (callees, leaked internals). **Fan-out** is how many distinct definitions the unit reaches for. Stdlib and third-party do not count; extra sites of *this* \(r\) do not count (you edit those; that is #1). | \(\sum_r P(r)\cdot H(r)\). \(h(s)\) = number of distinct same-repo definitions the enclosing unit of \(s\) **directly** references, excluding names defined in that unit, other sites of this \(r\), stdlib, and third-party. \(H(r)\) is the mean of \(h(s)\). Static resolution is a floor (dynamic imports under-count). |
| 8 | [Findability](08-findability.md) | **Orient** — cost of landing on the right first place | How hard it is, given only the *statement* of \(r\) (“new country codes may be added”), to find the authority in the code. The registry pointer is the answer key, not a search hint. A better-named clone that out-ranks the authority is a findability failure. | \(\sum_r P(r)\cdot F(r)\). A fixed ranker scores every project symbol by token overlap with the statement (qualified name, then first docstring line). \(\mathrm{rank}(r)\) is the 1-based position of the authority. \(F(r)=\min(\mathrm{rank}(r)-1,50)\); missing authority \(\Rightarrow F=50\). \(F=0\) means the authority is the top hit. Automatic. |
| 9 | [Checkability](09-checkability.md) | **Check** — cost/risk of knowing the edit worked | After you change the authority, whether a miss or a broken dependent is caught **mechanically**. **`verifies`** are tests tagged as checking this \(r\). They must *read* the authority (iterate/parametrize from it), not recopy its members. **Fail-loud** means uses break statically when the change shape requires per-variant handling (exhaustive `match`, types). Coverage % is not this score. | \(\sum_r P(r)\cdot V(r)\). \(V(r)\in\{0,1,2,3\}\): 0 = authority-driven verifies, and fail-loud where the change shape needs it; 1 = only one of those two; 2 = some test imports the module but does not bind or fail-loud; 3 = no automated reference to the authority’s module. Fail-loud does not apply when uses *should* keep working as the set grows. Automatic given tags + AST. |
| 10 | [Accidental volume](10-accidental-volume.md) | **Mass** — standing search tax from code that should not exist | How much of the codebase is **unreachable** from declared **entry points** (program starts and public API) plus live authorities. Reachable duplication is still #1; a huge *live* function is #4; this is dead mass. | \(u =\) (unreachable statements) / (total statements). \(u\in[0,1]\). One system number, not a sum over \(r\). Static follow-the-references from entry points is a floor; plugins/dynamic imports need confirm so live code is not marked dead. |

CRAP = **#5 × (lack of coverage)**. Coverage is only a hint toward #9; #9’s headline is authority-binding and fail-loud, not %.
