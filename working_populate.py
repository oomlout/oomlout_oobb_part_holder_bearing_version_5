import copy

from oomp_populate_helper import build_oomp_id, write_extras


def main(**kwargs):
    options = get_options(**kwargs)

    import working_oomp_populate_extra_detail
    working_oomp_populate_extra_detail.main(extras=options)

    write_extras(options)
    return options


def get_options(**kwargs):
    # Width / height are grid units. Depth is the ASSEMBLED thickness in mm.
    # Individual definitions so each variant can be edited independently.
    options = []

    option = {}
    option["bearing_size"] = '606'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_606'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 5
    option["height"] = 3
    option["depth"] = 9
    option["extra"] = ''
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 9
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6803'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6803'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6804'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6804'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6808'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_05_05_12_6808'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = ''
    option["legacy_id"] = 'oobb_bearing_plate_07_05_12_6810'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 15
    option["extra"] = ''
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_gearmotor_01'
    option["shaft"] = 'motor_gearmotor_01'
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_sh_motor_gearmotor_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_micro_01'
    option["shaft"] = 'motor_servo_micro_01'
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_sh_motor_servo_micro_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_printed'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'printed'
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_ex_horn_adapter_printed_sh_motor_servo_standard_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_screws'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'screws'
    option["body"] = 'cylinder'
    option["split_z"] = 0.5
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_ex_horn_adapter_screws_sh_motor_servo_standard_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_building_block_large_01'
    option["shaft"] = 'motor_building_block_large_01'
    option["body"] = 'cylinder'
    option["split"] = False
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_sh_motor_building_block_large_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_n20'
    option["shaft"] = 'motor_n20'
    option["body"] = 'cylinder'
    option["shaft_radius"] = 0.95
    option["shaft_cut_depth"] = 0
    option["migration_note"] = 'Saved N20 SCAD has r=0.95 and an impossible negative-depth flat. Preserve its actual circular hole; physical shaft fit unverified.'
    option["legacy_id"] = 'oobb_bearing_plate_03_03_12_6704_sh_motor_n20'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '606'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["holder_type"] = 'holder_90_degree'
    option["legacy_id"] = 'oobb_bearing_plate_jack_03_03_12_606'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '606'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'basic'
    option["holder_type"] = 'holder_90_degree'
    option["legacy_id"] = 'oobb_bearing_plate_jack_basic_03_03_12_606'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m3_nuts'
    option["inside"] = 'embedded_m3_nuts'
    option["embedded_nut_positions"] = [
        [-7.5, 0],
        [7.5, 0],
        [0, -7.5],
        [0, 7.5],
    ]
    option["inner_joining_head"] = 'socket_cap'
    option["embedded_nut_rotation"] = 30
    option["embedded_nut_rotation_radial"] = True
    option["experimental"] = True
    option["design_note"] = 'Standard 15 mm hole spacing. M3 nut pockets do not fit the 6704 inner race at these positions; retain plain M3 holes instead.'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 5
    option["height"] = 3
    option["depth"] = 9
    option["extra"] = ''
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m3_nuts'
    option["inside"] = 'embedded_m3_nuts'
    option["embedded_nut_positions"] = [
        [-7.5, 0],
        [7.5, 0],
        [0, -7.5],
        [0, 7.5],
    ]
    option["embedded_nut_rotation"] = 30
    option["embedded_nut_rotation_radial"] = True
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_building_block_large_01'
    option["shaft"] = 'motor_building_block_large_01'
    option["body"] = 'cylinder'
    option["split"] = False
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_gearmotor_01'
    option["shaft"] = 'motor_gearmotor_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_n20'
    option["shaft"] = 'motor_n20'
    option["body"] = 'cylinder'
    option["shaft_radius"] = 0.95
    option["shaft_cut_depth"] = 0
    option["design_note"] = 'Uses the migrated 6704 circular N20 opening. Physical shaft fit unverified.'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_micro_01'
    option["shaft"] = 'motor_servo_micro_01'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_printed'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'printed'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6705'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_screws'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'screws'
    option["body"] = 'cylinder'
    option["split_z"] = 0.5
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = ''
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m3_nuts'
    option["inside"] = 'embedded_m3_nuts'
    option["embedded_nut_radius_name"] = 'm3'
    option["embedded_nut_positions"] = [
        [-15, 0],
        [15, 0],
        [0, -15],
        [0, 15],
    ]
    option["embedded_nut_rotation_radial"] = True
    option["embedded_nut_rotation"] = 30
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m6_nuts'
    option["inside"] = 'embedded_m6_nuts'
    option["embedded_nut_radius_name"] = 'm6'
    option["embedded_nut_positions"] = [
        [-15, 0],
        [15, 0],
        [0, -15],
        [0, 15],
    ]
    option["embedded_nut_rotation_radial"] = True
    option["embedded_nut_rotation"] = 30
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_mechanical_coupler_flange_name_5_mm_bore'
    option["shaft"] = 'm5'
    option["inside"] = 'flange_coupler'
    option["coupler_oomp_id"] = 'mechanical_coupler_flange_name_5_mm_bore'
    option["coupler_source"] = 'C:/od/OneDrive/docs/oomp_mechanical_coupler/source_file/dimension/flange/dimension.csv'
    option["coupler_bore"] = 5
    option["coupler_flange_diameter"] = 22
    option["coupler_flange_depth"] = 2
    option["coupler_bolt_circle_diameter"] = 16
    option["coupler_mount_count"] = 4
    option["coupler_mount_radius_name"] = 'm3'
    option["coupler_mount_rotation"] = 0
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_building_block_large_01'
    option["shaft"] = 'motor_building_block_large_01'
    option["body"] = 'cylinder'
    option["split"] = False
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_gearmotor_01'
    option["shaft"] = 'motor_gearmotor_01'
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_n20'
    option["shaft"] = 'motor_n20'
    option["body"] = 'cylinder'
    option["shaft_radius"] = 0.95
    option["shaft_cut_depth"] = 0
    option["design_note"] = 'Uses the migrated 6704 circular N20 opening. Physical shaft fit unverified.'
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_servo_micro_01'
    option["shaft"] = 'motor_servo_micro_01'
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_printed'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'printed'
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6709'
    option["width"] = 5
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'motor_servo_standard_01_horn_adapter_screws'
    option["shaft"] = 'motor_servo_standard_01'
    option["horn_adapter"] = 'screws'
    option["body"] = 'cylinder'
    option["split_z"] = 0.5
    option["bearing_inner_diameter"] = 45
    option["bearing_outer_diameter"] = 55
    option["bearing_depth"] = 6
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.cxnjs.com/content/150.html'
    options.append(copy.deepcopy(option))

    # Standard 608: 8 mm bore, 22 mm outside diameter, 7 mm bearing width.
    option = {}
    option["bearing_size"] = '608'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = ''
    option["bearing_inner_diameter"] = 8
    option["bearing_outer_diameter"] = 22
    option["bearing_depth"] = 7
    option["bearing_print_radial_clearance"] = 0.2
    option["bearing_dimension_source"] = 'https://www.emarketplace.in.skf.com/industrial/bearings?search=608-RSH'
    options.append(copy.deepcopy(option))

    # Reuse the existing 6810 7 x 5 outline; only add captive-nut insides.
    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m3_nuts'
    option["inside"] = 'embedded_m3_nuts'
    option["embedded_nut_radius_name"] = 'm3'
    option["embedded_nut_positions"] = [
        [-15, 0],
        [15, 0],
        [0, -15],
        [0, 15],
        [-15, -15],
        [-15, 15],
        [15, -15],
        [15, 15],
    ]
    option["embedded_nut_rotation"] = 30
    option["embedded_nut_rotation_radial"] = True
    option["inner_joining_rotation"] = 45
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_embedded_m6_nuts'
    option["inside"] = 'embedded_m6_nuts'
    option["embedded_nut_radius_name"] = 'm6'
    option["embedded_nut_positions"] = [
        [-15, 0],
        [15, 0],
        [0, -15],
        [0, 15],
    ]
    option["embedded_nut_rotation"] = 30
    option["embedded_nut_rotation_radial"] = True
    option["inner_joining_rotation"] = 45
    options.append(copy.deepcopy(option))

    # 6810 centre ring: 30 mm bore, with the four 3 x 3 M6 corners.
    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'inside_hole_30_mm'
    option["inside"] = 'hole_30_mm'
    option["shaft"] = 'round_bore'
    option["centre_hole_diameter"] = 30
    # Move the M3 joins 1.5 mm inward from the half-grid positions.
    # Full-depth nuts now clear the bearing inside and sit flush.
    option["inner_joining_positions"] = [[0, 21], [0, -21]]
    options.append(copy.deepcopy(option))

    # Two 6704 bearings, three OOBB pitches apart on the middle row.
    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 8
    option["height"] = 3
    option["depth"] = 9
    option["extra"] = 'double'
    option["bearing_positions"] = [[3, 2], [6, 2]]
    options.append(copy.deepcopy(option))

    # Both outer bearing retainers belong to each continuous corner half.
    option = {}
    option["bearing_size"] = '6810'
    option["width"] = 7
    option["height"] = 5
    option["depth"] = 12
    option["extra"] = 'corner_bevel_50_teeth'
    option["holder_type"] = 'holder_90_degree'
    option["corner"] = {
        "bearing_inner_diameter": 50,
        "bearing_outer_diameter": 65,
        "bearing_depth": 7,
        "radial_clearance": 0.15,
        "axial_clearance": 0.2,
        "split_gap": 0.2,
        "joining_screw_length": 25,
        "gear_teeth": 50,
        "gear_module": 1.5,
        "gear_depth": 12,
        "gear_face_width": 6,
        "gear_backlash": 0.2,
        "minimum_gear_gap": 1,
        "mounting_row": 45,
        "gear_repo": "../oomlout_oobb_gear_version_5",
    }
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '6704'
    option["width"] = 5
    option["height"] = 3
    option["depth"] = 9
    option["extra"] = 'corner_bevel_30_teeth'
    option["holder_type"] = 'holder_90_degree'
    option["corner"] = {
        "bearing_inner_diameter": 20,
        "bearing_outer_diameter": 27,
        "bearing_depth": 4,
        "radial_clearance": 0.15,
        "axial_clearance": 0.2,
        "split_gap": 0.2,
        "joining_screw_length": 25,
        "axis_pitch": 7.5,
        "hub_nut_depth": 2.4,
        "gear_teeth": 30,
        "gear_module": 1.5,
        "gear_depth": 12,
        "gear_face_width": 6,
        "gear_backlash": 0.2,
        "minimum_gear_gap": 1,
        "mounting_row": 30,
        "gear_mounts": [[-7.5, 0], [7.5, 0], [0, -7.5], [0, 7.5]],
        "gear_mount_radius_name": "m3",
        "gear_pad_radius": 3,
        "gear_join_access": True,
        "gear_repo": "../oomlout_oobb_gear_version_5",
    }
    options.append(copy.deepcopy(option))

    for option in options:
        # These centres either lacked joins or used off-grid joins.
        # Use actual M3 half-grid positions, never the M6 grid corners.
        if option["bearing_size"] in ["6808", "6810"]:
            option.setdefault("inner_joining_positions", [[-7.5, 7.5], [7.5, -7.5]])

        holder_type = option.get("holder_type", "holder")
        bearing_size = option["bearing_size"]
        width = option["width"]
        height = option["height"]
        depth = option["depth"]
        extra = option["extra"]

        if bearing_size in ["6704", "6705", "6804", "6709", "6810"]:
            option.setdefault("inner_joining_rotation", 45)

        option["taxonomy_1"] = "oobb"
        option["taxonomy_2"] = "part"
        option["taxonomy_3"] = holder_type
        option["taxonomy_4"] = "bearing"
        option["taxonomy_5"] = f"{bearing_size}_bearing_size"
        option["taxonomy_6"] = f"{width}_width"
        option["taxonomy_7"] = f"{height}_height"
        option["taxonomy_8"] = f"{depth}_depth"
        option["taxonomy_9"] = extra
        option["id"] = build_oomp_id(option)
        if "legacy_id" in option:
            option["legacy_source"] = f"C:/gh/oomlout_oobb_version_3/things/{option['legacy_id']}"

        oobb_details = {}
        oobb_details["oobb_name"] = "bearing_holder"
        if holder_type == "holder_90_degree":
            oobb_details["oobb_name"] = "bearing_holder_90_degree"
        if "corner" in option:
            oobb_details["oobb_name"] = "bearing_holder_corner"
            oobb_details["corner"] = copy.deepcopy(option["corner"])
        oobb_details["holder_type"] = holder_type
        oobb_details["mounting_minimum_web"] = option.get("mounting_minimum_web", 0.3)
        oobb_details["bearing_size"] = bearing_size
        if "bearing_positions" in option:
            oobb_details["bearing_positions"] = copy.deepcopy(option["bearing_positions"])
        oobb_details["width"] = width
        oobb_details["height"] = height
        oobb_details["depth"] = depth
        oobb_details["extra"] = extra
        oobb_details["shaft"] = option.get("shaft", "m6")
        oobb_details["body"] = option.get("body", "plate")
        oobb_details["horn_adapter"] = option.get("horn_adapter", "")
        oobb_details["split"] = option.get("split", True)
        oobb_details["split_z"] = option.get("split_z", 0)
        oobb_details["prepare_print"] = option.get("prepare_print", True)
        oobb_details["print_gap"] = option.get("print_gap", 10)
        oobb_details["interior_hole_positions"] = option.get("interior_hole_positions", [])
        oobb_details["interior_radius_name"] = option.get("interior_radius_name", "m3")
        if "centre_hole_diameter" in option:
            oobb_details["centre_hole_diameter"] = option["centre_hole_diameter"]
        if "shaft_radius" in option:
            oobb_details["shaft_radius"] = option["shaft_radius"]
            oobb_details["shaft_cut_depth"] = option["shaft_cut_depth"]
        if "inside" in option:
            oobb_details["inside"] = option["inside"]
        if "embedded_nut_radius_name" in option:
            oobb_details["embedded_nut_radius_name"] = option["embedded_nut_radius_name"]
        if "embedded_nut_positions" in option:
            oobb_details["embedded_nut_positions"] = option["embedded_nut_positions"]
        if "embedded_nut_rotation" in option:
            oobb_details["embedded_nut_rotation"] = option["embedded_nut_rotation"]
        if "coupler_oomp_id" in option:
            oobb_details["coupler_oomp_id"] = option["coupler_oomp_id"]
        if "coupler_bore" in option:
            oobb_details["coupler_bore"] = option["coupler_bore"]
        if "coupler_flange_diameter" in option:
            oobb_details["coupler_flange_diameter"] = option["coupler_flange_diameter"]
        if "coupler_flange_depth" in option:
            oobb_details["coupler_flange_depth"] = option["coupler_flange_depth"]
        if "coupler_bolt_circle_diameter" in option:
            oobb_details["coupler_bolt_circle_diameter"] = option["coupler_bolt_circle_diameter"]
        if "coupler_mount_count" in option:
            oobb_details["coupler_mount_count"] = option["coupler_mount_count"]
        if "coupler_mount_radius_name" in option:
            oobb_details["coupler_mount_radius_name"] = option["coupler_mount_radius_name"]
        if "coupler_mount_rotation" in option:
            oobb_details["coupler_mount_rotation"] = option["coupler_mount_rotation"]
        if "bearing_inner_diameter" in option:
            oobb_details["bearing_inner_diameter"] = option["bearing_inner_diameter"]
        if "bearing_outer_diameter" in option:
            oobb_details["bearing_outer_diameter"] = option["bearing_outer_diameter"]
        if "bearing_depth" in option:
            oobb_details["bearing_depth"] = option["bearing_depth"]
        if "bearing_print_radial_clearance" in option:
            oobb_details["bearing_print_radial_clearance"] = option["bearing_print_radial_clearance"]
        if "inner_joining_positions" in option:
            oobb_details["inner_joining_positions"] = option["inner_joining_positions"]
        if "inner_joining_radius" in option:
            oobb_details["inner_joining_radius"] = option["inner_joining_radius"]
        if "inner_joining_rotation" in option:
            oobb_details["inner_joining_rotation"] = option["inner_joining_rotation"]
        if "embedded_nut_rotation_radial" in option:
            oobb_details["embedded_nut_rotation_radial"] = option["embedded_nut_rotation_radial"]
        if "inner_joining_head" in option:
            oobb_details["inner_joining_head"] = option["inner_joining_head"]
        option["oobb_details"] = oobb_details

    return options


if __name__ == "__main__":
    main()
