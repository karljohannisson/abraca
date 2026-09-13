# Orchestrate — you drive; the human talks

You are the coordinator. The human never has to know which phase this is.

## Every turn

1. Read `product/status.yaml`. If it does not exist, you are in **Phase 1**, `not_started`. Create `product/` if needed.
2. Load **only** `status.next_instructions` and `status.artifacts` (Phase 1 files if status is missing). Do not mine other `product/` files for “maybe useful” context. Leftover files from another product (no matching status) are **not** locked intent — start Phase 1 from what the human said.
3. Do the current phase. Write its artifact as you go.
4. When that phase’s **done-criteria** are true, lock the artifact, update `status.yaml` to the next phase, and **reset** (below). Do not ask “shall we go to the next phase?”
5. If done-criteria need a human answer, set `status: waiting_human`, ask in their language, stay in this phase.

`status: complete` on a phase is transient: immediately bump `phase` to the next and set `in_progress`.

## `product/status.yaml`

```yaml
version: 1
phase: 1                    # 1 2 3 4 5 or maintenance
phase_name: brainstorm      # brainstorm | requirements | axes | implement | handover | maintenance
status: in_progress         # not_started | in_progress | waiting_human
waiting_on: null            # when waiting_human: slice_accept (mid-Phase-4 runnable slice)
next_instructions: .nose/docs/workflow/phase-1-brainstorm.md
artifacts:
  - product/status.yaml
  - product/phase-1.md      # only files the current agent may read
human:
  technical_depth: low      # low | mixed | high — from their language
  domains: []               # domains where they already used the terms
w_baseline: null            # set after first Phase 4 metric run; headline W
```

When advancing, rewrite `next_instructions` and `artifacts` to the **incoming** phase’s list (see each phase file, “Cold agent loads”).

## Context reset

Between **phases**, and between **Phase 4 tasks**, the next agent gets a new context. Conversation memory does not travel. Files do.

**If you can start an isolated subagent / new session:** do that. Prompt:

```
You are a coding agent in the nose workflow.
Read in order: AGENTS.md, .nose/docs/README.md, .nose/docs/workflow/orchestrate.md,
product/status.yaml, then the file in status.next_instructions, then only status.artifacts.
Do not use prior chat. Do not read other product/ files.
Then do that phase (or that one Phase 4 task).
```

**If you cannot reset:** say one line that Phase N is locked on disk, load only the new instruction + artifacts, and do not use earlier conversation except as already written into those files. Then continue.

Do not implement the whole of Phase 4 in one context. One task per context.

## Who the human talks to

| Phase | Conversation |
|---|---|
| 1–3, 5 | You and the human. You write files. |
| 4 plan | You, no human (unless the plan lint finds a missing axis → back to Phase 3). |
| 4 each task | Isolated agent. No human. Product questions (`confirmed_live`) go to the decision log; if you truly cannot decide, stop the pipeline and ask the human, then resume the same task. |
| 5 complaints | Route and rewind (below). |

## Advancing (do not skip)

| From | To when | Incoming artifacts |
|---|---|---|
| — | 1 | `status.yaml` (create it) |
| 1 | 2 | status, `phase-1.md` |
| 2 | 3 | status, `phase-1.md`, `phase-2.md` |
| 3 | 4 | status, `phase-1.md`, `phase-2.md`, `axes.yaml` |
| 4 | 5 | those + `phase-4-plan.md`, `decisions.md`, `entry-points.yaml`, code |
| 5 accept | `maintenance` | all of the above + `phase-5.md` |
| 5 complaint (UX / “not what I meant”) | **2** | keep artifacts; Phase 2 amends `phase-2.md` |
| 5 complaint (new kind of change / vendor / widget) | **3** | keep artifacts; Phase 3 amends `axes.yaml` then 4 |

Never jump 1 → 4. Never write `src/` in 1–3.

## Phase 4 coordination

1. Cold Phase 4 agent runs [phase-4-plan.md](phase-4-plan.md): write `product/phase-4-plan.md`, **lint the plan**, create empty `product/decisions.md` if needed. Do not code.
2. Copy the **next undone task only** into `product/current-task.md` (never hand the whole plan to a task agent). Set `next_instructions` to [phase-4-task.md](phase-4-task.md). `artifacts`: status, current-task, axes, decisions, entry-points if it exists.
3. Run **one** task agent. It commits, appends decisions, records \(W\). If two task agents in one wave both edit `product/*.yaml`, diff those files before advancing.
4. If the task failed or \(W\) rose without a logged reason: do not start the next task; fix or replan.
5. **Slice checkpoint.** After the first few authority tasks are done (before any composition/UI task): stop and ship a thin runnable vertical — one screen, one command the human can run. Set `status: waiting_human` with `waiting_on: slice_accept`, tell the human how to run it in their words, and run no further tasks until they try it and accept. If they reject, rewind (plan or Phase 2/3) while it is still cheap.
6. Repeat 2–4 until the plan is done, then Phase 5.

## Language

Match the human ([human.md](human.md)). Infer and confirm. Explain a technical term the first time if they have not used that depth. Five whys stay **internal** — they get one clear question at a time, in their words.

## What you never ask the human

- Which phase, which file, which module, yaml, \(k\), extra sites, atom names, whether to run the metric.
- Permission to advance a phase that already meets its done-criteria.
