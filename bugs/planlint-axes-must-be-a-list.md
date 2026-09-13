# Planlint rejects real `product/axes.yaml`

**Status:** open.

**Where.** `.nose/planlint/__init__.py` `main()`.

**What is wrong.** `main()` requires `axes.yaml` to be a YAML list of rows. Real registries (`product/axes.yaml`, `.nose/example/product/axes.yaml`, `.nose/docs/workflow/templates/axes.yaml`) are `{version, axes: [...]}` maps. `python3 -m planlint` on the example exits 1 with `must be a YAML list of axis rows`. Fixture tests never call `main()`, so they stay green.

**Why it matters.** Agents who "fix" axes.yaml into a bare list break `load_registry`, which does `axes_raw.get("axes")`.

**Fix.** Accept a list or a mapping with an `axes` key, same as `load_registry`. Keep a CLI test on the example or template axes file.
