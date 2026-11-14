$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 4.5]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -4.5]) {
											cylinder(h = 9, r = 11.35);
										}
									}
									union() {
										translate(v = [0, 0, 0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -2.0]) {
															cylinder(h = 4, r = 13.7);
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
										translate(v = [0, 0, 0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -19.5]) {
															cylinder(h = 39, r = 12.35);
														}
													}
													union() {
														translate(v = [0, 0, -19.51]) {
															cylinder(h = 39.02, r = 11.35);
														}
													}
												}
											}
										}
										translate(v = [-5.303300858899107, 5.303300858899107, 4.5]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -1.9]) {
															cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
														}
														translate(v = [0, 0, -9.0]) {
															cylinder(h = 9, r = 1.8);
														}
													}
													union();
												}
											}
										}
										translate(v = [-5.303300858899107, 5.303300858899107, -4.5]) {
											rotate(a = [0, 0, 45.0]) {
												difference() {
													union() {
														linear_extrude(height = 2.4) {
															polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
														}
														translate(v = [-1.75, -3.25, -0.3]) {
															cube(size = [3.5, 6.5, 0.3]);
														}
														translate(v = [-1.75, -1.75, -0.6]) {
															cube(size = [3.5, 3.5, 0.3]);
														}
														translate(v = [-1.75, -3.25, 2.4]) {
															cube(size = [3.5, 6.5, 0.3]);
														}
														translate(v = [-1.75, -1.75, 2.6999999999999997]) {
															cube(size = [3.5, 3.5, 0.3]);
														}
													}
													union();
												}
											}
										}
										translate(v = [5.303300858899107, -5.303300858899107, -4.5]) {
											rotate(a = [0, 180, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -1.9]) {
															cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
														}
														translate(v = [0, 0, -9.0]) {
															cylinder(h = 9, r = 1.8);
														}
													}
													union();
												}
											}
										}
										translate(v = [5.303300858899107, -5.303300858899107, 4.5]) {
											rotate(a = [0, 180, -45.0]) {
												difference() {
													union() {
														linear_extrude(height = 2.4) {
															polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
														}
														translate(v = [-1.75, -3.25, -0.3]) {
															cube(size = [3.5, 6.5, 0.3]);
														}
														translate(v = [-1.75, -1.75, -0.6]) {
															cube(size = [3.5, 3.5, 0.3]);
														}
														translate(v = [-1.75, -3.25, 2.4]) {
															cube(size = [3.5, 6.5, 0.3]);
														}
														translate(v = [-1.75, -1.75, 2.6999999999999997]) {
															cube(size = [3.5, 3.5, 0.3]);
														}
													}
													union();
												}
											}
										}
										translate(v = [-30.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [-30.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [-30.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [-15.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [-15.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [15.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [15.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [30.0, -15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [30.0, 0.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [30.0, 15.0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
										translate(v = [-30.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-30.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-22.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-22.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-22.5, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-22.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-15.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-7.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [-7.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [0.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [0.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [7.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [7.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [15.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [22.5, -15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [22.5, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [22.5, 0.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [22.5, 15.0, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [30.0, -7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [30.0, 7.5, -5.5]) {
											cylinder(h = 11, r = 1.8);
										}
										translate(v = [0, 0, -5.5]) {
											cylinder(h = 11, r = 3.25);
										}
									}
								}
							}
						}
					}
					union() {
						translate(v = [-250.0, -250.0, 0.0]) {
							cube(size = [500, 500, 500]);
						}
					}
				}
			}
		}
	}
	union();
}
