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
						translate(v = [0, -15, -6.0]) {
							hull() {
								translate(v = [-17.0, 2.0, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [17.0, 2.0, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [-17.0, -2.0, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [17.0, -2.0, 0]) {
									cylinder(h = 12, r = 5);
								}
							}
						}
						translate(v = [-22.0, -28.5, -6.0]) {
							cube(size = [44, 13.5, 12]);
						}
					}
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -3.0]) {
											cylinder(h = 6, r = 8.5);
										}
									}
									union() {
										translate(v = [0, 0, -3.01]) {
											cylinder(h = 6.02, r = 3.0);
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
											cylinder(h = 42, r = 7.5);
										}
									}
									union() {
										translate(v = [0, 0, -21.01]) {
											cylinder(h = 42.02, r = 4.0);
										}
									}
								}
							}
						}
						translate(v = [15.0, 0, -3.0]) {
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
						translate(v = [0, -15.0, -3.0]) {
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
						translate(v = [-15.0, 0, -3.0]) {
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
						translate(v = [0, 15.0, -3.0]) {
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
						translate(v = [-7.5, -15, -3.0]) {
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
						translate(v = [7.5, -15, -3.0]) {
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
						translate(v = [15.0, 0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [15.0, 0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, -15.0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, -15.0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [-15.0, 0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [-15.0, 0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 15.0, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 15.0, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [0, 0, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [-15.0, -15, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [-15.0, -15, 0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 13.5, r = 3.0);
							}
						}
						translate(v = [-20.346620450606586, -24.9, -7.0]) {
							cube(size = [10.693240901213173, 5.4, 14]);
						}
						translate(v = [0.0, -15, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [0.0, -15, 0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 13.5, r = 3.0);
							}
						}
						translate(v = [-5.346620450606586, -24.9, -7.0]) {
							cube(size = [10.693240901213173, 5.4, 14]);
						}
						translate(v = [15.0, -15, -7.0]) {
							cylinder(h = 14, r = 3.0);
						}
						translate(v = [15.0, -15, 0]) {
							rotate(a = [90, 0, 0]) {
								cylinder(h = 13.5, r = 3.0);
							}
						}
						translate(v = [9.653379549393414, -24.9, -7.0]) {
							cube(size = [10.693240901213173, 5.4, 14]);
						}
						translate(v = [-7.5, -15, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [-7.5, -15, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [7.5, -15, -6.0]) {
							cylinder(h = 3, r = 2.4);
						}
						translate(v = [7.5, -15, 3.0]) {
							cylinder(h = 3, r = 2.4);
						}
					}
				}
			}
		}
	}
	union();
}
