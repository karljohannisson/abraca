"""Plan lint: a small checker for the phase-4 plan (stdlib only).

Validates `product/phase-4-plan.md` against `product/axes.yaml`:

- Every `status: locked` axis id has exactly one task with `encodes: [that id]`.
- No task encodes two ids.
- No task encodes a dormant axis (frozen reasons are never rows, so any
  unknown id is also a failure).

Plan convention (minimal): each task is a `## Tnnn — …` heading that contains
one fenced YAML block with a `task` info string:

    ## T001 — example authority

    ```yaml task
    encodes: [example]
    uses: []
    ```

Anything before the first task heading, and any fenced block that is not
`yaml task`, is ignored. Run: `PYTHONPATH=.nose python3 -m planlint`.
Exit 0 on pass, 1 on any failure.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from maintainability.yaml_lite import load as yaml_load

DEFAULT_PLAN = Path("product/phase-4-plan.md")
DEFAULT_AXES = Path("product/axes.yaml")

_TASK_HEADING = re.compile(r"^##\s+(T\d+)\b")
_FENCE = re.compile(r"^```(.*)$")
_LIST = re.compile(r"\[[^\]]*\]")


def lint(plan_text: str, axes) -> list[str]:
    """Return a list of failure messages (empty = pass)."""
    locked = [r["id"] for r in axes if r.get("status") == "locked"]
    dormant = {r["id"] for r in axes if r.get("status") == "dormant"}
    known = {r["id"] for r in axes} | dormant

    encodes: dict[str, list[str]] = {}
    for tid, block in _task_blocks(plan_text):
        data = yaml_load(block)
        ids = _ids(data.get("encodes") if isinstance(data, dict) else None)
        encodes[tid] = ids

    errors: list[str] = []
    for tid, ids in encodes.items():
        if len(ids) > 1:
            errors.append(f"{tid}: encodes {len(ids)} axes ({', '.join(ids)}); exactly one allowed")
        for aid in ids:
            if aid not in known:
                errors.append(f"{tid}: encodes unknown axis id '{aid}'")
            elif aid in dormant:
                errors.append(f"{tid}: encodes dormant axis '{aid}'")

    counts: dict[str, int] = {}
    for ids in encodes.values():
        for aid in ids:
            counts[aid] = counts.get(aid, 0) + 1
    for aid in locked:
        n = counts.get(aid, 0)
        if n != 1:
            errors.append(f"locked axis '{aid}' has {n} encodes tasks; exactly one required")
    return errors


def _task_blocks(text: str):
    """Yield (task_id, yaml_block) for each `## Tnnn` heading with a ```yaml task fence."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = _TASK_HEADING.match(lines[i])
        if not m:
            i += 1
            continue
        tid = m.group(1)
        i += 1
        block: list[str] | None = None
        while i < len(lines):
            fence = _FENCE.match(lines[i].strip())
            if fence and (fence.group(1) or "").split()[0:1] == ["yaml"] and "task" in fence.group(1):
                block = []
                i += 1
                while i < len(lines) and lines[i].strip() != "```":
                    block.append(lines[i])
                    i += 1
                break
            if _TASK_HEADING.match(lines[i]) or lines[i].startswith("# "):
                break
            i += 1
        if block is not None:
            yield tid, "\n".join(block)


def _ids(value) -> list[str]:
    """Accept a parsed list or an inline `[a, b]` string; return ids."""
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    text = str(value).strip()
    if not text:
        return []
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]
    return [p.strip().strip("'\"") for p in text.split(",") if p.strip()]


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    plan = DEFAULT_PLAN
    axes_path = DEFAULT_AXES
    i = 0
    while i < len(args):
        if args[i] == "--axes":
            axes_path = Path(args[i + 1])
            i += 2
        elif args[i].startswith("--"):
            i += 1
        else:
            plan = Path(args[i])
            i += 1

    if not plan.is_file():
        print(f"planlint: plan not found: {plan}", file=sys.stderr)
        return 1
    if not axes_path.is_file():
        print(f"planlint: axes not found: {axes_path}", file=sys.stderr)
        return 1

    axes = yaml_load(axes_path.read_text(encoding="utf-8"))
    if not isinstance(axes, list):
        print(f"planlint: {axes_path} must be a YAML list of axis rows", file=sys.stderr)
        return 1

    errors = lint(plan.read_text(encoding="utf-8"), axes)
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1
    print(f"planlint: OK ({len(axes)} axes, {plan})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
