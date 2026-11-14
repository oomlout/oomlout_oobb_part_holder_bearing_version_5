import copy
import math
import oobb
import yaml
import os
import scad_help

def main(**kwargs):
    make_scad(**kwargs)

def make_scad(**kwargs):
    typ = scad_help.get_typ(**kwargs)
    oomp_mode = "project"
    #oomp_mode = "oobb"
    filt = kwargs.get("filter", "")
    build_variables = scad_help.get_build_variables(typ, filter=filt)
    if True:
        kwargs.setdefault("filter", build_variables["filter"])
        kwargs.setdefault("save_type", build_variables["save_type"])
        kwargs.setdefault("navigation", build_variables["navigation"])
        kwargs.setdefault("overwrite", build_variables["overwrite"])
        kwargs.setdefault("modes", build_variables["modes"])
        kwargs["oomp_mode"] = oomp_mode
        kwargs.setdefault("oomp_run", build_variables["oomp_run"])
    parts = get_parts(kwargs, oomp_mode)
    
    kwargs["parts"] = parts

    scad_help.make_parts(**kwargs)

    if kwargs["navigation"]:
        oobb_style = False  
        sort = scad_help.get_navigation_sort(oobb_style=oobb_style)
        scad_help.generate_navigation(sort=sort)

def get_parts(kwargs, oomp_mode):
    parts = []    

    #load parts from parts/folder/working.yaml
    parts_directory = os.path.join(os.path.dirname(__file__), "parts")
    if not os.path.isdir(parts_directory):
        return parts

    for folder in os.listdir(parts_directory):
        folder_path = os.path.join(parts_directory, folder)
        if not os.path.isdir(folder_path):
            continue

        working_yaml_path = os.path.join(folder_path, "working.yaml")
        if not os.path.isfile(working_yaml_path):
            continue

        with open(working_yaml_path, "r", encoding="utf-8") as infile:
            loaded_part = yaml.safe_load(infile)

        if not isinstance(loaded_part, dict):
            continue

        oobb_details = loaded_part.get("oobb_details")
        if not isinstance(oobb_details, dict):
            continue

        part = loaded_part

        part_kwargs = {}
        part_kwargs.update(copy.deepcopy(oobb_details))
        part_kwargs.update(copy.deepcopy(kwargs))
        # Build switches must beat defaults saved in the catalogue.
        part_kwargs.update(copy.deepcopy(kwargs))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = oobb_details.get("oobb_name", "bearing_holder")

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)


    return parts


def get_base(thing, **kwargs):
    get_bearing_holder(thing, **kwargs)


def get_bearing_holder_corner(thing, **kwargs):
    from working_corner import get_bearing_holder_corner as draw_corner
    draw_corner(thing, **kwargs)


def get_bearing_holder_90_degree(thing, **kwargs):
    p2 = copy.deepcopy(kwargs)
    p2["holder_type"] = "holder_90_degree"
    get_bearing_holder(thing, **p2)


def get_bearing_holder(thing, **kwargs):
    # Draw locally around z=0. Move / rotate the complete part only at the end.
    pos = copy.deepcopy(kwargs.get("pos", [0, 0, 0]))
    rot = copy.deepcopy(kwargs.get("rot", [0, 0, 0]))
    modes = kwargs.get("modes", ["3dpr", "true", "laser"])
    if "mode" in kwargs:
        modes = kwargs["mode"]
    if modes == "all":
        modes = ["3dpr", "true", "laser"]
    if isinstance(modes, str):
        modes = [modes]

    for mode in modes:
        p2 = copy.deepcopy(kwargs)
        p2["pos"] = [0, 0, 0]
        p2["rot"] = [0, 0, 0]
        p2["mode"] = mode
        p2["bearing_size"] = str(kwargs.get("bearing_size", "606"))
        p3 = {}
        p3["type"] = "bearing_holder"
        p3["width"] = p2.get("width", 3)
        p3["height"] = p2.get("height", 3)
        p3["depth"] = p2.get("depth", 12)
        local = oobb.get_default_thing(**p3)

        define_bearing_dimensions(**p2)
        p2["mounting_layout"] = get_mounting_layout(**p2)
        add_bearing_holder_body(local, **p2)
        add_bearing_features(local, **p2)
        add_perimeter_holes(local, **p2)
        add_joining_fasteners(local, **p2)

        if p2.get("holder_type", "holder") == "holder_90_degree":
            add_90_degree_extension(local, **p2)

        if kwargs.get("prepare_print", False) and mode == "3dpr":
            prepare_bearing_holder_print(local, **p2)

        # A group keeps each part's subtraction local to that part.
        group = {}
        group["type"] = "rotation"
        group["typetype"] = "positive"
        group["pos"] = pos
        group["rot"] = rot
        group["inclusion"] = mode
        group["objects"] = local["components"]
        thing["components"].append(group)
        thing["components_objects"].extend(local["components_objects"])
        thing["components_string"].extend(local["components_string"])


def get_bearing_centers(**kwargs):
    # Explicit positions use one-based OOBB grid coordinates.
    positions = kwargs.get("bearing_positions")
    if positions is None:
        return [[0, 0]]
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    pitch = oobb.gv("osp")
    return [[(x - (width + 1) / 2) * pitch,
             (y - (height + 1) / 2) * pitch] for x, y in positions]


def add_bearing_features(thing, **kwargs):
    for x, y in get_bearing_centers(**kwargs):
        local = oobb.get_default_thing(type="bearing_features")
        p2 = copy.deepcopy(kwargs)
        # Nut pockets are planned on the plate; draw each hub's pockets locally.
        p2["mounting_layout"]["nuts"] = []
        inner = oobb.gv(f"holder_bearing_{kwargs['bearing_size']}_id", kwargs["mode"])
        for nut in kwargs["mounting_layout"]["nuts"]:
            if math.hypot(nut["x"] - x, nut["y"] - y) < inner:
                translated = copy.deepcopy(nut)
                translated["x"] -= x
                translated["y"] -= y
                p2["mounting_layout"]["nuts"].append(translated)
        add_bearing_seat_and_relief(local, **p2)
        add_interior_holes(local, **p2)
        add_shaft_interface(local, **p2)
        oobb.shift(local["components"], [x, y, 0])
        oobb.shift(local["components_objects"], [x, y, 0])
        thing["components"].extend(local["components"])
        thing["components_objects"].extend(local["components_objects"])
        thing["components_string"].extend(local["components_string"])


def define_bearing_dimensions(**kwargs):
    # Project names preserve the saved v3 fits without changing global OOBB fits.
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    name = f"holder_bearing_{bearing_size}"
    dimensions = {}
    if "bearing_inner_diameter" in kwargs:
        # Catalogue dimensions for bearings not yet in the shared library.
        radius_inner = kwargs["bearing_inner_diameter"] / 2
        radius_outer = kwargs["bearing_outer_diameter"] / 2
        bearing_depth = kwargs["bearing_depth"]
        if mode == "3dpr":
            radius_outer += kwargs.get("bearing_print_radial_clearance", 0.2)
    else:
        radius_inner = oobb.gv(f"bearing_{bearing_size}_id", mode)
        radius_outer = oobb.gv(f"bearing_{bearing_size}_od", mode)
        bearing_depth = oobb.gv(f"bearing_{bearing_size}_depth", mode)
    clearance = 2

    if bearing_size == "606":
        clearance = 7
        if mode == "3dpr":
            radius_outer = 8.55
    if bearing_size == "6810":
        radius_inner = 25
        bearing_depth = 7

    # Relief between the inner rotating hub and the stationary outer holder.
    relief = (radius_outer - radius_inner - clearance / 2) / 2
    dimensions[f"{name}_id"] = radius_inner
    dimensions[f"{name}_od"] = radius_outer
    dimensions[f"{name}_depth"] = bearing_depth
    dimensions[f"{name}_relief_id"] = radius_inner + relief
    dimensions[f"{name}_relief_od"] = radius_outer - relief

    # Named interface dimensions. Unusual dimensions remain easy to edit here.
    dimensions["holder_bearing_adapter_radius"] = 12
    if bearing_size == "6705":
        # Keep the same lip beyond the larger inner race on round adapters.
        dimensions["holder_bearing_adapter_radius"] = 14.5
    if bearing_size == "6709":
        dimensions["holder_bearing_adapter_radius"] = 24.5
    dimensions["holder_bearing_servo_micro_radius_bottom"] = 2.5
    dimensions["holder_bearing_servo_micro_radius_top"] = 2.4
    dimensions["holder_bearing_servo_standard_radius_bottom"] = 2.9
    dimensions["holder_bearing_servo_standard_radius_top"] = 2.8
    dimensions["holder_bearing_building_block_radius"] = 3.55
    dimensions["holder_bearing_n20_radius"] = kwargs.get("shaft_radius", 0.95)
    if "centre_hole_diameter" in kwargs:
        # Literal requested bore diameter, with no extra fastener clearance.
        dimensions["holder_bearing_centre_hole_radius"] = kwargs["centre_hole_diameter"] / 2


    dimensions["holder_bearing_insert_radius"] = oobb.gv("threaded_insert_01_radius_m3", mode)
    if mode == "3dpr":
        dimensions["holder_bearing_insert_radius"] = 2.0

    # The current v5 cylinder expands all modes and reuses its first radius.
    # Each enclosing group here renders ONE mode, so give these project-only
    # names that mode's dimensions in all three slots before expanding it.
    # Standard OOBB variables are never overwritten.
    for variable_name, value in dimensions.items():
        for cylinder_mode in ["laser", "3dpr", "true"]:
            oobb.set_variable(variable_name, value, cylinder_mode)


def add_bearing_holder_body(thing, **kwargs):
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    depth = kwargs.get("depth", 12)
    mode = kwargs.get("mode", "3dpr")
    body = kwargs.get("body", "plate")

    p3 = {}
    p3["type"] = "positive"
    p3["shape"] = "oobb_plate"
    p3["width"] = width
    p3["height"] = height
    p3["depth"] = depth
    p3["extra_mm"] = True
    p3["holes"] = False
    p3["zz"] = "middle"
    p3["pos"] = [0, 0, 0]
    p3["mode"] = mode
    p3["inclusion"] = mode
    if kwargs.get("bearing_size") == "6804" and mode == "laser":
        p3["width"] = width + 0.25
        p3["height"] = height + 0.25
        p3["extra_mm"] = False
    if body == "cylinder":
        p3["shape"] = "oobb_cylinder"
        p3["radius_name"] = "holder_bearing_adapter_radius"
        p3["zz"] = "center"
    oobb.append_full(thing, **p3)


def add_bearing_seat_and_relief(thing, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    name = f"holder_bearing_{bearing_size}"
    depth = kwargs.get("depth", 12)
    bearing_depth = oobb.gv(f"{name}_depth", mode)

    positions = [0]
    if kwargs.get("shaft") == "motor_building_block_large_01":
        # This legacy adapter slides into the bearing from one side.
        positions = [0, -3, -6]

    for z in positions:
        p2 = copy.deepcopy(kwargs)
        p2["outer_radius_name"] = f"{name}_od"
        p2["inner_radius_name"] = f"{name}_id"
        p2["depth"] = bearing_depth
        p2["pos"] = [0, 0, z]
        add_annular_cutout(thing, **p2)

    p2 = copy.deepcopy(kwargs)
    p2["outer_radius_name"] = f"{name}_relief_od"
    p2["inner_radius_name"] = f"{name}_relief_id"
    p2["depth"] = depth + 30
    p2["pos"] = [0, 0, 0]
    add_annular_cutout(thing, **p2)


def add_annular_cutout(thing, **kwargs):
    # A negative group containing an outer cylinder minus an inner cylinder.
    # Keeping that inner cylinder in the group preserves the rotating hub.
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)
    local = oobb.get_default_thing(type="annular_cutout")

    p3 = {}
    p3["type"] = "positive"
    p3["shape"] = "oobb_cylinder"
    p3["radius_name"] = kwargs["outer_radius_name"]
    p3["depth"] = depth
    p3["zz"] = "center"
    p3["pos"] = [0, 0, 0]
    p3["mode"] = mode
    oobb.append_full(local, **p3)

    p3 = {}
    p3["type"] = "negative"
    p3["shape"] = "oobb_cylinder"
    p3["radius_name"] = kwargs["inner_radius_name"]
    p3["depth"] = depth + 0.02
    p3["zz"] = "center"
    p3["pos"] = [0, 0, 0]
    p3["mode"] = mode
    oobb.append_full(local, **p3)

    group = {}
    group["type"] = "rotation"
    group["typetype"] = "negative"
    group["pos"] = kwargs.get("pos", [0, 0, 0])
    group["rot"] = [0, 0, 0]
    group["inclusion"] = mode
    group["objects"] = local["components"]
    thing["components"].append(group)
    thing["components_objects"].extend(local["components_objects"])


def mounting_footprint(**kwargs):
    # These outlines only decide what fits. Every actual cut below is still
    # an OOBB primitive with a named radius.
    footprint = copy.deepcopy(kwargs)
    x = kwargs.get("x", 0)
    y = kwargs.get("y", 0)
    radius_name = kwargs.get("radius_name", "m3")
    dimension = "hole_radius_" + radius_name
    if kwargs.get("nut", False):
        dimension = "nut_radius_" + radius_name
    radius = kwargs.get("radius")
    if radius is None:
        radius = max(oobb.gv(dimension, mode) for mode in ["3dpr", "true", "laser"])
    footprint["radius"] = radius
    if kwargs.get("nut", False):
        angle = kwargs.get("rotation", 30)
        footprint["vertices"] = []
        for index in range(6):
            radians = math.radians(angle + index * 60)
            footprint["vertices"].append([
                x + radius * math.cos(radians),
                y + radius * math.sin(radians),
            ])
    return footprint


def mounting_point_edge_distance(point, a, b):
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    along = ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / (dx * dx + dy * dy)
    along = max(0, min(1, along))
    return math.hypot(point[0] - a[0] - along * dx, point[1] - a[1] - along * dy)


def mounting_gap(first, second):
    centres = math.hypot(first["x"] - second["x"], first["y"] - second["y"])
    round_gap = centres - first["radius"] - second["radius"]
    if round_gap > 0.3:
        return round_gap
    a = first.get("vertices")
    b = second.get("vertices")
    if a is None and b is None:
        return round_gap
    if a is None:
        return mounting_gap(second, first)
    edges_a = list(zip(a, a[1:] + a[:1]))
    if b is None:
        point = [second["x"], second["y"]]
        inside = all((end[0] - start[0]) * (point[1] - start[1]) -
                     (end[1] - start[1]) * (point[0] - start[0]) >= 0
                     for start, end in edges_a)
        distance = min(mounting_point_edge_distance(point, start, end) for start, end in edges_a)
        if inside:
            distance = -distance
        return distance - second["radius"]
    edges_b = list(zip(b, b[1:] + b[:1]))
    separated = False
    for start, end in edges_a + edges_b:
        normal = [start[1] - end[1], end[0] - start[0]]
        values_a = [v[0] * normal[0] + v[1] * normal[1] for v in a]
        values_b = [v[0] * normal[0] + v[1] * normal[1] for v in b]
        if max(values_a) < min(values_b) or max(values_b) < min(values_a):
            separated = True
    if not separated:
        return -1
    return min(
        [mounting_point_edge_distance(v, start, end) for v in a for start, end in edges_b] +
        [mounting_point_edge_distance(v, start, end) for v in b for start, end in edges_a]
    )


def mounting_region(footprint, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    inner = oobb.gv(f"holder_bearing_{bearing_size}_id", kwargs.get("mode", "3dpr"))
    inner *= math.cos(math.pi / 50)
    if "bearing_outer_diameter" in kwargs:
        outer = kwargs["bearing_outer_diameter"] / 2 + kwargs.get("bearing_print_radial_clearance", 0.2)
    else:
        outer = max(oobb.gv(f"bearing_{bearing_size}_od", mode) for mode in ["3dpr", "true", "laser"])
    if bearing_size == "606":
        outer = 8.55
    web = kwargs.get("mounting_minimum_web", 0.3)
    radius = footprint["radius"]
    distances = []
    for x, y in get_bearing_centers(**kwargs):
        distance = math.hypot(footprint["x"] - x, footprint["y"] - y)
        distances.append(distance)
        furthest = distance + radius
        if "vertices" in footprint:
            furthest = max(math.hypot(v[0] - x, v[1] - y) for v in footprint["vertices"])
        if furthest + web <= inner:
            return "inside"
    if kwargs.get("body", "plate") == "cylinder":
        return None
    if any(distance - radius < outer + web for distance in distances):
        return None
    if abs(footprint["x"]) + radius + web > kwargs.get("width", 3) * 7.5:
        return None
    if abs(footprint["y"]) + radius + web > kwargs.get("height", 3) * 7.5:
        return None
    return "perimeter"


def get_mounting_layout(**kwargs):
    # M6 on the 15 mm grid, M3 on the intervening 7.5 mm grid.
    # Fit in the tightest mode, so the same holes exist in every export.
    web = kwargs.get("mounting_minimum_web", 0.3)
    shaft = kwargs.get("shaft", "m6")
    inside = kwargs.get("inside", "")
    embedded = inside in ["embedded_m3_nuts", "embedded_m6_nuts"]
    nut_name = kwargs.get("embedded_nut_radius_name", "m3")
    joining = get_joining_positions(**kwargs)
    fixed = []
    shaft_radius = 3.25
    if shaft == "m5":
        shaft_radius = max(oobb.gv("hole_radius_m5", mode) for mode in ["3dpr", "true", "laser"])
    if shaft == "motor_gearmotor_01":
        shaft_radius = math.hypot(5.5, 3.85) / 2
    if shaft == "motor_servo_micro_01":
        shaft_radius = 2.5
    if shaft == "motor_servo_standard_01":
        shaft_radius = 2.9
    if shaft == "motor_building_block_large_01":
        shaft_radius = 3.55
    if shaft == "motor_n20":
        shaft_radius = kwargs.get("shaft_radius", 0.95)
    if shaft == "round_bore":
        shaft_radius = kwargs["centre_hole_diameter"] / 2
    fixed.append(mounting_footprint(x=0, y=0, radius=shaft_radius))
    if shaft not in ["m5", "m6", "round_bore"]:
        for x in [-7.5, 7.5]:
            fixed.append(mounting_footprint(x=x, y=0, radius=2.1))
    if shaft == "motor_servo_standard_01":
        for y in [-7.375, 7.375]:
            fixed.append(mounting_footprint(x=0, y=y, radius=2.5))
    if inside == "flange_coupler":
        for index in range(kwargs.get("coupler_mount_count", 4)):
            angle = kwargs.get("coupler_mount_rotation", 0) + index * 90
            radius = kwargs["coupler_bolt_circle_diameter"] / 2
            fixed.append(mounting_footprint(
                x=radius * math.cos(math.radians(angle)),
                y=radius * math.sin(math.radians(angle)),
                radius_name="m3",
                nut=True,
                rotation=angle + 30,
            ))
    for x, y in kwargs.get("interior_hole_positions", []):
        fixed.append(mounting_footprint(x=x, y=y, radius_name=kwargs.get("interior_radius_name", "m3")))
    centers = get_bearing_centers(**kwargs)
    fixed_local = fixed
    fixed = []
    for cx, cy in centers:
        for footprint in fixed_local:
            translated = copy.deepcopy(footprint)
            translated["x"] += cx
            translated["y"] += cy
            if "vertices" in translated:
                translated["vertices"] = [[x + cx, y + cy] for x, y in translated["vertices"]]
            fixed.append(translated)
    join_heads = []
    join_bores = []
    for screw in joining:
        radius = 3.6
        if screw["inner_joining"] and kwargs.get("inner_joining_head") == "socket_cap":
            # The opposite M3 nut is wider than the socket-cap recess.
            radius = max(3.0, oobb.gv("nut_radius_m3", "3dpr"))
        join_heads.append(mounting_footprint(x=screw["screw_x"], y=screw["screw_y"], radius=radius))
        join_bores.append(mounting_footprint(x=screw["screw_x"], y=screw["screw_y"], radius_name="m3"))
    if kwargs.get("holder_type") == "holder_90_degree":
        for x in [-7.5, 7.5]:
            fixed.append(mounting_footprint(x=x, y=-15, radius=3.6))
        # The transverse mounting holes and their loading pockets occupy
        # the lower extension. Its existing M6 connections are drawn there.
        for x in [-15, 0, 15]:
            fixed.append(mounting_footprint(x=x, y=-19.5, radius=6.5))
    nuts = []
    if embedded:
        # Keep the intended captive connections first. A requested pocket
        # that cannot fit becomes an ordinary grid hole below.
        for x, y in kwargs.get("embedded_nut_positions", []):
            rotation = kwargs.get("embedded_nut_rotation", 30)
            if kwargs.get("embedded_nut_rotation_radial", False):
                rotation += math.degrees(math.atan2(y, x))
            nut = mounting_footprint(x=x, y=y, radius_name=nut_name, nut=True, rotation=rotation)
            if mounting_region(nut, **kwargs) != "inside":
                continue
            if any(mounting_gap(nut, other) < web for other in fixed + join_bores + nuts):
                continue
            nuts.append(nut)
    holes = []
    omitted = []
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    for half_grid in [False, True]:
        for ix in range(2 * width - 1):
            for iy in range(2 * height - 1):
                is_half_grid = ix % 2 != 0 or iy % 2 != 0
                if is_half_grid != half_grid:
                    continue
                x = (ix - width + 1) * 7.5
                y = (iy - height + 1) * 7.5
                if [x, y] in centers:
                    continue  # Each shaft interface owns its centre.
                radius_name = "m3" if half_grid else "m6"
                # M3 captive versions keep M3 bolts at their main-grid nuts.
                if embedded and nut_name == "m3" and min(math.hypot(x - cx, y - cy) for cx, cy in centers) < oobb.gv(f"holder_bearing_{kwargs['bearing_size']}_id", kwargs.get("mode", "3dpr")):
                    radius_name = "m3"
                hole = mounting_footprint(x=x, y=y, radius_name=radius_name)
                region = mounting_region(hole, **kwargs)
                if region is None and radius_name == "m6":
                    # A smaller M3 hole is useful even where M6 cannot fit.
                    radius_name = "m3"
                    hole = mounting_footprint(x=x, y=y, radius_name=radius_name)
                    region = mounting_region(hole, **kwargs)
                if region is None:
                    continue
                other_nuts = [nut for nut in nuts if (nut["x"], nut["y"]) != (x, y)]
                obstacles = fixed + join_heads + other_nuts + holes
                if any(mounting_gap(hole, other) < web for other in obstacles):
                    omitted.append([x, y, radius_name])
                    continue
                hole["region"] = region
                holes.append(hole)
    if embedded:
        for hole in holes:
            if hole["region"] != "inside":
                continue
            x = hole["x"]
            y = hole["y"]
            if any((nut["x"], nut["y"]) == (x, y) for nut in nuts):
                continue
            other_holes = [other for other in holes if (other["x"], other["y"]) != (x, y)]
            for rotation_offset in [30, 0, 15, 45]:
                rotation = rotation_offset + math.degrees(math.atan2(y, x))
                nut = mounting_footprint(x=x, y=y, radius_name=hole["radius_name"], nut=True, rotation=rotation)
                if mounting_region(nut, **kwargs) != "inside":
                    continue
                if any(mounting_gap(nut, other) < web for other in fixed + join_bores + other_holes + nuts):
                    continue
                nuts.append(nut)
                break
    return {"holes": holes, "nuts": nuts, "joining": joining, "omitted": omitted}


def add_perimeter_holes(thing, **kwargs):
    # One complete grid covers both the outer frame and the rotating inside.
    depth = kwargs.get("depth", 12)
    mode = kwargs.get("mode", "3dpr")
    for hole in kwargs["mounting_layout"]["holes"]:
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = hole["radius_name"]
        p3["depth"] = depth + 2
        p3["pos"] = [hole["x"], hole["y"], -depth / 2 - 1]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)


def add_interior_holes(thing, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    shaft = kwargs.get("shaft", "m6")
    depth = kwargs.get("depth", 12)
    if kwargs.get("inside") == "flange_coupler":
        p2 = copy.deepcopy(kwargs)
        add_flange_coupler_connections(thing, **p2)
    elif kwargs.get("inside") in ["embedded_m3_nuts", "embedded_m6_nuts"]:
        p2 = copy.deepcopy(kwargs)
        add_embedded_nuts(thing, **p2)
    elif shaft not in ["m6", "round_bore"] and oobb.gv(f"holder_bearing_{bearing_size}_id", mode) * 2 > 15:
        # Retain the motor's insert holes; ordinary insides now use round
        # OOBB grid holes instead of the old two off-centre slots.
        for x in [-7.5, 7.5]:
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_cylinder"
            p3["radius_name"] = "holder_bearing_insert_radius"
            p3["depth"] = oobb.gv("threaded_insert_01_depth_m3", mode)
            p3["zz"] = "center"
            p3["pos"] = [x, 0, -p3["depth"] / 2]
            p3["mode"] = mode
            oobb.append_full(thing, **p3)

            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_hole"
            p3["radius_name"] = "m3"
            p3["depth"] = depth + 2
            p3["pos"] = [x, 0, -depth / 2 - 1]
            p3["mode"] = mode
            oobb.append_full(thing, **p3)

    # Optional extra interior holes: [[x_mm, y_mm], ...]. Put a name in extra
    # in working_populate when making a separate catalogue variant.
    for position in kwargs.get("interior_hole_positions", []):
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = kwargs.get("interior_radius_name", "m3")
        p3["pos"] = [position[0], position[1], -depth / 2 - 1]
        p3["depth"] = depth + 2
        p3["mode"] = mode
        oobb.append_full(thing, **p3)


def add_embedded_nuts(thing, **kwargs):
    # Fit captive nuts around the complete inside hole pattern.
    # Each hex opens onto BOTH split faces, trapping the nut on assembly.
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)
    split_z = kwargs.get("split_z", 0)
    for nut in kwargs["mounting_layout"]["nuts"]:
        position = [nut["x"], nut["y"]]
        radius_name = nut["radius_name"]
        nut_depth = oobb.gv(f"nut_depth_{radius_name}", mode)
        nut_rotation = nut["rotation"]
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = radius_name
        p3["depth"] = nut_depth
        p3["zz"] = "middle"
        p3["pos"] = [position[0], position[1], split_z]
        p3["rot"] = [0, 0, nut_rotation]
        p3["overhang"] = False
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = radius_name
        p3["depth"] = depth + 2
        p3["pos"] = [position[0], position[1], -depth / 2 - 1]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)


def add_flange_coupler_connections(thing, **kwargs):
    # OOMP mechanical_coupler_flange_name_5_mm_bore has a 16 mm bolt circle,
    # NOT a 16 mm square pattern. The metal flange sits on the hub's outer face.
    # Its barrel and grub screws remain outside the plastic and accessible.
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)
    split_z = kwargs.get("split_z", 0)
    bolt_radius = kwargs["coupler_bolt_circle_diameter"] / 2
    radius_name = kwargs["coupler_mount_radius_name"]
    count = kwargs["coupler_mount_count"]
    rotation = kwargs.get("coupler_mount_rotation", 0)

    for index in range(count):
        angle = rotation + index * 360 / count
        x = bolt_radius * math.cos(math.radians(angle))
        y = bolt_radius * math.sin(math.radians(angle))

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = radius_name
        p3["depth"] = depth + 2
        p3["pos"] = [x, y, -depth / 2 - 1]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = radius_name
        p3["depth"] = oobb.gv(f"nut_depth_{radius_name}", mode)
        p3["zz"] = "middle"
        p3["pos"] = [x, y, split_z]
        p3["rot"] = [0, 0, angle + 30]
        p3["overhang"] = False
        p3["mode"] = mode
        oobb.append_full(thing, **p3)


def get_joining_positions(**kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    shaft = kwargs.get("shaft", "m6")
    mode = kwargs.get("mode", "3dpr")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    if kwargs.get("horn_adapter") == "screws" or shaft == "motor_building_block_large_01":
        return []

    # The wider small-bearing plates extend the mounting grid while keeping
    # the frame clamps in the same positions as their 3 x 3 counterparts.
    if bearing_size in ["6704", "6705"] and (width, height) == (5, 3):
        width = height = 3

    # Put frame joining screws between mounting-grid rows, beyond the
    # outermost grid column. This frees the four M6 perimeter midpoints.
    x = width * 15 / 2 - 4
    y = height * 15 / 2 - 4
    between = 8
    if width == 5:
        between = 22.5
    positions = [
        [x, between, 0, 15],
        [-between, y, 180, 0],
        [-x, -between, 0, 15],
        [between, -y, 180, 0],
    ]
    if bearing_size == "6810":
        positions = [
            [x, 22.5, 0, 15],
            [-x, 22.5, 180, 0],
            [-x, -22.5, 0, 15],
            [x, -22.5, 180, 0],
        ]
    if kwargs.get("holder_type") == "holder_90_degree":
        positions = [[x, 8, 0, 15], [-x, 8, 180, 0]]
    if kwargs.get("body", "plate") == "cylinder":
        positions = []
    if shaft == "motor_gearmotor_01" and positions:
        positions[1][2] = 0
        positions[2][2] = 180
        positions[3][2] = 0

    outer_count = len(positions)
    inner_positions = []
    if bearing_size in ["6704", "6705", "6804"]:
        distance = kwargs.get("inner_joining_radius", 7.5)
        inner_positions.append([0, distance, 0, 0])
        inner_positions.append([0, -distance, 180, 0])
        if shaft in ["motor_gearmotor_01", "motor_servo_micro_01"] and mode == "3dpr":
            inner_positions.append([distance, 0, 0, 0])
            inner_positions.append([-distance, 0, 0, 0])

    if bearing_size == "6709" or (bearing_size == "6810" and kwargs.get("inside") in ["embedded_m3_nuts", "embedded_m6_nuts", "hole_30_mm"]):
        # 6709 joins sit beyond the 7.5 mm grid diagonals. On 6810 the
        # smaller joining circle frees the newly usable M6 corner holes.
        default_distance = 13 * math.sqrt(2)
        if bearing_size == "6810":
            default_distance = 7.5
        distance = kwargs.get("inner_joining_radius", default_distance)
        inner_positions.append([0, distance, 0, 0])
        inner_positions.append([0, -distance, 180, 0])
        if shaft in ["motor_gearmotor_01", "motor_servo_micro_01"] and mode == "3dpr":
            inner_positions.append([distance, 0, 0, 0])
            inner_positions.append([-distance, 0, 0, 0])

    # Default to diagonal inner joins; options can adjust angle and radius
    # to leave a large centre bore and useful grid positions unobstructed.
    angle_degrees = kwargs.get("inner_joining_rotation", 45)
    angle = math.radians(angle_degrees)
    for position in inner_positions:
        rotated_x = position[0] * math.cos(angle) - position[1] * math.sin(angle)
        rotated_y = position[0] * math.sin(angle) + position[1] * math.cos(angle)
        # add_joining_screw doubles this legacy nut_rotation parameter.
        positions.append([rotated_x, rotated_y, position[2], position[3] + angle_degrees / 2])

    if "inner_joining_positions" in kwargs:
        positions = positions[:outer_count]
        for index, position in enumerate(kwargs["inner_joining_positions"]):
            positions.append([position[0], position[1], (index % 2) * 180, 0])

    result = []
    for index, position in enumerate(positions):
        centers = get_bearing_centers(**kwargs) if index >= outer_count else [[0, 0]]
        for x, y in centers:
            p2 = {}
            p2["inner_joining"] = index >= outer_count
            p2["screw_x"] = position[0] + x
            p2["screw_y"] = position[1] + y
            p2["screw_face"] = position[2]
            p2["nut_rotation"] = position[3]
            result.append(p2)
    return result


def add_joining_fasteners(thing, **kwargs):
    for joining in kwargs["mounting_layout"]["joining"]:
        p2 = copy.deepcopy(kwargs)
        p2.update(joining)
        add_joining_screw(thing, **p2)


def add_joining_screw(thing, **kwargs):
    depth = kwargs.get("depth", 12)
    mode = kwargs.get("mode", "3dpr")
    face = kwargs.get("screw_face", 0)
    z = depth / 2
    if face == 180:
        z = -depth / 2

    grid_join = kwargs.get("inner_joining", False) and "inner_joining_positions" in kwargs
    inner_socket_cap = kwargs.get("inner_joining", False) and kwargs.get("inner_joining_head") == "socket_cap"
    if (mode == "laser" and kwargs.get("inner_joining", False) and not grid_join) or inner_socket_cap:
        # A long central hex standoff would collide with the captive nuts
        # in the small hubs. Use a bolt with head and nut in the OUTSIDE sheets.
        x = kwargs.get("screw_x", 0)
        y = kwargs.get("screw_y", 0)
        nut_depth = oobb.gv("nut_depth_m3", mode)
        head_radius_name = "screw_countersunk_radius_m3"
        head_depth = 3
        if inner_socket_cap:
            # Keep the smaller cap recess on the 6704 captive-labelled
            # variant, leaving more wall beside its standard-grid holes.
            head_radius_name = "screw_socket_cap_radius_m3"
            head_depth = oobb.gv("screw_socket_cap_height_m3", mode)
        head_z = depth / 2 - head_depth
        nut_z = -depth / 2
        if face == 180:
            head_z = -depth / 2
            nut_z = depth / 2 - nut_depth

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m3"
        p3["depth"] = depth + 2
        p3["pos"] = [x, y, -depth / 2 - 1]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = head_radius_name
        p3["depth"] = head_depth
        p3["pos"] = [x, y, head_z]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "m3"
        p3["depth"] = nut_depth
        p3["pos"] = [x, y, nut_z]
        p3["rot"] = [0, 0, kwargs.get("nut_rotation", 0) * 2]
        p3["overhang"] = False
        p3["mode"] = mode
        oobb.append_full(thing, **p3)
        return

    if mode == "laser" and not grid_join:
        # The laser sandwich uses round head pockets in the outer 3 mm sheets
        # and a hex standoff in the middle. A countersink cone is for printing.
        x = kwargs.get("screw_x", 0)
        y = kwargs.get("screw_y", 0)
        for pocket_z in [-depth / 2, depth / 2 - 3]:
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_hole"
            p3["radius_name"] = "screw_countersunk_radius_m3"
            p3["depth"] = 3
            p3["pos"] = [x, y, pocket_z]
            p3["mode"] = mode
            oobb.append_full(thing, **p3)

        # oobb_nut resolves nut_radius_<name>; this project-only alias uses
        # the OOBB standoff dimension and the existing hexagon primitive.
        oobb.set_variable("nut_radius_holder_bearing_standoff_m3", oobb.gv("standoff_radius_m3", mode), mode)
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "holder_bearing_standoff_m3"
        p3["depth"] = depth - 6
        p3["pos"] = [x, y, -depth / 2 + 3]
        p3["rot"] = [0, 0, kwargs.get("nut_rotation", 0) * 2]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)
        return

    p3 = {}
    p3["type"] = "negative"
    p3["shape"] = "oobb_screw_countersunk"
    p3["radius_name"] = "m3"
    p3["depth"] = depth
    p3["pos"] = [kwargs.get("screw_x", 0), kwargs.get("screw_y", 0), z]
    p3["rot"] = [0, face, 0]
    p3["rotation_nut"] = [0, 0, kwargs.get("nut_rotation", 0) * 2]
    p3["hole"] = True
    tight_nut = False
    if kwargs.get("shaft") in ["motor_gearmotor_01", "motor_servo_micro_01"]:
        if abs(kwargs.get("screw_x", 0)) == 7.5 and kwargs.get("screw_y", 0) == 0:
            tight_nut = True
    shallow_inner_nut = kwargs.get("inner_joining", False) and "joining_nut_depth" in kwargs
    p3["nut_include"] = not tight_nut and not shallow_inner_nut
    p3["overhang"] = True
    p3["mode"] = mode
    oobb.append_full(thing, **p3)

    if shallow_inner_nut:
        # Thin bearing sandwiches need the actual nut depth, rather than the
        # standard print-depth allowance entering the bearing's axial envelope.
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "m3"
        p3["depth"] = kwargs["joining_nut_depth"]
        p3["pos"] = [kwargs.get("screw_x", 0), kwargs.get("screw_y", 0),
                     depth / 2 if face == 180 else -depth / 2]
        p3["rot"] = [0, face, kwargs.get("nut_rotation", 0) * ( -2 if face == 180 else 2)]
        p3["overhang"] = True
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

    if tight_nut:
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "m3"
        p3["clearance_tightness"] = oobb.gv("nut_radius_m3_tight", mode) - oobb.gv("nut_radius_m3", mode)
        p3["pos"] = [kwargs.get("screw_x", 0), kwargs.get("screw_y", 0), -depth / 2]
        p3["overhang"] = True
        p3["mode"] = mode
        oobb.append_full(thing, **p3)


def add_shaft_interface(thing, **kwargs):
    shaft = kwargs.get("shaft", "m6")
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)

    if shaft in ["m5", "m6", "round_bore"]:
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = shaft
        if shaft == "round_bore":
            p3["radius_name"] = "holder_bearing_centre_hole_radius"
        p3["pos"] = [0, 0, -depth / 2 - 1]
        p3["depth"] = depth + 2
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

    elif shaft == "motor_gearmotor_01":
        # The saved gearmotor interface is rectangular, not a guessed D shaft.
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_cube_center"
        p3["size"] = [5.5, 3.85, depth + 2]
        p3["zz"] = "center"
        p3["pos"] = [0, 0, 0]
        p3["inclusion"] = mode
        oobb.append_full(thing, **p3)

    elif shaft in ["motor_servo_micro_01", "motor_servo_standard_01"]:
        p2 = copy.deepcopy(kwargs)
        add_servo_interface(thing, **p2)

    elif shaft == "motor_building_block_large_01":
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_cylinder"
        p3["radius_name"] = "holder_bearing_building_block_radius"
        p3["depth"] = 6.6
        p3["zz"] = "bottom"
        p3["pos"] = [0, 0, -depth / 2]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        for size in [[5, 3, depth + 2], [3, 5, depth + 2]]:
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_cube_center"
            p3["size"] = size
            p3["zz"] = "center"
            p3["pos"] = [0, 0, 0]
            p3["inclusion"] = mode
            oobb.append_full(thing, **p3)

    elif shaft == "motor_n20":
        # Saved SCAD has a 0.95 mm radius and no valid flat. Preserve that
        # geometry explicitly; shaft_radius / shaft_cut_depth are editable.
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_cylinder_d_shaft"
        p3["radius_name"] = "holder_bearing_n20_radius"
        p3["cut_d"] = kwargs.get("shaft_cut_depth", 0)
        p3["depth"] = depth + 2
        p3["zz"] = "center"
        p3["pos"] = [0, 0, 0]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

    else:
        raise ValueError(f"Unknown shaft interface: {shaft}")


def add_servo_interface(thing, **kwargs):
    shaft = kwargs.get("shaft")
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)
    name = "holder_bearing_servo_micro"
    horn_depth = 3
    screw_radius_name = "m2"
    if shaft == "motor_servo_standard_01":
        name = "holder_bearing_servo_standard"
        horn_depth = 4
        screw_radius_name = "m2d5"

    p3 = {}
    p3["type"] = "negative"
    p3["shape"] = "oobb_cylinder"
    p3["radius_1"] = oobb.gv(f"{name}_radius_bottom", mode)
    p3["radius_2"] = oobb.gv(f"{name}_radius_top", mode)
    p3["depth"] = horn_depth
    p3["zz"] = "bottom"
    p3["pos"] = [0, 0, -depth / 2]
    p3["mode"] = mode
    oobb.append_full(thing, **p3)

    p3 = {}
    p3["type"] = "negative"
    p3["shape"] = "oobb_hole"
    p3["radius_name"] = screw_radius_name
    p3["depth"] = depth + 2
    p3["pos"] = [0, 0, -depth / 2 - 1]
    p3["mode"] = mode
    oobb.append_full(thing, **p3)

    if shaft == "motor_servo_standard_01":
        for y in [-7.375, 7.375]:
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_screw_self_tapping"
            p3["radius_name"] = "m2"
            p3["depth"] = depth
            p3["pos"] = [0, y, -depth / 2]
            p3["rot"] = [0, 180, 0]
            p3["zz"] = "top"
            p3["loose"] = ["screw"]
            p3["overhang"] = True
            p3["mode"] = mode
            oobb.append_full(thing, **p3)


def add_90_degree_extension(thing, **kwargs):
    width = kwargs.get("width", 3)
    depth = kwargs.get("depth", 12)
    mode = kwargs.get("mode", "3dpr")
    basic = kwargs.get("extra", "") == "basic"
    spacing = oobb.gv("osp")
    extension_depth = 13.5
    extension_y = -28.5

    p3 = {}
    p3["type"] = "positive"
    p3["shape"] = "oobb_plate"
    p3["width"] = width
    p3["height"] = 1
    p3["depth"] = depth
    p3["zz"] = "middle"
    p3["pos"] = [0, -15, 0]
    p3["holes"] = False
    p3["inclusion"] = mode
    oobb.append_full(thing, **p3)

    p3 = {}
    p3["type"] = "positive"
    p3["shape"] = "oobb_cube_center"
    p3["size"] = [width * spacing - 1, extension_depth, depth]
    p3["zz"] = "middle"
    p3["pos"] = [0, extension_y + extension_depth / 2, 0]
    p3["inclusion"] = mode
    oobb.append_full(thing, **p3)

    for index in range(width):
        x = -(width - 1) * spacing / 2 + index * spacing
        # Vertical mounting-strip holes, followed by the transverse holes.
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m6"
        p3["depth"] = depth + 2
        p3["pos"] = [x, -15, -depth / 2 - 1]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = "m6"
        p3["depth"] = extension_depth
        p3["pos"] = [x, -15, 0]
        p3["rot"] = [90, 0, 0]
        p3["mode"] = mode
        oobb.append_full(thing, **p3)

        if not basic:
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_nut"
            p3["radius_name"] = "loose_m6"
            p3["pos"] = [x, -19.5, 0]
            # Saved v3 SCAD rotates this hex twice by 90 degrees. Preserve
            # its downward nut pocket explicitly, rather than silently
            # changing the pocket into a horizontal hex tunnel.
            p3["rot"] = [180, 0, 0]
            p3["overhang"] = False
            p3["mode"] = mode
            oobb.append_full(thing, **p3)
        else:
            # Basic means an open nut loading slot, not a closed hex pocket.
            nut_width = oobb.gv("nut_radius_loose_m6", mode) * 2 / 1.154
            nut_depth = oobb.gv("nut_depth_loose_m6", mode)
            p3 = {}
            p3["type"] = "negative"
            p3["shape"] = "oobb_cube_center"
            p3["size"] = [nut_width, nut_depth, depth + 2]
            p3["zz"] = "center"
            p3["pos"] = [x, -19.5 - nut_depth / 2, 0]
            p3["inclusion"] = mode
            oobb.append_full(thing, **p3)

    for index in range(width - 1):
        x = -(width - 2) * spacing / 2 + index * spacing
        p2 = copy.deepcopy(kwargs)
        p2["screw_x"] = x
        p2["screw_y"] = -15
        p2["screw_face"] = (index % 2) * 180
        p2["nut_rotation"] = 0
        add_joining_screw(thing, **p2)


def prepare_bearing_holder_print(thing, **kwargs):
    depth = kwargs.get("depth", 12)
    width = kwargs.get("width", 3)
    mode = kwargs.get("mode", "3dpr")
    split_z = kwargs.get("split_z", 0)
    gap = kwargs.get("print_gap", 10)
    split = kwargs.get("split", True)
    if depth <= 0 or gap <= 0:
        raise ValueError("Depth and print_gap must be positive")
    if split and not -depth / 2 < split_z < depth / 2:
        raise ValueError("split_z must be inside the assembled thickness")

    original = copy.deepcopy(thing["components"])
    thing["components"] = []

    if not split:
        group = {}
        group["type"] = "rotation"
        group["typetype"] = "positive"
        group["pos"] = [0, 0, depth / 2]
        group["rot"] = [0, 0, 0]
        group["inclusion"] = mode
        group["objects"] = original
        thing["components"].append(group)
        return

    span = width * oobb.gv("osp")
    if kwargs.get("body", "plate") == "cylinder":
        span = 2 * oobb.gv("holder_bearing_adapter_radius", mode)
    distance = span + gap

    # Lower half: subtract everything ABOVE the cut plane, then place its
    # original outer face on the bed. Upper half: subtract everything BELOW,
    # turn it over, and place its outer face on the bed. These are NOT copies
    # of one half: asymmetric shaft holes and nut pockets remain complementary.
    for half in ["lower", "upper"]:
        local = oobb.get_default_thing(type="print_half")
        local["components"] = copy.deepcopy(original)
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_slice"
        p3["size"] = [500, 500, 500]
        p3["pos"] = [-250, -250, split_z]
        p3["zz"] = "bottom"
        p3["mode"] = mode
        p3["inclusion"] = mode
        if half == "upper":
            p3["zz"] = "top"
        oobb.append_full(local, **p3)

        group = {}
        group["type"] = "rotation"
        group["typetype"] = "positive"
        group["pos"] = [0, 0, depth / 2]
        group["rot"] = [0, 0, 0]
        group["inclusion"] = mode
        group["objects"] = local["components"]
        if half == "upper":
            group["pos"] = [distance, 0, depth / 2]
            group["rot"] = [180, 0, 0]
        thing["components"].append(group)


if __name__ == "__main__":
    main()
