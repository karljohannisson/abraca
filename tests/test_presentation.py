"""verifies: tui-presentation — read the authority, do not recopy a second theme."""

from chat.tui import presentation


def test_presentation_values_come_from_authority() -> None:
    assert presentation.WIDTH > 0
    assert presentation.SCROLL_STEP > 0
    assert presentation.COLOR_USER
    assert presentation.COLOR_ASSISTANT
