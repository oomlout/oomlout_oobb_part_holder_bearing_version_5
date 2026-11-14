include <components/github_belfry_bosl2_gear/BOSL2/std.scad>;
include <components/github_belfry_bosl2_gear/BOSL2/gears.scad>;

// True bevel teeth, not a scaled spur extrusion. All dimensions refer to the large end.
module oobb_gear_bevel_raw(teeth=20, mate_teeth=20, gear_mod=1.5, depth=9,
    face_width=4.5, shaft_diam=0, pressure_angle=20, backlash=0.2,
    clearance=0.375, gear_spin=0, anchor="center") {
    bare = bevel_gear(mod=gear_mod, teeth=teeth, mate_teeth=mate_teeth,
        shaft_angle=90, face_width=face_width, backing=0,
        pressure_angle=pressure_angle, backlash=backlash, clearance=clearance,
        spiral=0, cutter_radius=0, gear_spin=gear_spin, anchor="pitchbase");
    bounds = pointlist_bounds(bare[0]);
    tooth_height = bounds[1].z - bounds[0].z;
    backing = depth - tooth_height;
    assert(backing > 0, "depth must exceed the complete tooth envelope");
    delta = atan(teeth/mate_teeth);
    apex = gear_mod*teeth/2/tan(delta);
    shift = anchor == "center" ? depth/2-bounds[1].z
          : anchor == "bottom" ? depth-bounds[1].z
          : anchor == "apex" ? -apex : 0;
    translate([0,0,shift])
        bevel_gear(mod=gear_mod, teeth=teeth, mate_teeth=mate_teeth,
            shaft_angle=90, face_width=face_width, backing=backing,
            cone_backing=false, shaft_diam=shaft_diam,
            pressure_angle=pressure_angle, backlash=backlash, clearance=clearance,
            spiral=0, cutter_radius=0, gear_spin=gear_spin, anchor="pitchbase");
}
