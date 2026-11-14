$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -2.0]) {
							cylinder(h = 4, r = 13.5);
						}
					}
					union() {
						translate(v = [0, 0, -2.01]) {
							cylinder(h = 4.02, r = 10.0);
						}
					}
				}
			}
		}
	}
	union();
}
