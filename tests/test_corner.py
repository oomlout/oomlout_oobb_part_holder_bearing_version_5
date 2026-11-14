"""The corner uses a vertical frame seam and independent axial hub seams."""

import copy
import json
import hashlib

import pytest

import working_corner
import working_populate
from action_make_corner import EXAMPLES, ROOT


def config(bearing_size="6810"):
    return copy.deepcopy(next(o["oobb_details"] for o in working_populate.get_options()
                              if "corner" in o and o["bearing_size"] == bearing_size))


def test_corner_apex_and_mounting_contract():
    c = working_corner.layout(**config())
    assert c["distance"] == 60
    assert c["mounting_row"] == 45
    assert c["spacer"] > c["minimum_gear_gap"]
    assert c["distance"] - c["depth"] / 2 - c["spacer"] - c["gear_depth"] / 2 == pytest.approx(c["apex"])
    assert c["gear_mounts"] == [[-15, -15], [-15, 15], [15, -15], [15, 15]]


@pytest.mark.parametrize("update", [
    {"bearing_depth": 15}, {"bearing_inner_diameter": 80},
    {"bearing_outer_diameter": 90}, {"mounting_row": 30},
    {"mounting_row": 44}, {"gear_teeth": 40}, {"split_gap": -0.1},
])
def test_incompatible_dimensions_fail_early(update):
    k = config()
    k["corner"].update(update)
    with pytest.raises(ValueError):
        working_corner.layout(**k)


def test_bearing_dimensions_are_parameterized():
    k = config()
    k["bearing_size"] = "future_bearing"
    k["corner"].update(bearing_inner_diameter=52, bearing_outer_diameter=64, bearing_depth=6)
    c = working_corner.layout(**k)
    assert c["inner_radius"] == 26
    assert c["outer_radius"] == 32
    assert c["bearing_depth"] == 6
    assert c["bearing_size"] == "future_bearing"


@pytest.mark.parametrize("bearing_size", ["6810", "6704"])
def test_corner_connections_use_25_mm_socket_cap_primitive(bearing_size):
    c = working_corner.layout(**config(bearing_size))
    joins = working_corner.stationary(c)["components_objects"]
    assert len(joins) == 3
    for join in joins:
        assert join["shape"] == "oobb_screw_socket_cap"
        assert join["depth"] == 25
        assert join["nut_include"] and join["overhang"]
        assert join["clearance"] == ["top", "bottom"]


def test_6704_matches_three_wide_gear_and_regular_m3_grid():
    c = working_corner.layout(**config("6704"))
    assert c["gear_teeth"] * c["gear_module"] == 45
    assert c["depth"] == 9
    assert c["distance"] == 37.5
    assert c["spacer"] == pytest.approx(3.6437)
    assert c["mounting_row"] == 30
    assert c["height_mm"] == 45
    assert c["gear_mount_radius_name"] == "m3"
    assert c["gear_pad_radius"] == 3
    assert set(map(tuple, c["gear_mounts"])) == {(-7.5, 0), (7.5, 0), (0, -7.5), (0, 7.5)}
    assert c["hub_source"]["bearing_depth"] == 4
    import working_scad
    working_scad.define_bearing_dimensions(**c["hub_source"])
    grid = working_scad.get_mounting_layout(**c["hub_source"])
    assert set(map(tuple, c["gear_mounts"])) <= {
        (hole["x"], hole["y"]) for hole in grid["holes"] if hole["radius_name"] == "m3"
    }


@pytest.mark.parametrize("bearing_size,counts,near_column", [
    ("6810", {"m6": 14, "m3": 25}, -37.5),
    ("6704", {"m6": 7, "m3": 20}, -22.5),
])
def test_full_corner_mounting_grid(bearing_size, counts, near_column):
    c = working_corner.layout(**config(bearing_size))
    plan = c["frame_mounting"]
    assert plan["counts_per_arm"] == counts
    holes = {(h["u"], h["v"]): h["radius_name"] for h in plan["holes"]}
    assert holes[c["mounting_row"], 0] == "m6"
    assert holes[c["mounting_row"], 7.5] == "m3"
    assert holes[near_column, 0] == "m3"
    assert (0, 0) not in holes
    assert all(u != c["mounting_row"] - 7.5 for u, v in holes)
    for (u, v), name in holes.items():
        assert u % 7.5 == v % 7.5 == 0
        if name == "m6":
            assert u % 15 == v % 15 == 0


def test_only_9_mm_6704_corner_and_nuts_clear_bearing():
    options = [o for o in working_populate.get_options() if "corner" in o and o["bearing_size"] == "6704"]
    assert len(options) == 1 and options[0]["depth"] == 9
    c = working_corner.layout(**options[0]["oobb_details"])
    t = working_corner.regular_hub(json.dumps(c["hub_source"], sort_keys=True), c["hub_radius"])
    nuts = [p for p in t["components_objects"] if p["shape"] == "oobb_nut"]
    assert len(nuts) == 2
    for nut in nuts:
        assert nut["overhang"] and nut["depth"] == 2.4
        assert abs(nut["pos"][2]) - nut["depth"] == pytest.approx(c["bearing_depth"] / 2 + .1)
    holes = {(h["u"], h["v"]): h["radius_name"] for h in c["frame_mounting"]["holes"]}
    assert holes[-30, 0] == "m3"  # M6 would enter the closer perpendicular arm.


@pytest.mark.parametrize("bearing_size", ["6810", "6704"])
def test_saved_rendered_validation(bearing_size):
    # Recreate with python action_make_corner.py && python validate_corner.py.
    report = json.loads((ROOT / "examples" / f"corner_{bearing_size}" / "validation.json").read_text())
    assert report["print_components"] == 6
    assert report["print_volume_matches_assembly"]
    assert max(report["mounting_hole_gauge_intersection_mm3"]) < 1e-5
    assert report["mounting_holes_per_arm"]["m6"] > 0
    assert report["mounting_holes_per_arm"]["m3"] > 0
    assert max(report["regular_interior_difference_mm3"]) < 1e-5
    for name, digest in report["sha256"].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, f"Rebuild / revalidate {name}"
    assert all(c["watertight"] and c["components"] == 1 for c in report["components"].values())
    assert all(c["max_intersection_mm3"] < 1e-5 for c in report["motion_checks"])
    assert all(c["samples"] >= 16 for c in report["motion_checks"]
               if c["pair"] not in ("frame_halves", "hub_halves_and_gear"))
