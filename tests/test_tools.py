"""verifies: tool-calling — exhaustive on tool events."""

from chat.tools import ToolCall, ToolEvent, ToolResult


def test_every_tool_event_is_handled() -> None:
    events: tuple[ToolEvent, ...] = (
        ToolCall(id="1", name="x", arguments="{}"),
        ToolResult(id="1", output="ok"),
    )
    kinds: list[str] = []
    for event in events:
        match event:
            case ToolCall():
                kinds.append("call")
            case ToolResult():
                kinds.append("result")
    assert kinds == ["call", "result"]
