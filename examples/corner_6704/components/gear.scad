$fn = 50;

include <../scad_reference/oobb_gear_bevel_raw.scad>;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						oobb_gear_bevel_raw(anchor = "center", backlash = 0.2, clearance = 0.375, depth = 12, face_width = 6.0, gear_mod = 1.5, gear_spin = 0, mate_teeth = 30, pressure_angle = 20, shaft_diam = 0, teeth = 30);
					}
					union() {
						translate(v = [0, 0, -7.0]) {
							cylinder(h = 14, r = 3.25);
						}
						translate(v = [-7.5, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [-7.5, 0.0, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [-7.5, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [0.0, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [0.0, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [7.5, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [7.5, 0.0, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
						translate(v = [7.5, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.8);
						}
					}
				}
			}
		}
	}
	union();
}
