$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -3.5]) {
							cylinder(h = 7, r = 32.5);
						}
					}
					union() {
						translate(v = [0, 0, -3.51]) {
							cylinder(h = 7.02, r = 25.0);
						}
					}
				}
			}
		}
	}
	union();
}
