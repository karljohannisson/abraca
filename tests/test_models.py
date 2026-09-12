"""verifies: model-discovery — model id is an open string."""

from chat.api.models import ModelRef


def test_model_ref_is_an_open_string() -> None:
    assert ModelRef(id="any-string-the-user-typed").id == "any-string-the-user-typed"
