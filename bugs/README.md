# Bugs

Tracked defects. Status lives on each file. Scorer grains that are not Goal 0 work stay here too.

| Id | Status | What |
|---|---|---|
| [example-cli-never-calls-main](example-cli-never-calls-main.md) | fixed | Recorded `python3 -m world` never calls `main()` |
| [planlint-axes-must-be-a-list](planlint-axes-must-be-a-list.md) | fixed | Planlint rejects `{version, axes}` registries |
| [planlint-ignores-template-encodes](planlint-ignores-template-encodes.md) | fixed | Planlint misses markdown `encodes:` bullets |
| [authority-site-is-module](authority-site-is-module.md) | fixed | Authority site is the whole file, not the symbol’s enclosing function |
| [signature-rename-fail-loud](signature-rename-fail-loud.md) | fixed (minimal) | `shape: signature_rename` does not check type or attribute breakage |

Measurement grains that *are* implemented live in [`.nose/docs/measure/python.md`](../.nose/docs/measure/python.md).
