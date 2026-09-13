"""Minimal YAML subset for product/*.yaml (stdlib only). Block maps and lists only."""

from __future__ import annotations

from pathlib import Path

_BLOCK_FORM = (
    "flow collections are not allowed; use a block list or block map:\n"
    "code_roots:\n"
    "  - src\n"
    "verifies:\n"
    "authority:\n"
    "  symbol: pkg.mod.fn\n"
    "  path: src/pkg/mod.py"
)


class YamlError(ValueError):
    pass


def load(text: str, *, path: str = "<string>") -> object:
    lines = _preprocess(text.splitlines())
    value, _ = _parse_block(lines, 0, 0, path)
    return value


def load_path(path: Path) -> object:
    return load(path.read_text(encoding="utf-8"), path=str(path))


def _preprocess(raw: list[str]) -> list[tuple[int, int, str]]:
    out: list[tuple[int, int, str]] = []
    for lineno, line in enumerate(raw, start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        body = _strip_comment(line.lstrip(" "))
        if body:
            out.append((lineno, indent, body))
    return out


def _strip_comment(s: str) -> str:
    in_single = False
    in_double = False
    for i, ch in enumerate(s):
        if ch == "'" and not in_double:
            in_single = not in_single
        elif ch == '"' and not in_single:
            in_double = not in_double
        elif ch == "#" and not in_single and not in_double:
            return s[:i].rstrip()
    return s.rstrip()


def _reject_flow(raw: str, path: str, lineno: int) -> None:
    if raw.startswith("[") or raw.startswith("{"):
        raise YamlError(f"{path}:{lineno}: {_BLOCK_FORM}")


def _parse_block(lines: list[tuple[int, int, str]], i: int, min_indent: int, path: str):
    if i >= len(lines):
        return None, i
    _, indent, body = lines[i]
    if indent < min_indent:
        return None, i
    if body.startswith("- "):
        return _parse_list(lines, i, indent, path)
    return _parse_map(lines, i, indent, path)


def _parse_map(lines, i, indent, path) -> tuple[dict, int]:
    result: dict = {}
    while i < len(lines):
        lineno, ind, body = lines[i]
        if ind < indent or body.startswith("- "):
            break
        if ind > indent:
            break
        key, _, rest = body.partition(":")
        key = key.strip()
        rest = rest.strip()
        if rest in (">", ">-", "|", "|-"):
            value, i = _parse_folded(lines, i + 1, indent)
        elif rest == "":
            if i + 1 < len(lines) and lines[i + 1][1] > indent:
                value, i = _parse_block(lines, i + 1, indent + 1, path)
            else:
                value, i = None, i + 1
                result[key] = value
                continue
        else:
            _reject_flow(rest, path, lineno)
            value = _parse_scalar(rest)
            i += 1
        result[key] = value
    return result, i


def _parse_list(lines, i, indent, path) -> tuple[list, int]:
    result: list = []
    while i < len(lines):
        lineno, ind, body = lines[i]
        if ind < indent:
            break
        if ind > indent:
            break
        if not body.startswith("- "):
            break
        item = body[2:].strip()
        if item == "":
            value, i = _parse_block(lines, i + 1, indent + 1, path)
            result.append(value)
            continue
        if ":" in item and not item.startswith(("'", '"')):
            key, _, rest = item.partition(":")
            rest = rest.strip()
            nested: dict = {}
            if rest in (">", ">-", "|", "|-"):
                nested[key.strip()], i = _parse_folded(lines, i + 1, indent)
            elif rest == "":
                if i + 1 < len(lines) and lines[i + 1][1] > indent:
                    nested[key.strip()], i = _parse_block(lines, i + 1, indent + 1, path)
                else:
                    nested[key.strip()] = None
                    i += 1
            else:
                _reject_flow(rest, path, lineno)
                nested[key.strip()] = _parse_scalar(rest)
                i += 1
                while i < len(lines) and lines[i][1] > indent and not lines[i][2].startswith("- "):
                    more, i = _parse_map(lines, i, lines[i][1], path)
                    nested.update(more)
            result.append(nested)
        else:
            _reject_flow(item, path, lineno)
            result.append(_parse_scalar(item))
            i += 1
    return result, i


def _parse_folded(lines, i, parent_indent) -> tuple[str, int]:
    parts: list[str] = []
    while i < len(lines) and lines[i][1] > parent_indent:
        parts.append(lines[i][2])
        i += 1
    return " ".join(parts), i


def _parse_scalar(s: str) -> object:
    if s in ("null", "Null", "~"):
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        return s
