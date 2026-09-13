from app.reports import build_report_format_registry


def test_formats() -> None:
    assert build_report_format_registry()
