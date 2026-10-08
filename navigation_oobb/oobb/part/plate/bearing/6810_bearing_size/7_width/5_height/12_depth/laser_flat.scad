$fn = 50;

union() {
	translate(v = [0, 0, 0]) {
		projection() {
			intersection() {
				translate(v = [-500, -500, 1.5]) {
					cube(size = [1000, 1000, 0.1]);
				}
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -6.0]) {
											hull() {
												translate(v = [-47.5, 32.5, 0]) {
													cylinder(h = 12, r = 5);
												}
												translate(v = [47.5, 32.5, 0]) {
													cylinder(h = 12, r = 5);
												}
												translate(v = [-47.5, -32.5, 0]) {
													cylinder(h = 12, r = 5);
												}
												translate(v = [47.5, -32.5, 0]) {
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
														translate(v = [0, 0, -3.5]) {
															cylinder(h = 7, r = 32.5);
														}
													}
													union() {
														translate(v = [0, 0, -3.51]) {
															cylinder(h = 7.02, r = 25);
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
															cylinder(h = 42, r = 29.25);
														}
													}
													union() {
														translate(v = [0, 0, -21.01]) {
															cylinder(h = 42.02, r = 28.25);
														}
													}
												}
											}
										}
										translate(v = [30.0, -22, -3.0]) {
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
										translate(v = [-22, -30.0, -3.0]) {
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
										translate(v = [-30.0, 22, -3.0]) {
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
										translate(v = [22, 30.0, -3.0]) {
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
										translate(v = [-45.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [-45.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [-45.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [-45.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [-45.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [45.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [45.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [45.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [45.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [45.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.0);
										}
										translate(v = [-30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [-30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [-15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [0.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [0.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.0);
										}
										translate(v = [30.0, -22, -6.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [30.0, -22, 3.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-22, -30.0, -6.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-22, -30.0, 3.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-30.0, 22, -6.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-30.0, 22, 3.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [22, 30.0, -6.0]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [22, 30.0, 3.0]) {
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
			}
		}
	}
}
