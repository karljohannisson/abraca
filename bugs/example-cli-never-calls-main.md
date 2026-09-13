# Example `python3 -m world` never calls `main`

**Status:** open.

**Where.** `.nose/example/src/world/__main__.py`.

**What is wrong.** `main()` is defined and the tests import it. The module never calls it. Handover and `.nose/example/README.md` tell a human to run `PYTHONPATH=src python3 -m world Europe` (print Germany/France) and `… Atlantis` (exit 1). Both commands print nothing and exit 0.

**Why it matters.** A cold agent copies the recorded loop. The product the human is supposed to try is a no-op.

**Fix.** End `__main__.py` with `if __name__ == "__main__": raise SystemExit(main())`. Prove it with the handover commands, not only `unittest` imports of `main`.
