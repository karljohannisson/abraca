"""Minimal YAML subset for product/*.yaml (stdlib only)."""

from __future__ import annotations


def load(text: str) -> object:
    lines = _preprocess(text.splitlines())
    value, _ = _parse_block(lines, 0, 0)
    return value


def load_path(path) -> object:
    return load(path.read_text(encoding="utf-8"))


def _preprocess(raw: list[str]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for line in raw:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        body = _strip_comment(line.lstrip(" "))
        if body:
            out.append((indent, body))
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


def _parse_block(lines: list[tuple[int, str]], i: int, min_indent: int):
    if i >= len(lines):
        return None, i
    indent, body = lines[i]
    if indent < min_indent:
        return None, i
    if body.startswith("- "):
        return _parse_list(lines, i, indent)
    return _parse_map(lines, i, indent)


def _parse_map(lines, i, indent) -> tuple[dict, int]:
    result: dict = {}
    while i < len(lines):
        ind, body = lines[i]
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
            if i + 1 < len(lines) and lines[i + 1][0] > indent:
                value, i = _parse_block(lines, i + 1, indent + 1)
            else:
                value, i = None, i + 1
                result[key] = value
                continue
        else:
            value = _parse_scalar(rest)
            i += 1
        result[key] = value
    return result, i


def _parse_list(lines, i, indent) -> tuple[list, int]:
    result: list = []
    while i < len(lines):
        ind, body = lines[i]
        if ind < indent:
            break
        if ind > indent:
            break
        if not body.startswith("- "):
            break
        item = body[2:].strip()
        if item == "":
            value, i = _parse_block(lines, i + 1, indent + 1)
            result.append(value)
            continue
        if ":" in item and not item.startswith(("'", '"')):
            key, _, rest = item.partition(":")
            rest = rest.strip()
            nested: dict = {}
            if rest in (">", ">-", "|", "|-"):
                nested[key.strip()], i = _parse_folded(lines, i + 1, indent)
            elif rest == "":
                if i + 1 < len(lines) and lines[i + 1][0] > indent:
                    nested[key.strip()], i = _parse_block(lines, i + 1, indent + 1)
                else:
                    nested[key.strip()] = None
                    i += 1
            else:
                nested[key.strip()] = _parse_scalar(rest)
                i += 1
                while i < len(lines) and lines[i][0] > indent and not lines[i][1].startswith("- "):
                    more, i = _parse_map(lines, i, lines[i][0])
                    nested.update(more)
            result.append(nested)
        else:
            result.append(_parse_scalar(item))
            i += 1
    return result, i


def _parse_folded(lines, i, parent_indent) -> tuple[str, int]:
    parts: list[str] = []
    while i < len(lines) and lines[i][0] > parent_indent:
        parts.append(lines[i][1])
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
