"""verifies: multimodal — read content parts from the authority."""

from chat.content import ContentPart, TextPart


def test_text_part_is_the_first_content_variant() -> None:
    part: ContentPart = TextPart(text="hi")
    match part:
        case TextPart(text=text):
            assert text == "hi"
