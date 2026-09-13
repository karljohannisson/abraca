# nose

Clone this repo. Open it with a coding agent. **Talk** about what you want to build until it exists.

You do not pick phases, edit yaml, or run a process. The agent does.

The agent’s entry is [`AGENTS.md`](AGENTS.md). How it works lives in [`.nose/`](.nose/README.md) (dot directory — open it if a listing hides it).

## Install into a new project

One command, from this repo:

```
./nose-new <name> [parent-dir]
```

Copies `AGENTS.md` + `.nose/` into `<parent-dir>/<name>/` (default parent: `.`),
`git init`s it with a seed commit, and leaves `product/` empty at Phase 1.
Then open that folder with a coding agent and talk.

The example finished run (`.nose/example/`) travels with the seed so the agent
can imitate a complete loop; the fresh product's own `product/` starts empty.

