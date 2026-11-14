$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -6.0]) {
							cylinder(h = 12, r = 24.5);
						}
					}
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -3.0]) {
											cylinder(h = 6, r = 27.5);
										}
									}
									union() {
										translate(v = [0, 0, -3.01]) {
											cylinder(h = 6.02, r = 22.5);
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
											cylinder(h = 42, r = 25.5);
										}
									}
									union() {
										translate(v = [0, 0, -21.01]) {
											cylinder(h = 42.02, r = 24.5);
										}
									}
								}
							}
						}
						translate(v = [-13.000000000000004, 13.000000000000004, -6.0]) {
							rotate(a = [0, 0, 45.0]) {
								difference() {
									union() {
										linear_extrude(height = 2.5) {
											polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [13.000000000000004, -13.000000000000004, 3.5]) {
							rotate(a = [0, 0, 45.0]) {
								difference() {
									union() {
										linear_extrude(height = 2.5) {
											polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -7.0]) {
											cylinder(h = 14, r = 0.95);
										}
									}
									union();
								}
							}
						}
						translate(v = [-15.0, 0.0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [0.0, -15.0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [0.0, 15.0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [15.0, 0.0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [-15.0, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-15.0, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-7.5, -15.0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-7.5, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-7.5, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-7.5, 15.0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [0.0, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [0.0, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, -15.0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, 15.0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [15.0, -7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [15.0, 7.5, -7.0]) {
							cylinder(h = 14, r = 1.5);
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
						translate(v = [-13.000000000000004, 13.000000000000004, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [-13.000000000000004, 13.000000000000004, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [13.000000000000004, -13.000000000000004, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [13.000000000000004, -13.000000000000004, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
					}
				}
			}
		}
	}
	union();
}
