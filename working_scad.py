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
        # Build switches must beat defaults saved in the catalogue.
        part_kwargs.update(copy.deepcopy(kwargs))
        part["kwargs"] = part_kwargs
        part["oobb_name"] = oobb_details.get("oobb_name", "bearing_plate")

        if oomp_mode == "oobb":
            part["kwargs"]["oomp_size"] = part["oobb_name"]

        parts.append(part)


    return parts


def get_base(thing, **kwargs):
    get_bearing_plate(thing, **kwargs)


def get_bearing_plate_90_degree(thing, **kwargs):
    p2 = copy.deepcopy(kwargs)
    p2["plate_type"] = "plate_90_degree"
    get_bearing_plate(thing, **p2)


def get_bearing_plate(thing, **kwargs):
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
        p3["type"] = "bearing_plate"
        p3["width"] = p2.get("width", 3)
        p3["height"] = p2.get("height", 3)
        p3["depth"] = p2.get("depth", 12)
        local = oobb.get_default_thing(**p3)

        define_bearing_dimensions(**p2)
        add_bearing_plate_body(local, **p2)
        add_bearing_seat_and_relief(local, **p2)
        add_perimeter_holes(local, **p2)
        add_interior_holes(local, **p2)
        add_joining_fasteners(local, **p2)
        add_shaft_interface(local, **p2)

        if p2.get("plate_type", "plate") == "plate_90_degree":
            add_90_degree_extension(local, **p2)

        if kwargs.get("prepare_print", False) and mode == "3dpr":
            prepare_bearing_plate_print(local, **p2)

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


def define_bearing_dimensions(**kwargs):
    # Project names preserve the saved v3 fits without changing global OOBB fits.
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    name = f"plate_bearing_{bearing_size}"
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

    # Relief between the inner rotating hub and the stationary outer plate.
    relief = (radius_outer - radius_inner - clearance / 2) / 2
    dimensions[f"{name}_id"] = radius_inner
    dimensions[f"{name}_od"] = radius_outer
    dimensions[f"{name}_depth"] = bearing_depth
    dimensions[f"{name}_relief_id"] = radius_inner + relief
    dimensions[f"{name}_relief_od"] = radius_outer - relief

    # Named interface dimensions. Unusual dimensions remain easy to edit here.
    dimensions["plate_bearing_adapter_radius"] = 12
    if bearing_size == "6705":
        # Keep the same lip beyond the larger inner race on round adapters.
        dimensions["plate_bearing_adapter_radius"] = 14.5
    if bearing_size == "6709":
        dimensions["plate_bearing_adapter_radius"] = 24.5
    dimensions["plate_bearing_servo_micro_radius_bottom"] = 2.5
    dimensions["plate_bearing_servo_micro_radius_top"] = 2.4
    dimensions["plate_bearing_servo_standard_radius_bottom"] = 2.9
    dimensions["plate_bearing_servo_standard_radius_top"] = 2.8
    dimensions["plate_bearing_building_block_radius"] = 3.55
    dimensions["plate_bearing_n20_radius"] = kwargs.get("shaft_radius", 0.95)


    dimensions["plate_bearing_insert_radius"] = oobb.gv("threaded_insert_01_radius_m3", mode)
    if mode == "3dpr":
        dimensions["plate_bearing_insert_radius"] = 2.0

    # The current v5 cylinder expands all modes and reuses its first radius.
    # Each enclosing group here renders ONE mode, so give these project-only
    # names that mode's dimensions in all three slots before expanding it.
    # Standard OOBB variables are never overwritten.
    for variable_name, value in dimensions.items():
        for cylinder_mode in ["laser", "3dpr", "true"]:
            oobb.set_variable(variable_name, value, cylinder_mode)


def add_bearing_plate_body(thing, **kwargs):
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
        p3["radius_name"] = "plate_bearing_adapter_radius"
        p3["zz"] = "center"
    oobb.append_full(thing, **p3)


def add_bearing_seat_and_relief(thing, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    name = f"plate_bearing_{bearing_size}"
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


def add_perimeter_holes(thing, **kwargs):
    mode = kwargs.get("mode", "3dpr")
    bearing_size = kwargs.get("bearing_size", "606")

    p3 = {}
    p3["type"] = "negative"
    p3["shape"] = "oobb_holes"
    p3["width"] = kwargs.get("width", 3)
    p3["height"] = kwargs.get("height", 3)
    p3["holes"] = "perimeter_miss_middle"
    p3["radius_name"] = "m6"
    p3["mode"] = mode
    p3["inclusion"] = mode
    if bearing_size == "6810":
        p3["holes"] = ["top", "bottom"]
        p3["pos"] = [0, 0, -kwargs.get("depth", 12) / 2 - 1]
        p3["depth"] = kwargs.get("depth", 12) + 2
    oobb.append_full(thing, **p3)

    if bearing_size == "6810":
        p3["width"] = 5
        p3["height"] = 5
        p3["holes"] = "corners"
        oobb.append_full(thing, **p3)


def add_interior_holes(thing, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    mode = kwargs.get("mode", "3dpr")
    shaft = kwargs.get("shaft", "m6")
    depth = kwargs.get("depth", 12)
    inner_grid = kwargs.get("interior_grid")
    if inner_grid is None:
        inner_grid = oobb.gv(f"bearing_{bearing_size}_inner_holes", "true")

    if inner_grid > 1:
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_holes"
        p3["width"] = inner_grid
        p3["height"] = inner_grid
        p3["holes"] = "circle"
        p3["circle_dif"] = 5
        p3["middle"] = False
        p3["radius_name"] = "m6"
        p3["mode"] = mode
        p3["inclusion"] = mode
        oobb.append_full(thing, **p3)

    if kwargs.get("inside") == "flange_coupler":
        p2 = copy.deepcopy(kwargs)
        add_flange_coupler_connections(thing, **p2)
    elif kwargs.get("inside") in ["embedded_m3_nuts", "embedded_m6_nuts"]:
        p2 = copy.deepcopy(kwargs)
        add_embedded_nuts(thing, **p2)
    elif oobb.gv(f"plate_bearing_{bearing_size}_id", mode) * 2 > 15:
        if shaft == "m6":
            for x in [-7.75, 7.75]:
                # Named M3 holes hulled 0.5 mm apart form the legacy slot.
                # Use component groups because v5 oobb_slot's named-radius
                # branch currently refers to an undefined `ob` variable.
                local = oobb.get_default_thing(type="interior_slot")
                for end_x in [-0.25, 0.25]:
                    p3 = {}
                    p3["type"] = "positive"
                    p3["shape"] = "oobb_hole"
                    p3["radius_name"] = "m3"
                    p3["depth"] = depth + 2
                    p3["pos"] = [end_x, 0, -depth / 2 - 1]
                    p3["mode"] = mode
                    oobb.append_full(local, **p3)
                group = {}
                group["type"] = "hull"
                group["typetype"] = "negative"
                group["pos"] = [x, 0, 0]
                group["rot"] = [0, 0, 0]
                group["inclusion"] = mode
                group["objects"] = local["components"]
                thing["components"].append(group)
        else:
            for x in [-7.5, 7.5]:
                p3 = {}
                p3["type"] = "negative"
                p3["shape"] = "oobb_cylinder"
                p3["radius_name"] = "plate_bearing_insert_radius"
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
    # Replace the usual two interior slots with captive nuts and bolt holes.
    # Each hex opens onto BOTH split faces, trapping the nut on assembly.
    mode = kwargs.get("mode", "3dpr")
    depth = kwargs.get("depth", 12)
    split_z = kwargs.get("split_z", 0)
    radius_name = kwargs.get("embedded_nut_radius_name", "m3")
    nut_depth = oobb.gv(f"nut_depth_{radius_name}", mode)

    for position in kwargs.get("embedded_nut_positions", []):
        nut_rotation = kwargs.get("embedded_nut_rotation", 30)
        if kwargs.get("embedded_nut_rotation_radial", False):
            nut_rotation += math.degrees(math.atan2(position[1], position[0]))
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


def add_joining_fasteners(thing, **kwargs):
    bearing_size = kwargs.get("bearing_size", "606")
    shaft = kwargs.get("shaft", "m6")
    mode = kwargs.get("mode", "3dpr")
    width = kwargs.get("width", 3)
    height = kwargs.get("height", 3)
    if kwargs.get("horn_adapter") == "screws" or shaft == "motor_building_block_large_01":
        return

    x = (width - 1) * oobb.gv("osp") / 2
    y = (height - 1) * oobb.gv("osp") / 2
    offset = 0
    if bearing_size == "6803":
        offset = 2
    if bearing_size in ["6704", "6705", "6804"]:
        offset = 3
    if bearing_size == "6804" and mode == "3dpr":
        # At exactly 18 mm the M3 hole touches the 16.2 mm bearing recess
        # along one edge, producing a non-manifold STL. Move it outward by
        # 0.01 mm, leaving the bearing fit and named screw radius unchanged.
        offset += kwargs.get("joining_tangent_clearance", 0.01)

    # x, y, screw-face rotation, nut rotation. Keep the order visible here.
    positions = []
    positions.append([x + offset, 0, 0, 15])
    positions.append([0, -y - offset, 180, 0])
    positions.append([-x - offset, 0, 0, 15])
    positions.append([0, y + offset, 180, 0])
    if bearing_size == "6810":
        positions = []
        positions.append([x - 15, -22, 0, 15])
        positions.append([-22, -y, 180, 0])
        positions.append([-x + 15, 22, 0, 15])
        positions.append([22, y, 180, 0])
    if shaft == "motor_gearmotor_01":
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

    if bearing_size == "6709" or (bearing_size == "6810" and kwargs.get("inside") in ["embedded_m3_nuts", "embedded_m6_nuts"]):
        distance = kwargs.get("inner_joining_radius", 15)
        inner_positions.append([0, distance, 0, 0])
        inner_positions.append([0, -distance, 180, 0])
        if shaft in ["motor_gearmotor_01", "motor_servo_micro_01"] and mode == "3dpr":
            inner_positions.append([distance, 0, 0, 0])
            inner_positions.append([-distance, 0, 0, 0])

    # All inner joining screws move onto diagonals; motor interfaces and
    # outer-frame mounting screws keep their original coordinates.
    angle_degrees = kwargs.get("inner_joining_rotation", 45)
    angle = math.radians(angle_degrees)
    for position in inner_positions:
        rotated_x = position[0] * math.cos(angle) - position[1] * math.sin(angle)
        rotated_y = position[0] * math.sin(angle) + position[1] * math.cos(angle)
        # add_joining_screw doubles this legacy nut_rotation parameter.
        positions.append([rotated_x, rotated_y, position[2], position[3] + angle_degrees / 2])

    for index, position in enumerate(positions):
        p2 = copy.deepcopy(kwargs)
        p2["inner_joining"] = index >= outer_count
        p2["screw_x"] = position[0]
        p2["screw_y"] = position[1]
        p2["screw_face"] = position[2]
        p2["nut_rotation"] = position[3]
        add_joining_screw(thing, **p2)


def add_joining_screw(thing, **kwargs):
    depth = kwargs.get("depth", 12)
    mode = kwargs.get("mode", "3dpr")
    face = kwargs.get("screw_face", 0)
    z = depth / 2
    if face == 180:
        z = -depth / 2

    inner_socket_cap = kwargs.get("inner_joining", False) and kwargs.get("inner_joining_head") == "socket_cap"
    if (mode == "laser" and kwargs.get("inner_joining", False)) or inner_socket_cap:
        # A long central hex standoff would collide with the captive nuts
        # in the small hubs. Use a bolt with head and nut in the OUTSIDE sheets.
        x = kwargs.get("screw_x", 0)
        y = kwargs.get("screw_y", 0)
        nut_depth = oobb.gv("nut_depth_m3", mode)
        head_radius_name = "screw_countersunk_radius_m3"
        head_depth = 3
        if inner_socket_cap:
            # The smaller cap recess leaves a wall beside all four captive
            # nuts in the experimental 6704, unlike a wide countersink.
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

    if mode == "laser":
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
        oobb.set_variable("nut_radius_plate_bearing_standoff_m3", oobb.gv("standoff_radius_m3", mode), mode)
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_nut"
        p3["radius_name"] = "plate_bearing_standoff_m3"
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
    p3["nut_include"] = not tight_nut
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

    if shaft in ["m5", "m6"]:
        p3 = {}
        p3["type"] = "negative"
        p3["shape"] = "oobb_hole"
        p3["radius_name"] = shaft
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
        p3["radius_name"] = "plate_bearing_building_block_radius"
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
        p3["radius_name"] = "plate_bearing_n20_radius"
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
    name = "plate_bearing_servo_micro"
    horn_depth = 3
    screw_radius_name = "m2"
    if shaft == "motor_servo_standard_01":
        name = "plate_bearing_servo_standard"
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


def prepare_bearing_plate_print(thing, **kwargs):
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
        span = 2 * oobb.gv("plate_bearing_adapter_radius", mode)
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
