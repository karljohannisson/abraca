# Bootstrap — first conversation, empty or new product

Run this when `product/` is missing, is a stub, or the human is starting a new codebase from the seed. After the first lock, later brief-changes use [planning.md](planning.md) only.

The human has [human.md](human.md). You never ask them to open a yaml file.

## Session script

1. **Listen.** What is it? Who uses it? What does “working” mean for the first version? What might change in their world later? Optional: they may say “this should be a change axis because …” — treat that as a named bet, not as the whole registry.
2. **Do not** mention modules, protocols, yaml, \(P\), shape, \(k\), or \(W\). Do not list files they should create.
3. **Infer** (see [planning.md](planning.md) inference rule). Silently draft independent reasons, including ones they did not name.
4. **Probe** in their language. Write the open questions in `product/probes.md` as you go. One round of **2–4** questions when you can. Ask only what would split, merge, set likelihood, or choose design-now vs later vs never.
5. **Write** `product/requirements.md`, `product/axes.yaml`, `product/entry-points.yaml`, `product/probes.md`. You own every field. Create the directories if needed.
6. **Recap in ordinary language** (not yaml):
   - what it is, and what this first version will do
   - what you will treat as **off the table** (frozen)
   - what can change independently, each in one sentence, each with *because*
   - which of those you inferred (say so: “you didn’t mention this; I think it is separate because …”)
   - what you will **not** build yet (dormant / later)
7. **Wait.** Yes / no / later / freeze that / “this should also be an axis because …”. Fold. Delete resolved probes. Repeat until the recap is accepted.
8. **Handoff.** [handoff.md](handoff.md) must be true. First code slice is **authorities only** (modules whose docstring is the statement, first member/variant only). Then [implementing.md](implementing.md).

## Empty-repo layout you create

```
AGENTS.md                 # already there if they copied the seed
.nose/                    # already there
product/
  requirements.md
  axes.yaml
  entry-points.yaml
  probes.md
src/<name>/               # after handoff, not before
tests/
```

Worked example of a finished first lock: this mothership repo’s `product/` (chat). Protocols there were **inferred**, not named by a software person.
