"""Generate text-only navigation and canonical part READMEs."""
from pathlib import Path
from catalogue import navigation
def generate_navigation(folder="parts", sort=None):
    return navigation(Path(folder).resolve().parent)
if __name__ == "__main__":
    generate_navigation(Path(__file__).resolve().parent / "parts")
