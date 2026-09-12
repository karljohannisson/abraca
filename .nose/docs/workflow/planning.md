# Tier 2 — Planning

Run when: greenfield ([bootstrap.md](bootstrap.md)), the brief changed, a slice starts, or implementation would need an undeclared axis.

You write every `product/` file. The human talks ([human.md](human.md)). Chat is for probes; the lock is `product/` plus a recap they accepted.

## Loop

1. **Listen** → draft `product/requirements.md` (brief, Frozen, current slice). Frozen = will not change, or they refuse to design for it.
2. **Extract named axes.** Independent expectable reasons they actually said, including “this should be a change axis because …”. Cluster by *what can change without the others*. Draft `status: proposed`.
3. **Infer unnamed axes.** Domain-typical independent reasons the brief did not name. Same clustering test. Each is a **bet**: `plain`, `because`, `origin: inferred`. Do not lock without yes / no / later.
4. **Probe** in **domain language**. Write questions in `product/probes.md`. Do not interview for a full spec. Prefer one round of 2–4 questions.
5. **Fold.** Update yaml and Frozen. Delete resolved probes. `locked` or `dormant`. No leftover `proposed` after they accepted the recap.
6. **Authorities** (you only): symbol + path so `statement` tokens appear in the name. Entry points the human would actually start.
7. **Slice.** Smallest product that is honest about locked high/medium axes (stubs/ADTs allowed). Dormant and low-\(P\) rows get a *place* only if a tiny port now prevents later shotgun surgery; no frameworks.
8. **Recap** in ordinary language, including inferred bets marked as such. Wait.
9. **Stop** when [handoff.md](handoff.md) is true.

## Inference rule

Propose axes the brief never named when they are independently expectable in this kind of product.

Each bet, in their language:

- one sentence (`plain`)
- **because** (why it is not the same as another row)
- what happens if we ignore it (shotgun later vs nothing)
- ask: design for it **now** / **later** (dormant, no code) / **never** (Frozen)

Do **not** implement a framework because “this often changes.” Locked vs dormant vs frozen still applies.

Example: they say “OpenRouter now, maybe OpenAI later.” Infer **protocols**: “Some companies use the same kind of connection; some use a different kind. A new company is not always a new kind of connection.” If yes → two axes. If “I don’t care” → Frozen or merge, with a note. A non-software person will not name this; you must.

## Domain probes (intents, not jargon)

Never ask: in-process vs deployable, `set_grows` vs `new_variant`, modules, \(P\) labels, \(k\), extra sites.

| You need | Ask |
|---|---|
| Split vs merge | “Could you add a new vendor without changing how the messages look?” |
| Likelihood | “Is this something you expect, a maybe, or basically never?” → `high` / `medium` / `low` |
| Shape | “When it happens, is it another one of the same kind, or a different kind of thing that needs its own handling?” Also: wording/layout/formula vs rename/fields vs “we don’t know yet.” |
| Now / later / never | “Make room now, remember it but don’t build it, or treat it as off the table?” |
| One product vs two | “Is this the same program, or a separate product?” |
| Human-suggested axis | “You’re saying X can change because Y. If X happens, does anything else on this list have to change with it?” |

Map answers to `shape` yourself ([artifacts.md](artifacts.md)). “We don’t know what it looks like yet” → `unknown` + `dormant`.

## Mind change

| They say | You do |
|---|---|
| “this should be a change axis because Y” | Proposed row, `origin: human`, `because: Y`. Probe independence. Still infer related unnamed axes. |
| “also Slack” | One question: another way to talk to the same program, or a separate product? Then member vs new axis. Update `product/`, then code. |
| “history on disk” | If history is locked: new member. If dormant: lock shape, then implement. |
| “we will never stream” | Frozen; remove streaming forks; do not keep the axis live. |

One question if the clustering is unclear. Then fold. Then implement. Do not leave the mind-change only in chat.

## Greenfield first slice

Create authority modules (docstring = `statement`) before feature depth. Do not implement dormant rows. Do not add a second member, variant, or UI until the slice says so.

Worked example: this repo’s `product/` (chat). `protocols` is inferred.
