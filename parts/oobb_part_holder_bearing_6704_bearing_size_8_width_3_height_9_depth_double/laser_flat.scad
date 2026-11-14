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
										translate(v = [0, 0, -4.5]) {
											hull() {
												translate(v = [-55.0, 17.5, 0]) {
													cylinder(h = 9, r = 5);
												}
												translate(v = [55.0, 17.5, 0]) {
													cylinder(h = 9, r = 5);
												}
												translate(v = [-55.0, -17.5, 0]) {
													cylinder(h = 9, r = 5);
												}
												translate(v = [55.0, -17.5, 0]) {
													cylinder(h = 9, r = 5);
												}
											}
										}
									}
									union() {
										translate(v = [-22.5, 0.0, 0]) {
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
										translate(v = [-22.5, 0.0, 0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -19.5]) {
															cylinder(h = 39, r = 12.25);
														}
													}
													union() {
														translate(v = [0, 0, -19.51]) {
															cylinder(h = 39.02, r = 11.25);
														}
													}
												}
											}
										}
										translate(v = [22.5, 0.0, 0]) {
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
										translate(v = [22.5, 0.0, 0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -19.5]) {
															cylinder(h = 39, r = 12.25);
														}
													}
													union() {
														translate(v = [0, 0, -19.51]) {
															cylinder(h = 39.02, r = 11.25);
														}
													}
												}
											}
										}
										translate(v = [56.0, 8, -1.5]) {
											rotate(a = [0, 0, 30]) {
												difference() {
													union() {
														linear_extrude(height = 3) {
															polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
														}
													}
													union();
												}
											}
										}
										translate(v = [-8, 18.5, -1.5]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														linear_extrude(height = 3) {
															polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
														}
													}
													union();
												}
											}
										}
										translate(v = [-56.0, -8, -1.5]) {
											rotate(a = [0, 0, 30]) {
												difference() {
													union() {
														linear_extrude(height = 3) {
															polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
														}
													}
													union();
												}
											}
										}
										translate(v = [8, -18.5, -1.5]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														linear_extrude(height = 3) {
															polygon(points = [[3.3465999999999996, 0.0], [1.6733000000000002, 2.8982406163050016], [-1.6732999999999991, 2.898240616305002], [-3.3465999999999996, 4.0984029780265316e-16], [-1.6733000000000013, -2.8982406163050016], [1.6732999999999976, -2.8982406163050034]]);
														}
													}
													union();
												}
											}
										}
										translate(v = [-27.803300858899107, 5.303300858899107, -4.5]) {
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
										translate(v = [17.196699141100893, 5.303300858899107, -4.5]) {
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
										translate(v = [-17.196699141100893, -5.303300858899107, 2.0]) {
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
										translate(v = [27.803300858899107, -5.303300858899107, 2.0]) {
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
										translate(v = [-22.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [22.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-52.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-52.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-52.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-37.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-37.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-7.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [7.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [37.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [37.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [52.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [52.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [52.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.0);
										}
										translate(v = [-52.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-45.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-45.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-45.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-45.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-45.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-37.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-37.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-30.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-30.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-30.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-22.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-22.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-15.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-15.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-15.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-7.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-7.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [0.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [0.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [0.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [0.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [0.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [7.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [7.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [15.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [15.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [15.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [22.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [22.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [30.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [30.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [30.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [37.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [37.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [45.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [45.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [45.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [45.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [45.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [52.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [56.0, 8, -4.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [56.0, 8, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-8, 18.5, -4.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-8, 18.5, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-56.0, -8, -4.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-56.0, -8, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [8, -18.5, -4.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [8, -18.5, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-27.803300858899107, 5.303300858899107, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-27.803300858899107, 5.303300858899107, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [17.196699141100893, 5.303300858899107, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [17.196699141100893, 5.303300858899107, 1.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [-17.196699141100893, -5.303300858899107, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [-17.196699141100893, -5.303300858899107, -4.5]) {
											cylinder(h = 3, r = 2.4);
										}
										translate(v = [27.803300858899107, -5.303300858899107, -5.5]) {
											cylinder(h = 11, r = 1.5);
										}
										translate(v = [27.803300858899107, -5.303300858899107, -4.5]) {
											cylinder(h = 3, r = 2.4);
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
