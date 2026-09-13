# Phase 2 — requirements (v1)

## Functional

- FR-1: Running the program prints the countries of a region, one per line.
- FR-2: Asking for an unknown region prints an error and exits nonzero.

## Technical

- TR-1: Data is hardcoded in the program; no network, no files read at runtime.

## Design

- DR-1: Plain command line, no flags beyond the region name.
  ```
  $ world Europe
  Germany
  France
  $ world Atlantis
  unknown region: Atlantis   (exit 1)
  ```

## Other

- (none)

## Parked

- API data source — Phase 1 parked idea, complexity declined.

## Hints for Phase 3

- “More regions later” — the set of regions will likely grow.
