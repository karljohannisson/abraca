# Decision log

Read by every Phase 4 task agent. Append only.

## D001
task: T001
decision: Hardcode the region table in one module.
why: TR-1 says no runtime data source; one authority keeps the growth axis cheap.
impact: FR-1, axis regions

## D002
task: T002
decision: Unknown region exits with status 1 after printing the message to stderr.
why: FR-2 needs a distinguishable failure without flags or config.
impact: FR-2
