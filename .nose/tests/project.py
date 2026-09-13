"""Build a tiny product tree for metric tests."""

from __future__ import annotations

from pathlib import Path


def write_project(root: Path, *, axes: str, entry: str, files: dict[str, str]) -> Path:
    (root / "product").mkdir(parents=True)
    (root / "product" / "axes.yaml").write_text(axes, encoding="utf-8")
    (root / "product" / "entry-points.yaml").write_text(entry, encoding="utf-8")
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root
