$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -6.0]) {
							cylinder(h = 12, r = 14.5);
						}
					}
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -2.0]) {
											cylinder(h = 4, r = 16.0);
										}
									}
									union() {
										translate(v = [0, 0, -2.01]) {
											cylinder(h = 4.02, r = 12.5);
										}
									}
								}
							}
						}
						translate(v = [0, 0, -3]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -2.0]) {
											cylinder(h = 4, r = 16.0);
										}
									}
									union() {
										translate(v = [0, 0, -2.01]) {
											cylinder(h = 4.02, r = 12.5);
										}
									}
								}
							}
						}
						translate(v = [0, 0, -6]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -2.0]) {
											cylinder(h = 4, r = 16.0);
										}
									}
									union() {
										translate(v = [0, 0, -2.01]) {
											cylinder(h = 4.02, r = 12.5);
										}
									}
								}
							}
						}
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -21.0]) {
											cylinder(h = 42, r = 14.75);
										}
									}
									union() {
										translate(v = [0, 0, -21.01]) {
											cylinder(h = 42.02, r = 13.75);
										}
									}
								}
							}
						}
						translate(v = [-15.0, -15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-15.0, 15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [15.0, -15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [15.0, 15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-7.5, 0, -6.0]) {
							cylinder(h = 6, r = 1.9);
						}
						translate(v = [-7.5, 0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, 0, -6.0]) {
							cylinder(h = 6, r = 1.9);
						}
						translate(v = [7.5, 0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [0, 0, -6.000000000000001]) {
							cylinder(h = 6.6, r = 3.55);
						}
						translate(v = [-2.5, -1.5, -7.0]) {
							cube(size = [5, 3, 14]);
						}
						translate(v = [-1.5, -2.5, -7.0]) {
							cube(size = [3, 5, 14]);
						}
					}
				}
			}
		}
	}
	union();
}
