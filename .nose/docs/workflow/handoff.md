# Planning → implementation handoff

Planning is done only when every box below is true. If any is false, stay in [planning.md](planning.md). [implementing.md](implementing.md) may assume this list; it must not invent axes or unfreeze Frozen.

## The human accepted a recap

In ordinary language they agreed: what it is, the current slice, what is off the table, what can change independently (including inferred bets they said yes to), what is later.

That recap is written into `product/requirements.md` (brief, Frozen, current slice) and `product/axes.yaml`. Chat is not the lock.

## `product/axes.yaml` is crisp

Every row:

| Field | Required |
|---|---|
| `id` | Stable slug you chose |
| `plain` | One sentence the human would recognize |
| `statement` | Design sentence (findability tokens live here) |
| `because` | Why this is its own axis (their words, or your inference why) |
| `origin` | `brief` · `human` · `inferred` |
| `p` | `high` · `medium` · `low` from their expect / maybe / basically never |
| `shape` | From domain answers ([artifacts.md](artifacts.md)); `unknown` only if `dormant` |
| `status` | `locked` · `dormant` (no leftover `proposed` after the recap) |
| `authority` | Symbol + path on **locked** rows; `null` on dormant |
| `verifies` | Empty until you add tests; then the paths |

No two locked rows change only together (independence was probed). No frozen reason is a row.

## Slice and mass

- Current slice names the smallest honest product: first members/variants allowed, and what is still forbidden (second vendor, second UI, …).
- Dormant rows have **no** module.
- `entry-points.yaml` lists the program the human would actually start, plus `code_roots` / `exclude` (exclude `.nose`).

## You may now implement

One authority per locked row. Uses read; they do not recopy. Do not encode frozen or dormant reasons. After the slice, [review.md](review.md).
