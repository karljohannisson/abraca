"""Tools may be added; the message model must represent tool calls and results."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolDef:
    name: str
    description: str


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: str


@dataclass(frozen=True)
class ToolResult:
    id: str
    output: str


ToolEvent = ToolCall | ToolResult
