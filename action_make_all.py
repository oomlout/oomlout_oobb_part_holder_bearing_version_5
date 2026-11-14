"""Rebuild the complete active catalogue, previews and documentation."""
from catalogue import build, cli
def main(**kwargs):
    return build(part_filter=kwargs.get("filter", ""), workers=kwargs.get("workers", 2),
                 native=kwargs.get("run_solidcraft", False), legacy_actions=kwargs.get("run_action", False),
                 populate=kwargs.get("run_oomp_populate", False))
if __name__ == "__main__":
    cli()
