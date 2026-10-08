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
    option["plate_type"] = 'plate_90_degree'
    option["legacy_id"] = 'oobb_bearing_plate_jack_03_03_12_606'
    options.append(copy.deepcopy(option))

    option = {}
    option["bearing_size"] = '606'
    option["width"] = 3
    option["height"] = 3
    option["depth"] = 12
    option["extra"] = 'basic'
    option["plate_type"] = 'plate_90_degree'
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
        [-6.5, 0],
        [6.5, 0],
        [0, -6.5],
        [0, 6.5],
    ]
    option["inner_joining_head"] = 'socket_cap'
    option["embedded_nut_rotation"] = 30
    option["embedded_nut_rotation_radial"] = True
    option["experimental"] = True
    option["design_note"] = '13 mm nut spacing, rotated flats, central M6 hole retained. Approximately 0.25 mm minimum web at print clearances: experimental, physical fit and strength unverified.'
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
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
    option["interior_grid"] = 0
    option["inner_joining_rotation"] = 45
    options.append(copy.deepcopy(option))

    for option in options:
        plate_type = option.get("plate_type", "plate")
        bearing_size = option["bearing_size"]
        width = option["width"]
        height = option["height"]
        depth = option["depth"]
        extra = option["extra"]

        if bearing_size in ["6704", "6705", "6804", "6709", "6810"]:
            option["inner_joining_rotation"] = 45
        if bearing_size == "6709":
            if extra == "":
                # Four usable 15 mm grid holes, with the centre drawn below.
                option["interior_grid"] = 3

        option["taxonomy_1"] = "oobb"
        option["taxonomy_2"] = "part"
        option["taxonomy_3"] = plate_type
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
        oobb_details["oobb_name"] = "bearing_plate"
        if plate_type == "plate_90_degree":
            oobb_details["oobb_name"] = "bearing_plate_90_degree"
        oobb_details["bearing_size"] = bearing_size
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
        oobb_details["joining_tangent_clearance"] = option.get("joining_tangent_clearance", 0.01)
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
        if "interior_grid" in option:
            oobb_details["interior_grid"] = option["interior_grid"]
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
