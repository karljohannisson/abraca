from app.items import ITEMS


def compose() -> list[str]:
    mode = "run"
    path = "out"
    tool = "cli"
    names = []
    for item in ITEMS:
        names.append(item.name)
    return names
