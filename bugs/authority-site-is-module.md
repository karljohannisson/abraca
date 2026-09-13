# Authority site is the module

**Status:** fixed.

**Where.** `sites_for_axis` in `.nose/maintainability/sites.py`.

**What the principle says.** Principle 4 (intra-site size) measures the innermost function that holds the encoding, or the module body if the encoding is not in a function. The registry stores both `authority.path` and `authority.symbol`.

**What the scorer does.** It always plants the authority site on the **module** unit of `authority.path`. Other functions in that file are treated as local shape, not extra copies. Size, complexity, mixing, and coupling for the authority therefore score the whole file.

**Why it is parked.** Changing the grain would move fixture \(W\) and mix with the language-backend split. Fix it in its own change: point the authority site at the enclosing unit of `authority.symbol`.
