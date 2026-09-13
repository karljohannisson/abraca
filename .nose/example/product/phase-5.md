# Handover

## Start

From `.nose/example/`:

```
PYTHONPATH=src python3 -m world Europe
PYTHONPATH=src python3 -m world Atlantis   # error, exit 1
```

## What it does

v1 answers which countries are in a region (FR-1). An unknown region is an error,
not a guess (FR-2). Data is hardcoded — the demo is the question, not the dataset
(TR-1). Plain command line (DR-1).

## Parked

- Live data from an API (complexity declined).

## Designed to change later

- The list of regions may grow (axis `regions`): add a key to
  `src/world/regions.py` and nothing else changes.
- Greeting output may be added later — remembered, not built (`greetings`, dormant).

## Maintenance score

W is well under 1 — everything sits behind one named authority, nothing to hunt.

## Decisions that affect you

- D001: the region table lives in one module; do not recopy it elsewhere.
- D002: unknown regions exit 1 with a stderr message.
