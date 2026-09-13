# `signature_rename` fail-loud is not implemented

**Status:** fixed (honest minimal version). The scorer now distinguishes `signature_rename` from `set_grows`: fail-loud is unmeasured for this shape, so a verifies test that reads the authority scores \(V=1\), never \(V=0\). No type checker was built. Documented in principle 9 and `.nose/docs/measure/python.md`.

**Where.** `checkability` in `.nose/maintainability/atoms.py`. Python `match` walk in `.nose/maintainability/languages/python.py`.

**What the principle says.** Principle 9 (checkability). For `shape: signature_rename`, fail-loud means a type checker or attribute errors at uses after a rename or field change.

**What the scorer does.** Fail-loud runs only when `shape == "new_variant"` (exhaustive `match` without `_` in Python). For `signature_rename`, \(V\) is “does a `verifies` test read the authority?”, same as `set_grows`.

**Why it is parked.** Real fail-loud needs a type checker (or an attribute-use analyzer that pretends to be one). Documented in principle 9 and in `.nose/docs/measure/python.md`.
