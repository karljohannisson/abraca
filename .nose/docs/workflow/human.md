# Tier 0 — Human

You know the product. You do not need to know software.

You **talk**. The agent writes every file under `product/`. You never have to open yaml, name a module, pick a test, or read a score.

## You say

- What it is, who uses it, what “working” means for now.
- What might change in your world later (vendors, channels, prices, languages, how people talk to it, how you store things, …).
- Optional: **“this should be a change axis because …”** — a reason you want the software to absorb without a rewrite. You do not have to find all of them. The agent will suggest others.
- **Yes / no / later / never** to the agent’s recap and to bets you did not name.
- Mind changes, in ordinary language: “also Slack”, “history on disk”, “we will never do X”.

## You answer questions in your language

The agent will ask things like:

- Could A happen without B?
- Is this something you expect, a maybe, or basically never?
- When it happens, is it another one of the same kind, or a different kind of thing?
- Make room now, remember it but don’t build it, or treat it as off the table?
- Is this the same program, or a separate product?

You do not have to know what an API protocol is. If the agent infers something technical, they must explain it as a bet in your words (“a new company is not always a new kind of connection”) and wait.

## You confirm

The recap in ordinary language: what it is, this version, what is off the table, what can change independently, what is later. That is the lock.

You do **not** confirm extra copies in the code, dead code, or that a scanner is clean. That is the agent’s job.

## You do not

- Edit `product/axes.yaml` or any other intent file (unless you want to; the agent still owns the schema).
- List every feature as an axis. Features are the brief. Axes are independent things that can change.
- Ask for a framework for something you said later or never.

## When you change your mind

Say it. The next turn the agent updates the recap and the files, then the code. You should not have to know whether that is “a new member” or “a new axis”; they will ask one question if it matters.
