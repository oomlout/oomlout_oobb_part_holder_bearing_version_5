"""Rendered-solid checks for the corner, bearings, and companion bevel gears."""

import json
import hashlib
from pathlib import Path
import subprocess
import tempfile

import numpy as np
import trimesh
import oobb
import working_corner as corner
import working_scad

from action_make_corner import EXAMPLES, OPENSCAD, ROOT, render


def solid_volume(mesh):
    if not len(mesh.faces):
        return 0.0
    triangles = mesh.triangles
    return max(0.0, float(np.einsum("ij,ij->i", triangles[:, 0],
                     np.cross(triangles[:, 1], triangles[:, 2])).sum() / 6))


def intersection_volume(check, angle, folder, example="assembly.scad", examples=EXAMPLES):
    path = folder / f"check_{check}_{angle:.3f}.stl"
    result = subprocess.run([OPENSCAD, "--backend=Manifold", "-o", str(path),
                             "-D", f"check={check}", "-D", f"angle={angle}",
                             str(examples / example)],
                            capture_output=True, text=True, timeout=120)
    log = result.stdout + result.stderr
    if "WARNING:" in log or "ERROR:" in log:
        raise RuntimeError(log)
    if "Current top level object is empty" in log:
        return 0.0
    if result.returncode or not path.is_file():
        raise RuntimeError(log)
    return solid_volume(trimesh.load_mesh(path))


def main(samples=16, bearing_size="6810"):
    examples = ROOT / "examples" / f"corner_{bearing_size}"
    c = json.loads((examples / "layout.json").read_text())
    checks = []
    components = {}
    for path in (examples / "components").glob("*.stl"):
        mesh = trimesh.load_mesh(path)
        assert mesh.is_watertight and mesh.volume > 0, path
        assert len(mesh.split()) == 1, path
        components[path.stem] = {"watertight": True, "components": 1,
                                  "volume_mm3": float(mesh.volume), "bounds_mm": mesh.bounds.tolist()}
    print_path = next((ROOT / "parts").glob(f"*_{bearing_size}_bearing_size_*_{c['depth']}_depth_corner*/3dpr.stl"))
    printed = trimesh.load_mesh(print_path)
    assert printed.is_watertight
    assert len(printed.split()) == 6, "Two connected corner halves and four whole hub discs"
    assert abs(printed.bounds[0, 2]) < 1e-5
    for piece in printed.split():
        assert abs(piece.bounds[0, 2]) < 1e-5, "Every part must start on the print bed"
    expected = sum(components[n]["volume_mm3"] for n in ("frame_negative", "frame_positive"))
    expected += 2 * sum(components[n]["volume_mm3"] for n in ("hub_outer", "hub_gear"))
    assert np.isclose(printed.volume, expected, rtol=1e-6), (printed.volume, expected)
    # Check the rebuilt OOBB gear against the selected, previously generated gear.
    source = Path(c["gear_source"])
    if source.suffix != ".stl":
        source = source.with_name("3dpr.stl")
    if not source.is_absolute():
        source = ROOT / source
    if source.is_file():
        companion = trimesh.load_mesh(source)
        local = trimesh.load_mesh(examples / "components" / "gear.stl")
        np.testing.assert_allclose(companion.bounds, local.bounds, atol=1e-4)
        assert np.isclose(companion.volume, local.volume, rtol=1e-5)
    meshes = {p.stem: trimesh.load_mesh(p) for p in (examples / "components").glob("*.stl")}

    def moved(mesh, translation, rotation=None):
        m = mesh.copy()
        if rotation is not None:
            m.apply_transform(rotation)
        m.apply_translation(translation)
        return m

    rx = trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0])
    ry = trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0])
    rotor = [moved(meshes["hub_outer"], [0, 0, -c["depth"] / 2]),
             moved(meshes["hub_gear"], [0, 0, c["depth"] / 2], rx),
             moved(meshes["gear"], [0, 0, c["distance"] - c["apex"]])]
    frames = [meshes["frame_negative"], meshes["frame_positive"]]

    def positions(angle):
        rz1 = trimesh.transformations.rotation_matrix(np.radians(angle), [0, 0, 1])
        rz2 = trimesh.transformations.rotation_matrix(np.radians(-angle + 180 / c["gear_teeth"]), [0, 0, 1])
        return ([moved(m, [0, 0, -c["distance"]], rz1) for m in rotor],
                [moved(m, [-c["distance"], 0, 0], ry @ rz2) for m in rotor])

    def volume(a, b):
        result = trimesh.boolean.intersection([a, b], engine="manifold")
        # Face contact may leave zero-volume triangles. The signed tetrahedron
        # sum avoids computing undefined centres of mass for those surfaces.
        return solid_volume(result)

    # Physical-size bolt gauges must pass through every planned mounting hole
    # on both arms. This catches filled outlets or a mirrored/misplaced cutter.
    gauges = []
    for hole in c["frame_mounting"]["holes"]:
        gauge = trimesh.creation.cylinder(radius=3 if hole["radius_name"] == "m6" else 1.5,
                                         height=c["depth"] + 2, sections=32)
        gauges.append(moved(gauge, [hole["u"], hole["v"], -c["distance"]]))
        gauges.append(moved(gauge, [-c["distance"], hole["v"], hole["u"]], ry))
    gauge_mesh = trimesh.util.concatenate(gauges)
    gauge_intersections = [volume(gauge_mesh, frame) for frame in frames]
    assert max(gauge_intersections) < 1e-5, gauge_intersections

    gear_volumes = []
    frame_volumes = []
    bearing_volumes = []
    rotor_volumes = []
    # Tooth-cycle checks resolve mesh phase; full-turn checks also exercise the
    # four stand-offs and every hole relative to the stationary corner.
    for i in range(samples):
        first, second = positions(i * 360 / c["gear_teeth"] / samples)
        gear_volumes.append(volume(first[-1], second[-1]))
    checks.append({"pair": "gear_gear", "samples": samples,
                   "max_intersection_mm3": max(gear_volumes)})
    for i in range(64):
        angle = i * 360 / 64
        first, second = positions(angle)
        rz1 = trimesh.transformations.rotation_matrix(np.radians(angle), [0, 0, 1])
        rz2 = trimesh.transformations.rotation_matrix(np.radians(-angle + 180 / c["gear_teeth"]), [0, 0, 1])
        bearings = [moved(meshes["bearing"], [0, 0, -c["distance"]], rz1),
                    moved(meshes["bearing"], [-c["distance"], 0, 0], ry @ rz2)]
        frame_volumes.append(max(volume(f, m) for f in frames for m in first + second))
        bearing_volumes.append(max(volume(b, m) for b in bearings for m in frames + first + second))
        rotor_volumes.append(max(volume(a, b) for a in first for b in second))
    checks.extend([
        {"pair": "frame_rotors", "samples": 64, "range_degrees": 360,
         "max_intersection_mm3": max(frame_volumes)},
        {"pair": "bearings_printed_parts", "samples": 64, "range_degrees": 360,
         "max_intersection_mm3": max(bearing_volumes)},
        {"pair": "frame_halves", "samples": 1, "max_intersection_mm3": volume(*frames)},
        {"pair": "cross_axis_rotors", "samples": 64, "range_degrees": 360,
         "max_intersection_mm3": max(rotor_volumes)},
        {"pair": "hub_halves_and_gear", "samples": 1,
         "max_intersection_mm3": max(volume(a, b) for i, a in enumerate(rotor) for b in rotor[i+1:])},
    ])
    print("Direct mesh checks:", checks, flush=True)
    # Independent OpenSCAD checks exercise the delivered assembly example's
    # own transforms and diagnostic selectors as well as the mesh calculations.
    with tempfile.TemporaryDirectory(prefix="oobb_corner_check_") as folder:
        temp = Path(folder)
        # Independently draw the complete regular holder, isolate its lower
        # interior and compare the copied half as actual rendered solids.
        regular = corner.new_thing()
        working_scad.get_bearing_holder(regular, **c["hub_source"])
        clip = corner.new_thing()
        corner.group(clip, regular)
        outside = corner.new_thing()
        corner.ring(outside, 500, c["hub_radius"], 100)
        corner.group(clip, outside, typ="negative")
        corner.primitive(clip, "oobb_cube", "negative", size=[1000, 1000, 500],
                         zz="bottom", pos=[0, 0, 0])
        reference = corner.new_thing()
        corner.group(reference, clip, pos=[0, 0, c["depth"] / 2])
        reference_path = temp / "regular_6810_interior.scad"
        oobb.opsc_make_object(str(reference_path), reference["components"], mode="3dpr", save_type="none")
        render(reference_path)
        reference_mesh = trimesh.load_mesh(reference_path.with_suffix(".stl"))
        hub_differences = [solid_volume(trimesh.boolean.difference(pair, engine="manifold"))
                           for pair in ([reference_mesh, meshes["hub_outer"]],
                                        [meshes["hub_outer"], reference_mesh])]
        assert max(hub_differences) < 1e-5, hub_differences
        cross_checks = [intersection_volume(check, 0, temp, examples=examples) for check in range(1, 6)]
        assert max(cross_checks) < 1e-5, cross_checks
        exploded_checks = [intersection_volume(check, 0, temp, "exploded.scad", examples=examples) for check in range(1, 6)]
        assert max(exploded_checks) < 1e-5, exploded_checks
    report = {"components": components, "print_components": 6,
              "mounting_holes_per_arm": c["frame_mounting"]["counts_per_arm"],
              "mounting_hole_gauges": len(gauges),
              "mounting_hole_gauge_intersection_mm3": gauge_intersections,
              "print_volume_matches_assembly": True, "motion_checks": checks,
              "engine": "Manifold: rendered STL intersections plus OpenSCAD example cross-checks",
              "openscad_cross_checks_mm3": cross_checks,
              "openscad_exploded_checks_mm3": exploded_checks,
              "regular_interior_difference_mm3": hub_differences,
              "tooth_cycle_degrees": 360 / c["gear_teeth"],
              "fit": "CAD clearance validated; physical fit and load testing pending"}
    sources = [ROOT / n for n in ("working_corner.py", "working_scad.py", "working_populate.py", "action_make_corner.py", "validate_corner.py")]
    sources += [examples / "assembly.scad", examples / "exploded.scad", examples / "layout.json", print_path]
    sources += list((examples / "components").glob("*.stl"))
    report["sha256"] = {str(p.relative_to(ROOT)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sources}
    (examples / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    assert all(check["max_intersection_mm3"] < 1e-5 for check in checks), checks
    print("All rendered corner checks passed.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bearing", choices=["6810", "6704", "all"], default="6810")
    args = parser.parse_args()
    for bearing_size in (["6810", "6704"] if args.bearing == "all" else [args.bearing]):
        main(bearing_size=bearing_size)
