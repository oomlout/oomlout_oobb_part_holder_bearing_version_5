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


OPTIONS = working_populate.get_options()
OPENSCAD = shutil.which("openscad")


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
    thing = oobb.get_default_thing(type="test_bearing_plate")
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
    assert len(OPTIONS) == 36
    assert len({option["id"] for option in OPTIONS}) == 36
    assert len({option["legacy_id"] for option in OPTIONS if "legacy_id" in option}) == 14
    extras_6704 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6704"}
    extras_6705 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6705"}
    assert extras_6705 == extras_6704
    assert len(extras_6705) == 8
    extras_6709 = {option["extra"] for option in OPTIONS if option["bearing_size"] == "6709"}
    assert extras_6709 == extras_6705 | {
        "inside_embedded_m6_nuts",
        "inside_mechanical_coupler_flange_name_5_mm_bore",
    }
    assert all(p["width"] == p["height"] == 5 for p in OPTIONS if p["bearing_size"] == "6709")
    angled = [option for option in OPTIONS if option["taxonomy_3"] == "plate_90_degree"]
    assert len(angled) == 2
    assert {option["taxonomy_9"] for option in angled} == {"", "basic"}
    for option in OPTIONS:
        assert "jack" not in option["id"]
        assert option["taxonomy_5"] == option["bearing_size"] + "_bearing_size"
        assert option["taxonomy_8"] == "12_depth"


@pytest.mark.parametrize("option", OPTIONS, ids=[option["id"] for option in OPTIONS])
def test_print_halves_preserve_assembly(tmp_path, option):
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    assembled = render(tmp_path / "assembled", **kwargs)
    kwargs["prepare_print"] = True
    printed = render(tmp_path / "printed", **kwargs)

    assert assembled.bounds[0, 2] == pytest.approx(-6)
    assert assembled.bounds[1, 2] == pytest.approx(6)
    assert printed.bounds[0, 2] == pytest.approx(0, abs=1e-6)
    assert printed.volume == pytest.approx(assembled.volume, rel=1e-6)

    if not kwargs.get("split", True):
        assert printed.bounds[1, 2] == pytest.approx(12)
        return

    split_z = kwargs.get("split_z", 0)
    assert printed.bounds[1, 2] == pytest.approx(6 + abs(split_z))
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

    # Volumes measured from the saved v3 lower-half STLs, in cubic mm.
    # Allow small tessellation / v5 fastener-support differences, but catch
    # lost through-holes, wrong bearing fits, or rotated-away nut pockets.
    legacy_volumes = {
        "oobb_bearing_plate_03_03_12_606": 9625.18,
        "oobb_bearing_plate_03_03_12_6704": 9428.25,
        "oobb_bearing_plate_03_03_12_6803": 9430.54,
        "oobb_bearing_plate_03_03_12_6804": 8254.62,
        "oobb_bearing_plate_05_05_12_6808": 26160.02,
        "oobb_bearing_plate_07_05_12_6810": 37438.13,
        "oobb_bearing_plate_jack_03_03_12_606": 9320.81,
    }
    if option.get("legacy_id") in legacy_volumes:
        assert left.volume == pytest.approx(legacy_volumes[option["legacy_id"]], rel=0.001)

    # Reassemble the two independently clipped halves and check mass properties.
    left.apply_translation([0, 0, -6])
    right.apply_translation([-distance, 0, -6])
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
    assert len(parts) == 36
    assert all(part["kwargs"]["prepare_print"] is False for part in parts)


def test_named_bearing_seats_and_6810_through_holes():
    kwargs = copy.deepcopy(OPTIONS[5]["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    thing = draw(**kwargs)
    # The perimeter array's top/bottom branches need an explicit bottom Z;
    # otherwise those holes only pierce the upper half of the assembly.
    patterns = [p for p in thing["components_objects"] if p.get("shape") == "oobb_holes"]
    perimeter = next(p for p in patterns if p.get("holes") == ["top", "bottom"])
    assert perimeter["pos"][2] < -6
    assert perimeter["depth"] > 12
    radii = [p.get("radius_name") for p in thing["components_objects"]]
    assert "plate_bearing_6810_od" in radii
    assert "plate_bearing_6810_id" in radii
    assert oobb.gv("plate_bearing_6810_od", "3dpr") == 32.7
    assert oobb.gv("plate_bearing_6810_id", "3dpr") == 25


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


@pytest.mark.parametrize("bearing_size", ["6704", "6705", "6709", "6810"])
@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_embedded_nuts_are_captive_and_open_at_the_split(tmp_path, bearing_size, mode):
    option = next(p for p in OPTIONS if p["bearing_size"] == bearing_size
                  and p["extra"] == "inside_embedded_m3_nuts")
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)

    def material_at(x, y, z):
        # Cross the rendered section contours, including all holes and islands.
        section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        crossings = 0
        for contour in section.discrete:
            for a, b in zip(contour[:-1], contour[1:]):
                if (a[1] > y) != (b[1] > y):
                    edge_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                    crossings += edge_x > x
        return bool(crossings % 2)

    nut_radius = oobb.gv("nut_radius_m3", mode)
    bore_radius = oobb.gv("hole_radius_m6", mode)
    hub_radius = oobb.gv(f"plate_bearing_{bearing_size}_id", mode)
    assert len(kwargs["embedded_nut_positions"]) == (8 if bearing_size == "6810" else 4)
    joining_radius = 7.5 if bearing_size in ["6704", "6705"] else 15
    joins = [np.array([-1, 1]) * joining_radius / np.sqrt(2),
             np.array([1, -1]) * joining_radius / np.sqrt(2)]
    for x, y in kwargs["embedded_nut_positions"]:
        # Sample beside the bolt bore, inside the hex. The pocket must span
        # the split plane, but have retaining material above AND below it.
        for z in [-1, 0, 1]:
            assert not material_at(x + 2.5, y, z)
        for z in [-2, 2]:
            assert material_at(x + 2.5, y, z)

        angle = kwargs["embedded_nut_rotation"]
        if kwargs.get("embedded_nut_rotation_radial"):
            angle += np.rad2deg(np.arctan2(y, x))
        angles = np.deg2rad(np.arange(6) * 60 + angle)
        vertices = np.column_stack([np.cos(angles), np.sin(angles)]) * nut_radius
        vertices += [x, y]
        # Allow for the inscribed 50-sided bearing cylinder in actual SCAD.
        outer_web = hub_radius * np.cos(np.pi / 50) - np.linalg.norm(vertices, axis=1).max()
        inner_web = np.hypot(x, y) - nut_radius * np.cos(np.pi / 6) - bore_radius
        minimum = 0.2 if bearing_size == "6704" else 1.2
        if bearing_size == "6810" and x and y:
            minimum = 0.6
        assert outer_web > minimum
        assert inner_web > minimum
        # The tiny web between centre bore and captive nut is actually present.
        web = np.array([x, y]) / np.hypot(x, y) * (bore_radius + inner_web / 2)
        assert material_at(web[0], web[1], 0)

        # Check a point in the actual plastic bridge between every hex and
        # joining bore. This catches the old central laser standoff collision.
        for index, join in enumerate(joins):
            if np.linalg.norm(join - [x, y]) > joining_radius:
                # The line to a distant screw can legitimately cross the
                # centre bore or another nut; only probe neighbouring webs.
                continue
            nearest = None
            distance = float("inf")
            for a, b in zip(vertices, np.roll(vertices, -1, axis=0)):
                edge = b - a
                t = np.clip(np.dot(join - a, edge) / np.dot(edge, edge), 0, 1)
                point = a + t * edge
                length = np.linalg.norm(join - point)
                if length < distance:
                    nearest, distance = point, length
            gap = distance - oobb.gv("hole_radius_m3", mode)
            assert gap > 0.3
            probe = nearest + (join - nearest) / distance * gap / 2
            assert material_at(probe[0], probe[1], 0)

            head_radius_name = "screw_countersunk_radius_m3"
            if kwargs.get("inner_joining_head") == "socket_cap":
                head_radius_name = "screw_socket_cap_radius_m3"
            head_radius = oobb.gv(head_radius_name, mode)
            centre = np.array([x, y])
            distance = np.linalg.norm(join - centre)
            gap = distance - head_radius - oobb.gv("hole_radius_m3", mode)
            assert gap > 0.25
            probe = join + (centre - join) / distance * (head_radius + gap / 2)
            assert material_at(probe[0], probe[1], 5.9 if index == 0 else -5.9)


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
    assert {p["extra"] for p in large} == {"", "inside_embedded_m3_nuts", "inside_embedded_m6_nuts"}
    assert all((p["width"], p["height"], p["depth"]) == (7, 5, 12) for p in large)


@pytest.mark.parametrize("mode", ["3dpr", "true", "laser"])
def test_608_bearing_seat_and_retaining_lips(tmp_path, mode):
    option = next(p for p in OPTIONS if p["bearing_size"] == "608")
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = mode
    kwargs["prepare_print"] = False
    mesh = render(tmp_path, **kwargs)
    assert len(mesh.split()) == 2
    assert oobb.gv("plate_bearing_608_id", mode) == 4
    assert oobb.gv("plate_bearing_608_od", mode) == (11.2 if mode == "3dpr" else 11)
    assert oobb.gv("plate_bearing_608_depth", mode) == 7
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
    hub_radius = oobb.gv(f"plate_bearing_{bearing_size}_id", mode)
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
        assert material_at(mesh, direction[0] * 21, direction[1] * 21, 0)

    assert not material_at(mesh, 2.8, 0, 0)  # Original M6 centre bore retained.
    assert material_at(mesh, 4, 0, 0)
    assert material_at(mesh, 7.75, 0, 0)   # No obsolete M3 slot left behind.
    for sign in [-1, 1]:
        assert not material_at(mesh, -sign * 15 / np.sqrt(2), sign * 15 / np.sqrt(2), 0)


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


@pytest.mark.parametrize("option", [p for p in OPTIONS if p["bearing_size"] == "6709" or (p["bearing_size"] == "6810" and p.get("inside"))], ids=lambda p: p["bearing_size"] + "_" + (p["extra"] or "standard"))
def test_joining_screws_are_diagonal_and_clear_grid(option):
    kwargs = copy.deepcopy(option["oobb_details"])
    kwargs["mode"] = "3dpr"
    kwargs["prepare_print"] = False
    thing = draw(**kwargs)
    screws = [p for p in thing["components_objects"] if p.get("shape") == "oobb_screw_countersunk"]
    inner = [p for p in screws if np.linalg.norm(p["pos"][:2]) < 25]
    if kwargs.get("horn_adapter") == "screws" or kwargs.get("split") is False:
        assert not inner
        return
    assert len(inner) == (4 if kwargs["shaft"] in ["motor_gearmotor_01", "motor_servo_micro_01"] else 2)
    for screw in inner:
        x, y = screw["pos"][:2]
        assert abs(x) == pytest.approx(15 / np.sqrt(2))
        assert abs(y) == pytest.approx(15 / np.sqrt(2))
        # Clearance using circumcircles bounds the entire head and nut shapes.
        for point in [(-15, 0), (15, 0), (0, -15), (0, 15)]:
            gap = np.linalg.norm(np.array([x, y]) - point) - 3.6 - oobb.gv("nut_radius_m6", "3dpr")
            assert gap > 1.9


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
        assert len(inner) == expected
        for screw in inner:
            assert abs(screw["screw_x"]) == pytest.approx(7.5 / np.sqrt(2))
            assert abs(screw["screw_y"]) == pytest.approx(7.5 / np.sqrt(2))
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
    assert oobb.gv("plate_bearing_6709_id", mode) == 22.5
    assert oobb.gv("plate_bearing_6709_od", mode) == (27.7 if mode == "3dpr" else 27.5)
    assert oobb.gv("plate_bearing_6709_depth", mode) == 6

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
    assert material_at(mesh, 8, 8, 0)        # Not a mistaken 16 mm square pattern.
    assert material_at(mesh, 4, 0, 0)        # Web between shaft bore and nut.
    assert material_at(mesh, 22, 0, 0)       # Full inner-race seat.
    assert not material_at(mesh, 26, 0, 0)   # Bearing recess.
    assert material_at(mesh, 26, 0, 4)       # Bearing retaining lip.
    for sign in [-1, 1]:
        assert not material_at(mesh, -sign * 15 / np.sqrt(2), sign * 15 / np.sqrt(2), 0)  # Independent hub joining screws.
