$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -6.0]) {
							hull() {
								translate(v = [-17.5, 17.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [17.5, 17.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [-17.5, -17.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [17.5, -17.5, 0]) {
									cylinder(h = 12, r = 5);
								}
							}
						}
					}
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -2.5]) {
											cylinder(h = 5, r = 13.0);
										}
									}
									union() {
										translate(v = [0, 0, -2.51]) {
											cylinder(h = 5.02, r = 8.5);
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
											cylinder(h = 42, r = 11.25);
										}
									}
									union() {
										translate(v = [0, 0, -21.01]) {
											cylinder(h = 42.02, r = 10.25);
										}
									}
								}
							}
						}
						translate(v = [17.0, 0, -3.0]) {
							rotate(a = [0, 0, 30]) {
								difference() {
									union() {
										linear_extrude(height = 6) {
											polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, -17.0, -3.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										linear_extrude(height = 6) {
											polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [-17.0, 0, -3.0]) {
							rotate(a = [0, 0, 30]) {
								difference() {
									union() {
										linear_extrude(height = 6) {
											polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 17.0, -3.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										linear_extrude(height = 6) {
											polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
										}
									}
									union();
								}
							}
						}
						translate(v = [-7.75, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [-0.25, 0, -7.0]) {
												cylinder(h = 14, r = 1.5);
											}
											translate(v = [0.25, 0, -7.0]) {
												cylinder(h = 14, r = 1.5);
											}
										}
										union();
									}
								}
							}
						}
						translate(v = [7.75, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								hull() {
									difference() {
										union() {
											translate(v = [-0.25, 0, -7.0]) {
												cylinder(h = 14, r = 1.5);
											}
											translate(v = [0.25, 0, -7.0]) {
												cylinder(h = 14, r = 1.5);
											}
										}
										union();
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
						translate(v = [17.0, 0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [17.0, 0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, -17.0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, -17.0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [-17.0, 0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [-17.0, 0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 17.0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 17.0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
					}
				}
			}
		}
	}
	union();
}
