"""Existing working.py / OOMP entry point; edit the catalogue in working_populate."""

from oomp_populate_helper import build_oomp_id
import working_populate


def main(**kwargs):
    return working_populate.main(**kwargs)


if __name__ == "__main__":
    main()
