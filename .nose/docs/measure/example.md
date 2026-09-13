# Score the dup fixture

The seed has no product. The scorer is checked on `.nose/tests/fixtures/dup`, a tiny app with a duplicated country list.

From the repo root:

```
PYTHONPATH=.nose python3 -m unittest discover -s .nose/tests -v
PYTHONPATH=.nose python3 -m maintainability --root .nose/tests/fixtures/dup
```

The suite exits 0. The dup CLI exits 1 because `recopy.py` recopies `US`:

```
W (headline) 0.4793   [0,5] lower=cheaper
W (floor)    0.3960   scanner only; not proof of zero extras
```

`countries` is `k=3` (authority, scan extra in `recopy.py`, confirmed meaning extra in `clone.py`). Volume is `0.2143`.

```
scan extras (floor; delete the listed token recopy):
  countries  src/app/recopy.py:2  app.recopy  string  US
```

A clone’s `product/` stays empty until Phase 1. Do not copy this fixture into `product/`.
