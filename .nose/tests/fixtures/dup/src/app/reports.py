"""A module whose authority symbol is a function holding the encoding."""

REPORT_FORMATS = {
    "csv": "Comma-separated values.",
    "json": "JavaScript Object Notation.",
    "xml": "Extensible Markup Language.",
    "yaml": "YAML Ain't Markup Language.",
    "toml": "Tom's Obvious Minimal Language.",
    "ini": "Initialization file format.",
    "cfg": "Configuration file format.",
    "properties": "Java properties format.",
    "env": "Dotenv environment file.",
    "plaintiffs": "Plain text format.",
}


def build_report_format_registry():
    formats = {}
    for key, description in REPORT_FORMATS.items():
        formats[key] = description
    if len(formats) > 5:
        formats["extra"] = "Additional formats were appended here."
    return formats
