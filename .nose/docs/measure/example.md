# Score the dup fixture

The seed has no product. The scorer is checked on `.nose/tests/fixtures/dup`, a tiny app with a duplicated country list.

From the repo root:

```
PYTHONPATH=.nose python3 -m unittest discover -s .nose/tests -v
PYTHONPATH=.nose python3 -m maintainability --root .nose/tests/fixtures/dup
```

You should see 15 tests pass and:

```
W (headline) 0.7833   [0,5] lower=cheaper
W (floor)    0.6167   scanner only; not proof of zero extras
```

`countries` is `k=3` (authority, scan extra in `recopy.py`, confirmed meaning extra in `clone.py`). Volume is `0.3333`.

A clone’s `product/` stays empty until Phase 1. Do not copy this fixture into `product/`.
