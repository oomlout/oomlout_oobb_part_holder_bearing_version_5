"""Render the actual OOBB drawings; check the assembled/print geometry contract."""

import copy
import shutil
import subprocess
from pathlib import Path

import numpy as np
import oobb
import pytest
import trimesh
import yaml

import working_populate
import working_scad


ALL_OPTIONS = working_populate.get_options()
# These tests exercise the axial split contract of the flat-holder family.
# The corner's vertical split and whole hub discs have their own mesh checks.
OPTIONS = [option for option in ALL_OPTIONS if "corner" not in option]
OPENSCAD = shutil.which("openscad.com") or shutil.which("openscad")


def material_at(mesh, x, y, z):
    section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
    crossings = 0
    for contour in section.discrete:
        for a, b in zip(contour[:-1], contour[1:]):
            if (a[1] > y) != (b[1] > y):
                edge_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                crossings += edge_x > x
    return bool(crossings % 2)


def draw(**kwargs):
    thing = oobb.get_default_thing(type="test_bearing_holder")
    function = getattr(working_scad, "get_" + kwargs["oobb_name"])
    function(thing, **kwargs)
    return thing


def render(folder, **kwargs):
    assert OPENSCAD, "OpenSCAD is required for the geometry checks"
    thing = draw(**kwargs)
    path = folder / "working.scad"
    oobb.opsc_make_object(str(path), thing["components"], mode=kwargs["mode"], save_type="none")
    result = subprocess.run(
        [OPENSCAD, "--backend=Manifold", "-o", str(path.with_suffix(".stl")), str(path)],
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "ERROR:" not in result.stderr, result.stderr
    assert "WARNING:" not in result.stderr, result.stderr
    mesh = trimesh.load_mesh(path.with_suffix(".stl"))
    assert mesh.is_watertight
    assert mesh.volume > 0
    return mesh


def test_catalogue_and_taxonomy():
    assert len(ALL_OPTIONS) == 44
    assert len({option["id"] for option in ALL_OPTIONS}) == 44
    assert len({option["legacy_id"] for option in OPTIONS if "legacy_id" in option}) == 14
    extras_6704 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6704"}
    extras_6705 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6705"}
    assert extras_6705 == extras_6704 - {"double"}
    assert len(extras_6705) == 8
    extras_6709 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6709"}
    assert extras_6709 == extras_6705 | {
        "inside_embedded_m6_nuts",
        "inside_mechanical_coupler_flange_name_5_mm_bore",
    }
    assert all(p["width"] == p["height"] == 5 for p in OPTIONS if p["bearing_size"] == "6709")
    angled = [option for option in OPTIONS if option["taxonomy_3"] == "holder_90_degree"]
    assert len(angled) == 2
    assert {option["taxonomy_9"] for option in angled} == {"", "basic"}
    for option in ALL_OPTIONS:
        assert "jack" not in option["id"]
        assert option["taxonomy_3"] in ["holder", "holder_90_degree"]
        assert option["id"].startswith("oobb_part_holder_")
        drawing_name = "bearing_" + option["taxonomy_3"]
        if "corner" in option:
            drawing_name = "bearing_holder_corner"
        assert option["oobb_details"]["oobb_name"] == drawing_name
        assert callable(getattr(working_scad, "get_" + drawing_name))
        assert option["taxonomy_5"] == option["bearing_size"] + "_bearing_size"
        assert option["taxonomy_8"] == f"{option['depth']}_depth"


@pytest.mark.parametrize("option", OPTIONS, ids=[option["id"] for option in OPTIONS])
def test_print_halves_preserve_assembly(tmp_path, option):
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    assembled = render(tmp_path / "assembled", **kwargs)
    kwargs["prepare_print"] = True
    printed = render(tmp_path / "printed", **kwargs)

    half_depth = option["depth"] / 2
    assert assembled.bounds[0, 2] == pytest.approx(-half_depth)
    assert assembled.bounds[1, 2] == pytest.approx(half_depth)
    assert printed.bounds[0, 2] == pytest.approx(0, abs=1e-6)
    assert printed.volume == pytest.approx(assembled.volume, rel=1e-6)

    if not kwargs.get("split", True):
        assert printed.bounds[1, 2] == pytest.approx(option["depth"])
        return

    split_z = kwargs.get("split_z", 0)
    assert printed.bounds[1, 2] == pytest.approx(half_depth + abs(split_z))
    span = option["width"] * 15
    if kwargs.get("body") == "cylinder":
        span = 24
        if option["bearing_size"] == "6705":
            span = 29
        if option["bearing_size"] == "6709":
            span = 49
    distance = span + kwargs["print_gap"]
    mid_gap = (span / 2 + distance - span / 2) / 2
    centers = printed.triangles_center[:, 0]
    left = printed.submesh([centers < mid_gap], append=True)
    right = printed.submesh([centers > mid_gap], append=True)
    assert len(left.faces) and len(right.faces)
    assert right.bounds[0, 0] - left.bounds[1, 0] >= kwargs["print_gap"] - 0.001

    # The complete grid intentionally changes the old v3 volumes.

    # Reassemble the two independently clipped halves and check mass properties.
    left.apply_translation([0, 0, -half_depth])
    right.apply_translation([-distance, 0, -half_depth])
    right.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    joined = trimesh.util.concatenate([left, right])
    np.testing.assert_allclose(joined.bounds, assembled.bounds, atol=1e-6)
    np.testing.assert_allclose(joined.center_mass, assembled.center_mass, atol=1e-6)
    np.testing.assert_allclose(joined.moment_inertia, assembled.moment_inertia, atol=0.01, rtol=1e-6)


@pytest.mark.parametrize("mode", ["true", "laser"])
def test_print_switch_does_not_split_other_modes(tmp_path, mode):
    kwargs = copy.deepcopy(OPTIONS[0]["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = True
    mesh = render(tmp_path / mode, **kwargs)
    assert mesh.bounds[0, 0] == pytest.approx(-22.5)
    assert mesh.bounds[1, 0] == pytest.approx(22.5)
    assert mesh.bounds[0, 2] == pytest.approx(-6)
    assert mesh.bounds[1, 2] == pytest.approx(6)


def test_runtime_print_override():
    parts = working_scad.get_parts({"prepare_print": False, "modes": ["3dpr"]}, "project")
    assert len(parts) == len(ALL_OPTIONS)
    assert all(part["kwargs"]["prepare_print"] is False for part in parts)


def test_named_bearing_seats_and_6810_through_holes():
    kwargs = copy.deepcopy(next(p for p in OPTIONS if p["bearing_size"] == "6810")["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    thing = draw(**kwargs)
    holes = [p for p in thing["components_objects"] if p.get("shape") == "oobb_hole"
             and p.get("radius_name") in ["m3", "m6"] and p.get("depth", 0) > 12]
    assert holes
    assert all(p["pos"][2] < -6 for p in holes)
    radii = [p.get("radius_name") for p in thing["components_objects"]]
    assert "holder_bearing_6810_od" in radii
    assert "holder_bearing_6810_id" in radii
    assert oobb.gv("holder_bearing_6810_od", "3dpr") == 32.7
    assert oobb.gv("holder_bearing_6810_id", "3dpr") == 25


def test_position_and_rotation_apply_to_the_whole_part(tmp_path):
    kwargs = copy.deepcopy(OPTIONS[0]["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    mesh = render(tmp_path / "origin", **kwargs)
    kwargs["pos"] = [13, -7, 20]
    kwargs["rot"] = [0, 0, 90]
    moved = render(tmp_path / "moved", **kwargs)
    mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 0, 1]))
    mesh.apply_translation(kwargs["pos"])
    np.testing.assert_allclose(moved.bounds, mesh.bounds, atol=1e-6)




def test_coupler_catalogue_matches_oomp_reference():
    reference = Path(__file__).resolve().parents[1] / "source_file/coupler_flange_5_mm_reference.yaml"
    reference = yaml.safe_load(reference.read_text())
    option = next(p for p in OPTIONS if p.get("inside") == "flange_coupler")
    assert option["coupler_oomp_id"] == reference["oomp_id"]
    dims = reference["dimensions_mm"]
    assert option["coupler_bore"] == dims["bore"] == 5
    assert option["coupler_flange_diameter"] == dims["diameter_baseplate"] == 22
    assert option["coupler_bolt_circle_diameter"] == dims["distance_diagonal_screw_hole"] == 16
    assert option["coupler_mount_count"] == dims["count_screw_hole"] == 4
    assert option["coupler_mount_radius_name"] == "m3"
    assert option["bearing_size"] == "6709"
    assert option["width"] == option["height"] == 5


def test_608_and_6810_catalogue_scope():
    small = [p for p in OPTIONS if p["bearing_size"] == "608"]
    assert len(small) == 1
    assert small[0]["extra"] == ""
    assert (small[0]["width"], small[0]["height"], small[0]["depth"]) == (3, 3, 12)
    large = [p for p in OPTIONS if p["bearing_size"] == "6810"]
    assert {p["extra"] for p in large} == {"", "inside_embedded_m3_nuts", "inside_embedded_m6_nuts", "inside_hole_30_mm"}
    assert all((p["width"], p["height"]) == (7, 5) for p in large)
    assert {p["depth"] for p in large if p["extra"] == ""} == {12, 15}
    assert all(p["depth"] == 12 for p in large if p["extra"])


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_608_bearing_seat_and_retaining_lips(tmp_path, mode):
    option = next(p for p in OPTIONS if p["bearing_size"] == "608")
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)
    assert len(mesh.split()) == 2
    assert oobb.gv("holder_bearing_608_id", mode) == 4
    assert oobb.gv("holder_bearing_608_od", mode) == (11.2 if mode == "3dpr" else 11)
    assert oobb.gv("holder_bearing_608_depth", mode) == 7
    assert not material_at(mesh, 2.8, 0, 0)  # Standard central M6 through-hole.
    assert material_at(mesh, 3.6, 0, 0)      # Inner-race seat remains intact.
    for z in [-3.4, 0, 3.4]:
        assert not material_at(mesh, 10, 0, z)
    for z in [-4, 4]:
        assert material_at(mesh, 10, 0, z)  # Both outer retaining lips.


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
@pytest.mark.parametrize("bearing_size", ["6709", "6810"])
def test_m6_nuts_fit_the_large_hub_and_remain_captive(tmp_path, mode, bearing_size):
    option = next(p for p in OPTIONS if p.get("inside") == "embedded_m6_nuts" and p["bearing_size"] == bearing_size)
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)
    assert len(mesh.split()) == 2
    assert kwargs["embedded_nut_positions"] == [[-15, 0], [15, 0], [0, -15], [0, 15]]

    radius = oobb.gv("nut_radius_m6", mode)
    nut_depth = oobb.gv("nut_depth_m6", mode)
    hub_radius = oobb.gv(f"holder_bearing_{bearing_size}_id", mode)
    for x, y in kwargs["embedded_nut_positions"]:
        # A sample 4 mm radially from the bolt is inside the M6 nut pocket,
        # outside the bolt bore, and outside an accidentally retained M3 hex.
        direction = np.array([x, y]) / 15
        pocket_x, pocket_y = np.array([x, y]) + direction * 4
        for z in [-nut_depth / 2 + 0.1, 0, nut_depth / 2 - 0.1]:
            assert not material_at(mesh, pocket_x, pocket_y, z)
        for z in [-nut_depth / 2 - 0.1, nut_depth / 2 + 0.1]:
            assert material_at(mesh, pocket_x, pocket_y, z)
        for z in [-5.5, 0, 5.5]:
            assert not material_at(mesh, x + 2.8, y, z)  # M6 bolt, not M3.
        vertices = np.column_stack([
            np.cos(np.deg2rad(np.arange(6) * 60 + 30 + np.rad2deg(np.arctan2(y, x)))),
            np.sin(np.deg2rad(np.arange(6) * 60 + 30 + np.rad2deg(np.arctan2(y, x)))),
        ]) * radius + [x, y]
        assert hub_radius * np.cos(np.pi / 50) - np.linalg.norm(vertices, axis=1).max() > 2
        assert np.hypot(x, y) - radius * np.cos(np.pi / 6) - oobb.gv("hole_radius_m6", mode) > 6
        assert material_at(mesh, direction[0] * 20.4, direction[1] * 20.4, 0)

    assert not material_at(mesh, 2.8, 0, 0)  # Original M6 centre bore retained.
    assert material_at(mesh, 4, 0, 0)
    assert not material_at(mesh, 7.5, 0, 0)  # New M3 half-grid hole.
    for sign in [-1, 1]:
        assert not material_at(mesh, -sign * (13 if bearing_size == "6709" else 7.5), sign * (13 if bearing_size == "6709" else 7.5), 0)


def test_m6_is_only_offered_where_there_is_room():
    m6_options = [p for p in OPTIONS if p.get("embedded_nut_radius_name") == "m6"]
    assert {p["bearing_size"] for p in m6_options} == {"6709", "6810"}
    # Even the minimum hex width cannot fit radially between the retained
    # centre bore and either smaller bearing seat, before adding any wall.
    for mode in ["3dpr", "true", "laser"]:
        minimum_hex_width = 2 * oobb.gv("nut_radius_m6", mode) * np.cos(np.pi / 6)
        for bearing_size in ["6704", "6705"]:
            space = oobb.gv(f"bearing_{bearing_size}_id", mode) - oobb.gv("hole_radius_m6", mode)
            assert minimum_hex_width > space


@pytest.mark.parametrize("bearing_size,extra", [
    ("6709", ""),
    ("6709", "inside_embedded_m3_nuts"),
    ("6709", "inside_embedded_m6_nuts"),
    ("6810", "inside_embedded_m3_nuts"),
    ("6810", "inside_embedded_m6_nuts"),
])
def test_cardinal_grid_holes_and_no_centre_nut(tmp_path, bearing_size, extra):
    option = next(p for p in OPTIONS if p["bearing_size"] == bearing_size and p["extra"] == extra)
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)
    positions = [(-15, 0), (15, 0), (0, -15), (0, 15)]
    for x, y in positions:
        assert not material_at(mesh, x, y, -5)
        assert not material_at(mesh, x, y, 5)
    # Centre remains an M6 through-hole, without a hex extending from it.
    assert not material_at(mesh, 3, 0, 0)
    for angle in np.deg2rad(np.arange(0, 360, 30)):
        assert material_at(mesh, 3.3 * np.cos(angle), 3.3 * np.sin(angle), 0)
    if extra:
        expected = set(positions)
        if bearing_size == "6810" and extra == "inside_embedded_m3_nuts":
            expected |= {(-15, -15), (-15, 15), (15, -15), (15, 15)}
        assert {tuple(p) for p in kwargs["embedded_nut_positions"]} == expected




@pytest.mark.parametrize("option", [p for p in OPTIONS if p["bearing_size"] in ["6704", "6705", "6804"]], ids=lambda p: p["id"])
def test_small_family_inner_fasteners_are_diagonal_in_every_mode(monkeypatch, option):
    calls = []
    monkeypatch.setattr(working_scad, "add_joining_screw", lambda thing, **kwargs: calls.append(kwargs))
    for mode in ["3dpr", "true", "laser"]:
        calls.clear()
        kwargs = copy.deepcopy(option["oobb_details"])
        kwargs["mode"] = mode
        kwargs["prepare_print"] = False
        draw(**kwargs)
        inner = [p for p in calls if p.get("inner_joining")]
        if kwargs.get("horn_adapter") == "screws" or kwargs.get("split") is False:
            assert not inner
            continue
        expected = 4 if mode == "3dpr" and kwargs["shaft"] in ["motor_gearmotor_01", "motor_servo_micro_01"] else 2
        centers = working_scad.get_bearing_centers(**kwargs)
        assert len(inner) == expected * len(centers)
        for screw in inner:
            x, y = min(centers, key=lambda p: np.hypot(screw["screw_x"] - p[0], screw["screw_y"] - p[1]))
            assert abs(screw["screw_x"] - x) == pytest.approx(7.5 / np.sqrt(2))
            assert abs(screw["screw_y"] - y) == pytest.approx(7.5 / np.sqrt(2))
        assert all(np.hypot(p["screw_x"], p["screw_y"]) > 15 for p in calls if not p.get("inner_joining"))


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_coupler_holes_nut_retention_and_bearing_seat(tmp_path, mode):
    option = next(p for p in OPTIONS if p.get("inside") == "flange_coupler")
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)
    assert len(mesh.split()) == 2  # Separate rotating hub and stationary frame.
    np.testing.assert_allclose(mesh.bounds[:, 0], [-37.5, 37.5])
    assert oobb.gv("holder_bearing_6709_id", mode) == 22.5
    assert oobb.gv("holder_bearing_6709_od", mode) == (27.7 if mode == "3dpr" else 27.5)
    assert oobb.gv("holder_bearing_6709_depth", mode) == 6

    for x, y in [(8, 0), (0, 8), (-8, 0), (0, -8)]:
        for z in [-5, 0, 5]:
            assert not material_at(mesh, x, y, z)
        # Radial sample beside the through-hole: hex is open at the split,
        # but captive between intact plastic above and below it.
        pocket_x, pocket_y = x * 10.5 / 8, y * 10.5 / 8
        assert not material_at(mesh, pocket_x, pocket_y, 0)
        assert material_at(mesh, pocket_x, pocket_y, -2)
        assert material_at(mesh, pocket_x, pocket_y, 2)

    assert not material_at(mesh, 2.4, 0, 0)  # 5 mm shaft bore.
    assert material_at(mesh, 2.9, 0, 0)      # No old M6 centre hole.
    assert not material_at(mesh, 7.5, 7.5, 0)  # Independent OOBB half-grid hole.
    assert material_at(mesh, 4, 0, 0)        # Web between shaft bore and nut.
    assert material_at(mesh, 22, 0, 0)       # Full inner-race seat.
    assert not material_at(mesh, 26, 0, 0)   # Bearing recess.
    assert material_at(mesh, 26, 0, 4)       # Bearing retaining lip.
    for sign in [-1, 1]:
        assert not material_at(mesh, -sign * 13, sign * 13, 0)  # Independent hub joining screws.


@pytest.mark.parametrize("bearing_size", ["6704", "6705"])
@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_wide_small_holders_keep_the_3_by_3_clamps(bearing_size, mode):
    def details(width):
        depth = 9 if width == 5 else 12
        option = next(p for p in OPTIONS if
                      p["bearing_size"] == bearing_size and
                      (p["width"], p["height"], p["depth"], p["extra"]) == (width, 3, depth, ""))
        return dict(option["oobb_details"], mode=mode, prepare_print=False)

    standard = details(3)
    wide = details(5)
    assert working_scad.get_joining_positions(**wide) == working_scad.get_joining_positions(**standard)
    # The extra columns retain plain M6 mounting holes.
    working_scad.define_bearing_dimensions(**wide)
    layout = working_scad.get_mounting_layout(**wide)
    outer_holes = {(h["x"], h["y"]) for h in layout["holes"] if h["radius_name"] == "m6"}
    assert {(x, y) for x in [-30, 30] for y in [-15, 0, 15]} <= outer_holes


def section_checker(mesh):
    sections = {}
    def contains(points, z):
        if z not in sections:
            section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
            starts = np.concatenate([c[:-1, :2] for c in section.discrete])
            ends = np.concatenate([c[1:, :2] for c in section.discrete])
            sections[z] = starts, ends
        starts, ends = sections[z]
        points = np.asarray(points)
        x = points[:, 0, None]
        y = points[:, 1, None]
        crossing = (starts[:, 1] > y) != (ends[:, 1] > y)
        delta_y = ends[:, 1] - starts[:, 1]
        safe_delta = np.where(delta_y == 0, 1, delta_y)
        edge_x = starts[:, 0] + (y - starts[:, 1]) * (ends[:, 0] - starts[:, 0]) / safe_delta
        return np.sum(crossing & (edge_x > x), axis=1) % 2 == 1
    return contains


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_double_6704_centers_seats_and_hubs(tmp_path, mode):
    option = next(p for p in OPTIONS if p["extra"] == "double")
    assert (option["bearing_size"], option["width"], option["height"], option["depth"]) == ("6704", 8, 3, 9)
    assert option["oobb_details"]["bearing_positions"] == [[3, 2], [6, 2]]
    assert "legacy_id" not in option
    kwargs = dict(option["oobb_details"], mode=mode, prepare_print=False)
    mesh = render(tmp_path, **kwargs)
    # Rounded OOBB edges use a 50-facet circle (about 0.01 mm at Y extrema).
    np.testing.assert_allclose(mesh.bounds, [[-60, -22.5, -4.5], [60, 22.5, 4.5]], atol=0.011)
    pieces = mesh.split()
    assert len(pieces) == 3  # One continuous frame and two independent hubs.
    hubs = sorted((p for p in pieces if p.extents[0] < 30), key=lambda p: p.bounds[0, 0])
    np.testing.assert_allclose([p.bounds.mean(axis=0)[:2] for p in hubs], [[-22.5, 0], [22.5, 0]], atol=1e-6)
    contains = section_checker(mesh)
    for x in [-22.5, 22.5]:
        for z in [-4, 0, 4]:
            assert not contains([[x, 0]], z).any()  # M6 shaft bore.
            assert contains([[x + 4, 0]], z).all()  # Solid hub around the bore.
        assert not contains([[x + 12.7, 0]], 0).any()  # Bearing seat.
        assert contains([[x + 12.7, 0]], 4).all()  # Outer retaining lip.
        assert not contains([[x + 11.5, 0]], 4).any()  # Continuous annular relief.


@pytest.mark.parametrize("option", OPTIONS, ids=lambda p: p["id"])
def test_complete_grid_holes_are_open_and_have_walls(tmp_path, option):
    kwargs = dict(option["oobb_details"], mode="3dpr", prepare_print=False)
    working_scad.define_bearing_dimensions(**kwargs)
    layout = working_scad.get_mounting_layout(**kwargs)
    mesh = render(tmp_path, **kwargs)
    contains = section_checker(mesh)
    directions = np.column_stack([np.cos(np.arange(16) * np.pi / 8), np.sin(np.arange(16) * np.pi / 8)])
    face_z = option["depth"] / 2 - 0.5
    for hole in layout["holes"]:
        centre = np.array([hole["x"], hole["y"]])
        radius = oobb.gv("hole_radius_" + hole["radius_name"], "3dpr")
        # Probe the actual mesh, not just the planner's exclusion shapes.
        for z in [-face_z, 0, face_z]:
            assert not contains(centre + directions * (radius - 0.1), z).any(), (hole, z)
        for z in [-face_z, face_z]:
            assert contains(centre + directions * (radius + 0.15), z).all(), (hole, z)
    if option["bearing_size"] in ["606", "608"] and option["taxonomy_3"] == "holder":
        expected = {(x, y) for x in [-15, 0, 15] for y in [-15, 0, 15] if x or y}
        actual = {(h["x"], h["y"]) for h in layout["holes"] if h["radius_name"] == "m6"}
        assert actual == expected
    if option["bearing_size"] == "6810" and option.get("inside") == "embedded_m6_nuts":
        expected = {(x, y) for x in [-15, 15] for y in [-15, 15]}
        actual = {(h["x"], h["y"]) for h in layout["holes"] if h["radius_name"] == "m6"}
        assert expected <= actual
        assert not expected & {(n["x"], n["y"]) for n in layout["nuts"]}


@pytest.mark.parametrize("option", [o for o in OPTIONS if o.get("inside", "").startswith("embedded")], ids=lambda p:p["id"])
@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_all_fitted_nuts_are_enclosed_and_retained(tmp_path, option, mode):
    kwargs = dict(option["oobb_details"], mode=mode, prepare_print=False)
    working_scad.define_bearing_dimensions(**kwargs)
    layout = working_scad.get_mounting_layout(**kwargs)
    mesh = render(tmp_path, **kwargs)
    contains = section_checker(mesh)
    expected_counts = {
        ("6704", "embedded_m3_nuts"): 0,
        ("6705", "embedded_m3_nuts"): 4,
        ("6709", "embedded_m3_nuts"): 20,
        ("6709", "embedded_m6_nuts"): 8,
        ("6810", "embedded_m3_nuts"): 22,
        ("6810", "embedded_m6_nuts"): 6,
    }
    assert len(layout["nuts"]) == expected_counts[option["bearing_size"], option["inside"]]
    for nut in layout["nuts"]:
        assert (nut["x"], nut["y"]) != (0, 0)
        radius = oobb.gv("nut_radius_" + nut["radius_name"], mode)
        depth = oobb.gv("nut_depth_" + nut["radius_name"], mode)
        angles = np.deg2rad(np.arange(6) * 60 + nut["rotation"])
        directions = np.column_stack([np.cos(angles), np.sin(angles)])
        centre = np.array([nut["x"], nut["y"]])
        shoulders = centre + directions * (radius - 0.15)
        assert not contains(shoulders, 0).any(), nut
        assert contains(centre + directions * (radius + 0.15), 0).all(), nut
        for z in [-depth / 2 - 0.15, depth / 2 + 0.15]:
            assert contains(shoulders, z).all(), (nut, z)
    if option["bearing_size"] == "6704":
        expected = {(-7.5, 0), (7.5, 0), (0, -7.5), (0, 7.5)}
        actual = {(h["x"], h["y"]) for h in layout["holes"] if h["region"] == "inside"}
        assert actual == expected


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_6810_30mm_bore_and_four_m6_corners(tmp_path, mode):
    option = next(o for o in OPTIONS if o["extra"] == "inside_hole_30_mm")
    kwargs = dict(option["oobb_details"], mode=mode, prepare_print=False)
    mesh = render(tmp_path, **kwargs)
    assert len(mesh.split()) == 2  # The frame and a continuous centre ring.
    contains = section_checker(mesh)
    angles = np.arange(64) * 2 * np.pi / 64
    directions = np.column_stack([np.cos(angles), np.sin(angles)])
    for z in [-5.5, 0, 5.5]:
        assert not contains(directions * 14.9, z).any()
        assert contains(directions * 15.15, z).all()
        for x in [-15, 15]:
            for y in [-15, 15]:
                centre = np.array([x, y])
                assert not contains(centre + directions * 2.9, z).any()
                assert contains(centre + directions * 3.4, z).all()
    assert oobb.gv("holder_bearing_centre_hole_radius", mode) == 15
    layout = working_scad.get_mounting_layout(**kwargs)
    inner = [h for h in layout["holes"] if h["region"] == "inside"]
    assert {(h["x"], h["y"]) for h in inner if h["radius_name"] == "m6"} == {
        (-15, -15), (-15, 15), (15, -15), (15, 15),
    }
    assert len(inner) == 6  # Two M3 grid holes now carry joining hardware.
    joins = [j for j in layout["joining"] if j["inner_joining"]]
    assert len(joins) == 2
    for joint in joins:
        x, y = joint["screw_x"], joint["screw_y"]
        assert np.hypot(x, y) - 3.6 > 15.3
        for corner_x in [-15, 15]:
            for corner_y in [-15, 15]:
                assert np.hypot(x - corner_x, y - corner_y) > 3.6 + 3.25 + 0.3
        assert not contains([[x, y]], 0).any()
    assert not layout["nuts"]


@pytest.mark.parametrize("option", [o for o in OPTIONS if o["bearing_size"] in ["6808", "6810"]], ids=lambda o:o["id"])
@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_centres_join_on_m3_grid_with_supported_nuts(tmp_path, option, mode):
    kwargs = dict(option["oobb_details"], mode=mode, prepare_print=False)
    thing = draw(**kwargs)
    layout = working_scad.get_mounting_layout(**kwargs)
    joins = [j for j in layout["joining"] if j["inner_joining"]]
    assert len(joins) == 2
    expected = {(0, 21), (0, -21)} if option["extra"] == "inside_hole_30_mm" else {(-7.5, 7.5), (7.5, -7.5)}
    assert {(j["screw_x"],j["screw_y"]) for j in joins} == expected
    components = thing["components_objects"]
    mesh = render(tmp_path, **kwargs)
    contains = section_checker(mesh)
    assert len(mesh.split()) == 2
    for join in joins:
        x,y = join["screw_x"],join["screw_y"]
        # The large bore moves 1.5 mm inward for full-depth flush nuts.
        # Other joins use M3 half-grid positions, never an M6 position.
        if option["extra"] != "inside_hole_30_mm":
            assert x / 7.5 == int(x / 7.5) and y / 7.5 == int(y / 7.5)
        assert x % 15 != 0 or y % 15 != 0
        screw = next(c for c in components if c.get("shape") == "oobb_screw_countersunk" and c["pos"][:2] == [x,y])
        assert screw["radius_name"] == "m3"
        assert screw["overhang"] is True
        assert screw["nut_include"] is True
        if option["extra"] == "inside_hole_30_mm":
            # The entire nut envelope clears the inner bearing surface,
            # even where the full-depth pocket enters the seat's Z range.
            assert np.hypot(x,y) + oobb.gv("nut_radius_m3", mode) + 0.3 < 25 * np.cos(np.pi/50)
        face = -1 if join["screw_face"] == 180 else 1
        half_depth = option["depth"] / 2
        assert not contains([[x,y]], 0).any()
        assert not contains([[x+2.3,y]], face * (half_depth - 0.1)).any()  # Countersink mouth.
        assert not contains([[x+2.5,y]], -face * (half_depth - 0.5)).any()  # Opposite M3 nut recess.
        if option["extra"] == "inside_hole_30_mm":
            assert not contains([[x+2.5,y]], -face * 3.8).any()  # Full-depth nut pocket.
            assert contains([[x+2.5,y]], -face * 2.8).all()  # Material beyond its floor.
            assert contains([[x,y + (3.65 if y > 0 else -3.65)]], -face * 3.8).all()  # Wall before bearing.
