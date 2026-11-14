"""OOBB corner bearing mount. Coordinates are mm; axes intersect at the origin.

The bearing axes are X and Z. The stationary corner splits on vertical Y=0.
Each inner race is retained by two complete, axially split hub discs.
"""

import copy
import functools
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

import oobb


def legacy_bevel_dimensions(teeth, module, depth, face_width, backlash=0.2):
    """Bounds for the saved backed-tooth gear used by the corner fixtures.

    These fixtures use a 6 mm tooth face on a 12 mm backed gear. The shared
    library now validates a different, full-depth flat-top gear. Applying that
    validator here rejected the existing fixtures and changing the face width
    would change their reviewed pitch-apex/spacer contract.
    """
    values = (teeth, module, depth, face_width, backlash)
    if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in values):
        raise ValueError("Legacy bevel dimensions must be finite numbers")
    if teeth < 3 or int(teeth) != teeth or min(module, depth, face_width) <= 0:
        raise ValueError("Invalid legacy bevel tooth count or dimensions")
    if not 0 <= backlash < math.pi * module / 2:
        raise ValueError("Invalid legacy bevel backlash")
    pitch_radius = module * teeth / 2
    cone_distance = pitch_radius / math.sin(math.pi / 4)
    if face_width >= cone_distance:
        raise ValueError("Legacy bevel tooth face reaches the pitch apex")
    return {"inner_root_radius": (pitch_radius - module * 1.25) * (1 - face_width / cone_distance)}


@functools.lru_cache(maxsize=32)
def bevel_apex(teeth, module, depth, face_width, backlash):
    """Measure the actual BOSL2 tooth bounds, as the gear repository does."""
    from components.oobb_gear_bevel.working import _build_wrapper_source
    legacy_bevel_dimensions(teeth, module, depth, face_width, backlash)
    source = _build_wrapper_source() + f'''
bare=bevel_gear(mod={module}, teeth={teeth}, mate_teeth={teeth},
    face_width={face_width}, backing=0, spiral=0, cutter_radius=0,
    pressure_angle=20, backlash={backlash}, clearance={module / 4}, anchor="pitchbase");
echo(CORNER_APEX={module * teeth / 2 + depth / 2}-pointlist_bounds(bare[0])[1].z);
cube(1);
'''
    executable = shutil.which("openscad.com") or shutil.which("openscad")
    if not executable:
        raise RuntimeError("OpenSCAD is needed to measure the bevel pitch apex")
    with tempfile.TemporaryDirectory(prefix="oobb_corner_apex_") as folder:
        path = Path(folder) / "measure.scad"
        path.write_text(source, encoding="utf-8")
        result = subprocess.run([executable, "-o", str(path.with_suffix(".csg")), str(path)],
                                capture_output=True, text=True, timeout=90)
    log = result.stdout + result.stderr
    match = re.search(r"CORNER_APEX\s*=\s*([\d.e+-]+)", log)
    if result.returncode or not match or "WARNING:" in log or "ERROR:" in log:
        raise RuntimeError(log)
    return float(match[1])


def layout(**kwargs):
    c = copy.deepcopy(kwargs["corner"])
    d = kwargs.get("depth", 12)
    h = kwargs.get("height", 5) * oobb.gv("osp")
    ri, ro = c["bearing_inner_diameter"] / 2, c["bearing_outer_diameter"] / 2
    bd = c["bearing_depth"]
    if not 0 < ri < ro or not 0 < bd + c["axial_clearance"] < d:
        raise ValueError("Bearing diameters / depth leave no retaining lips")
    if not 0 < c["split_gap"] < 1 or not 0 < c["radial_clearance"] < 1:
        raise ValueError("Use positive fit clearances below 1 mm")
    apex = bevel_apex(c["gear_teeth"], c["gear_module"], c["gear_depth"],
                      c["gear_face_width"], c["gear_backlash"])
    pitch = oobb.gv("osp")
    axis_pitch = c.get("axis_pitch", pitch)
    if axis_pitch not in (pitch, pitch / 2):
        raise ValueError("Axis pitch must use the full or half OOBB grid")
    distance = math.ceil(max(apex + c["gear_depth"] / 2 + d / 2 + c["minimum_gear_gap"],
                             ro + d / 2 + 3) / axis_pitch) * axis_pitch
    row = c["mounting_row"]
    if row % pitch or row - 3.5 < ro + c["radial_clearance"] + 2:
        raise ValueError("Far mounting row must clear the bearing and use the OOBB grid")
    if h / 2 < ro + c["radial_clearance"] + 3:
        raise ValueError("Increase height to leave material outside the bearing seat")
    hub_source = regular_hub_source(**kwargs)
    import working_scad
    working_scad.define_bearing_dimensions(**hub_source)
    hub_radius = oobb.gv(f"holder_bearing_{hub_source['bearing_size']}_relief_id", "3dpr")
    opening_radius = ro - min(1.8, (ro - ri) / 4)
    if opening_radius - hub_radius < 1:
        raise ValueError("Bearing races leave insufficient running clearance")
    # The small hub uses existing cardinal M3 grid holes; the large hub uses
    # the four M6 corners. Both patterns already exist in the companion gears.
    gear_mounts = c.get("gear_mounts", [[x, y] for x in (-15, 15) for y in (-15, 15)])
    mount_name = c.get("gear_mount_radius_name", "m6")
    mount_radius = max(oobb.gv(f"hole_radius_{mount_name}", m) for m in ("3dpr", "true", "laser"))
    reach = max(math.hypot(x, y) for x, y in gear_mounts)
    gd = legacy_bevel_dimensions(c["gear_teeth"], c["gear_module"],
                                c["gear_depth"], c["gear_face_width"], c["gear_backlash"])
    if reach + mount_radius + 1.2 > gd["inner_root_radius"]:
        raise ValueError("Choose a larger bevel gear for the hub mounting pattern")
    if reach + mount_radius + 0.3 > ri - c["radial_clearance"]:
        raise ValueError("Bearing bore is too small for this hub mounting pattern")
    c.update(depth=d, height_mm=h, distance=distance, apex=apex,
             inner_radius=ri, outer_radius=ro, hub_radius=hub_radius,
             opening_radius=opening_radius, far_edge=row + pitch / 2,
             gear_mounts=gear_mounts,
             gear_mount_radius_name=mount_name,
             gear_pad_radius=c.get("gear_pad_radius", 4.8),
             hub_source=hub_source,
             joining_screw_length=c.get("joining_screw_length", 25),
             spacer=distance - d / 2 - apex - c["gear_depth"] / 2,
             hub_split_gap=0,
             bearing_size=str(kwargs.get("bearing_size", "6810")))
    c["mounting_minimum_web"] = kwargs.get("mounting_minimum_web", 0.3)
    c["frame_mounting"] = flange_mounting_layout(c)
    return c


def regular_hub_source(**kwargs):
    """Use the regular catalogue interior, including its grid and hub joins."""
    import working_populate
    size = str(kwargs.get("bearing_size", "6810"))
    source = next((o for o in working_populate.get_options()
                   if o["bearing_size"] == size and not o["extra"]
                   and o.get("holder_type", "holder") == "holder"), None)
    if source is None:
        source = next(o for o in working_populate.get_options()
                      if o["bearing_size"] == "6810" and not o["extra"])
    k = copy.deepcopy(source["oobb_details"])
    k.update(bearing_size=size, width=kwargs.get("width", 7), height=kwargs.get("height", 5),
             depth=kwargs.get("depth", 12), mode="3dpr", prepare_print=False)
    if size != "6810":
        for key in ("bearing_inner_diameter", "bearing_outer_diameter", "bearing_depth"):
            k[key] = kwargs["corner"][key]
    if "hub_nut_depth" in kwargs["corner"]:
        nut_depth = kwargs["corner"]["hub_nut_depth"]
        if not 0 < nut_depth <= (k["depth"] - kwargs["corner"]["bearing_depth"]) / 2 - 0.1 + 1e-8:
            raise ValueError("Hub nut recess must stay outside the bearing with axial clearance")
        k["joining_nut_depth"] = nut_depth
    return k


def new_thing():
    return {"components": [], "components_objects": [], "components_string": []}


def primitive(thing, shape, typ="positive", **kwargs):
    p3 = {}
    p3["shape"] = shape
    p3["type"] = typ
    p3["mode"] = "3dpr"
    p3["pos"] = [0, 0, 0]
    p3.update(kwargs)
    oobb.append_full(thing, **p3)


def group(thing, child, pos=None, rot=None, color="", typ="positive"):
    p3 = {}
    p3["type"] = "rotation"
    p3["typetype"] = typ
    p3["objects"] = copy.deepcopy(child["components"])
    p3["pos"] = pos or [0, 0, 0]
    p3["rot"] = rot or [0, 0, 0]
    p3["inclusion"] = "all"
    if color:
        p3["color"] = color
    thing["components"].append(p3)


def ring(thing, outer, inner, depth, pos=None):
    child = new_thing()
    primitive(child, "oobb_cylinder", radius=outer, depth=depth)
    primitive(child, "oobb_cylinder", "negative", radius=inner, depth=depth + .02)
    group(thing, child, pos=pos)


def flange_mounting_layout(c):
    """Enumerate the entire OOBB/OOBE grid on each bearing-facing arm.

    Main-grid points prefer M6, falling back to M3 if necessary. Every other
    half-grid point is M3. A normal mounting bore must clear the bearing seat,
    perpendicular arm, and the transverse seam screw's head/nut channels.
    """
    step = oobb.gv("osp") / 2
    web = c["mounting_minimum_web"]
    radii = {name: max(oobb.gv(f"hole_radius_{name}", mode)
                      for mode in ("3dpr", "true", "laser")) for name in ("m6", "m3")}
    join_radius = max(oobb.gv("nut_radius_m3", "3dpr"),
                      oobb.gv("screw_socket_cap_radius_m3", "3dpr"))
    near = -c["distance"] - c["depth"] / 2
    # The other arm runs parallel to this bore; keep the entire circular
    # opening outside it so both ends remain accessible and fully drilled.
    free_near = -c["distance"] + c["depth"] / 2
    holes, omitted = [], []
    for iu in range(math.ceil(near / step), math.floor(c["far_edge"] / step) + 1):
        for iv in range(math.ceil(-c["height_mm"] / 2 / step),
                        math.floor(c["height_mm"] / 2 / step) + 1):
            u, v = iu * step, iv * step
            choices = ["m6", "m3"] if iu % 2 == iv % 2 == 0 else ["m3"]
            reasons = []
            for name in choices:
                radius = radii[name]
                if min(c["far_edge"] - u, c["height_mm"] / 2 - abs(v)) < radius + web:
                    reason = "edge"
                elif u - radius - web < free_near:
                    reason = "perpendicular_arm"
                elif math.hypot(u, v) - radius - web < c["outer_radius"] + c["radial_clearance"]:
                    reason = "bearing_seat"
                elif abs(u - (c["mounting_row"] - step)) < radius + join_radius + web:
                    reason = "joining_access"
                else:
                    holes.append({"u": u, "v": v, "radius_name": name, "radius": radius})
                    break
                reasons.append({"radius_name": name, "reason": reason})
            else:
                omitted.append({"u": u, "v": v, "attempts": reasons})
    return {"holes": holes, "omitted": omitted,
            "counts_per_arm": {name: sum(h["radius_name"] == name for h in holes)
                               for name in ("m6", "m3")}}


def flange(c, mirrored=False):
    """Complete unsplit stationary flange with bearing retaining shoulders."""
    t = new_thing()
    D, d, far = c["distance"], c["depth"], c["far_edge"]
    center = (far - D - d / 2) / 2 * (-1 if mirrored else 1)
    primitive(t, "oobb_cube", size=[far + D + d / 2, c["height_mm"], d],
              zz="center", pos=[center, 0, 0])
    primitive(t, "oobb_cylinder", "negative", radius=c["opening_radius"], depth=d + 2)
    primitive(t, "oobb_cylinder", "negative",
              radius=c["outer_radius"] + c["radial_clearance"],
              depth=c["bearing_depth"] + c["axial_clearance"])
    # Every fitting main-grid and half-grid hole, including the extra far row.
    sign = -1 if mirrored else 1
    for hole in c["frame_mounting"]["holes"]:
        primitive(t, "oobb_hole", "negative", radius_name=hole["radius_name"], depth=d + 2,
                  pos=[sign * hole["u"], hole["v"], -d / 2 - 1])
    return t


def stationary(c):
    t = new_thing()
    D = c["distance"]
    group(t, flange(c), pos=[0, 0, -D])
    group(t, flange(c, mirrored=True), pos=[-D, 0, 0], rot=[0, 90, 0])
    # The standard screw primitive supplies the bore, socket, nut and printable
    # overhang details. Top/bottom clearance opens both access channels.
    cut = new_thing()
    group(cut, t)
    for x, z in [(-D, -D), (c["mounting_row"] - 7.5, -D), (-D, c["mounting_row"] - 7.5)]:
        primitive(cut, "oobb_screw_socket_cap", "negative", radius_name="m3",
                  depth=c["joining_screw_length"], pos=[x, c["joining_screw_length"] / 2, z],
                  rot=[-90, 0, 0], hole=True, nut_include=True,
                  overhang=True, clearance=["top", "bottom"])
    return cut


def corner_half(c, positive=False):
    t = new_thing()
    group(t, stationary(c))
    # Remove one side including half the assembly seam clearance.
    span = 4 * (c["distance"] + c["far_edge"])
    side = -1 if positive else 1
    primitive(t, "oobb_cube", "negative", size=[span, span, span], zz="center",
              pos=[0, side * (span / 2 - c["split_gap"] / 2), 0])
    return t


@functools.lru_cache(maxsize=32)
def regular_hub(source_json, radius):
    """Draw the regular interior with the same shared feature functions."""
    import working_scad
    k = json.loads(source_json)
    working_scad.define_bearing_dimensions(**k)
    k["mounting_layout"] = working_scad.get_mounting_layout(**k)
    t = new_thing()
    primitive(t, "oobb_cylinder", radius=radius, depth=k["depth"])
    working_scad.add_bearing_seat_and_relief(t, **k)
    working_scad.add_perimeter_holes(t, **k)
    working_scad.add_interior_holes(t, **k)
    working_scad.add_shaft_interface(t, **k)
    for joining in k["mounting_layout"]["joining"]:
        if joining["inner_joining"]:
            working_scad.add_joining_screw(t, **dict(k, **joining))
    return t


def hub_half(c, gear_side=False):
    """Copy the regular bearing interior half, then add gear stand-offs."""
    d = c["depth"]
    clipped = new_thing()
    group(clipped, regular_hub(json.dumps(c["hub_source"], sort_keys=True), c["hub_radius"]))
    primitive(clipped, "oobb_cube", "negative", size=[500, 500, 500], zz="center",
              pos=[0, 0, -250 if gear_side else 250])
    t = new_thing()
    group(t, clipped, pos=[0, 0, d / 2], rot=[180, 0, 0] if gear_side else [0, 0, 0])
    # The gear-facing disc has four integral stand-offs on its outside face.
    # Build below z=0; print orientation is corrected by the layout generator.
    if gear_side:
        for x, y in c["gear_mounts"]:
            primitive(t, "oobb_cylinder", radius=c["gear_pad_radius"], depth=c["spacer"],
                      zz="top", pos=[x, y, 0])
        for x, y in c["gear_mounts"]:
            primitive(t, "oobb_hole", "negative", radius_name=c["gear_mount_radius_name"],
                      depth=c["spacer"] + 2, pos=[x, y, -c["spacer"] - 1])
        if c.get("gear_join_access"):
            import working_scad
            for join in working_scad.get_joining_positions(**c["hub_source"]):
                if join["inner_joining"]:
                    # Preserve tool and nut access where the smaller pads pass
                    # close to the regular hub's diagonal joining recesses.
                    primitive(t, "oobb_hole", "negative", radius_name="screw_countersunk_radius_m3",
                              depth=c["spacer"] + .01,
                              pos=[join["screw_x"], -join["screw_y"], -c["spacer"] - .01])
    return t


def bearing(c):
    t = new_thing()
    ring(t, c["outer_radius"], c["inner_radius"], c["bearing_depth"])
    return t


def get_bearing_holder_corner(thing, **kwargs):
    c = layout(**kwargs)
    t = new_thing()
    selected = kwargs.get("corner_part", "all")
    if kwargs.get("prepare_print", True):
        step = c["distance"] + c["far_edge"] + c["depth"] / 2 + kwargs.get("print_gap", 10)
        for index, positive in enumerate((False, True)):
            if selected in ("all", "frame", "frame_positive" if positive else "frame_negative"):
                group(t, corner_half(c, positive), pos=[index * step, 0, c["height_mm"] / 2],
                      rot=[-90 if positive else 90, 0, 0])
        for axis in range(2):
            for side in range(2):
                if selected in ("all", "hubs", "hub_gear" if side else "hub_outer"):
                    group(t, printable_hub(c, bool(side)),
                          pos=[axis * step + side * (2 * c["hub_radius"] + 10), step, 0])
    else:
        explode = kwargs.get("explode", 0)
        for positive in (False, True):
            if selected in ("all", "frame", "frame_positive" if positive else "frame_negative"):
                group(t, corner_half(c, positive), pos=[0, explode * (1 if positive else -1), 0],
                      color="LightSlateGray" if positive else "Silver")
        for axis, (pos, rot) in enumerate([([0, 0, -c["distance"]], [0, 0, 0]),
                                          ([-c["distance"], 0, 0], [0, 90, 0])]):
            stack = new_thing()
            for side in (False, True):
                if selected in ("all", "hubs", "hub_gear" if side else "hub_outer"):
                    group(stack, hub_half(c, side),
                          pos=[0, 0, (c["depth"] / 2 + explode) * (1 if side else -1)],
                          rot=[180, 0, 0] if side else [0, 0, 0], color="DarkOrange")
            if kwargs.get("show_bearings", False):
                group(stack, bearing(c), color="SteelBlue")
            group(t, stack, pos=pos, rot=rot)
    group(thing, t, pos=kwargs.get("pos"), rot=kwargs.get("rot"))


def printable_hub(c, gear_side):
    # Gear pads would leave a large unsupported disc if printed pads-down.
    # Instead print its split face down: the full spigot contacts the bed and
    # the regular bearing lip needs local support; pads grow from the top face.
    if gear_side:
        t = new_thing()
        group(t, hub_half(c, True), pos=[0, 0, (c["depth"] - c["hub_split_gap"]) / 2], rot=[180, 0, 0])
        return t
    return hub_half(c, False)
