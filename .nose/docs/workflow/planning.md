# Tier 2 — Planning

Run when: greenfield, the brief changed, a slice starts, or implementation would need an undeclared \(r\).

Human and agent share one surface: `product/`. Chat is for probes, not the lock.

## Loop

1. **Ingest** the brief into `product/requirements.md` (agent drafts, human owns). Split **Frozen** from the live product.
2. **Extract axes.** Independent expectable reasons, clustered by *what can change without the others*. Draft rows `status: proposed`.
3. **Probe** only what would split, merge, or set `shape` / `p`. Write questions in `product/probes.md`. Do not interview for a full spec.
4. **Fold answers** into `axes.yaml` and Frozen. Delete resolved probes. Set `status: locked` or `dormant`.
5. **Propose authorities** (symbol + path) so statement tokens appear in the name. Propose entry points.
6. **Slice.** Current slice ships the smallest product that is honest about locked high/medium axes (stubs/ADTs allowed). Dormant and low-\(P\) rows get a *place* only if a tiny port now prevents later shotgun surgery; no frameworks.
7. **Stop planning** when probes are empty or only dormant-shape questions remain, and yaml matches the human’s last answers.

## Probe types (only these)

| Ask | To decide |
|---|---|
| Can A happen without B? | Split vs merge |
| Set of members vs new mapping vs presentation vs rename? | `shape` |
| In-process vs another deployable? | Authority grain and locality |
| Will this happen / do we design for it? | locked vs frozen vs dormant |

Do not ask the human to name modules, tests, or member lists.

## Greenfield first slice

Create authority modules (docstring = statement) before feature depth. Do not implement dormant rows. Do not add a second member, variant, or UI until the slice says so.

Worked example of this loop: this repo’s `product/` (chat TUI).
