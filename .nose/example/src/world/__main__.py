import sys

from world.regions import REGIONS


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("usage: world REGION", file=sys.stderr)
        return 1
    region = argv[0]
    countries = REGIONS.get(region)
    if countries is None:
        print(f"unknown region: {region}", file=sys.stderr)
        return 1
    for country in countries:
        print(country)
    return 0
