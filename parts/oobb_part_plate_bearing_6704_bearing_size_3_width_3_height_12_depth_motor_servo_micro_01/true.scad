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
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -21.0]) {
											cylinder(h = 42, r = 12.25);
										}
									}
									union() {
										translate(v = [0, 0, -21.01]) {
											cylinder(h = 42.02, r = 11.25);
										}
									}
								}
							}
						}
						translate(v = [18.0, 0, 6.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 30]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, -18.0, -6.0]) {
							rotate(a = [0, 180, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [-18.0, 0, 6.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 30]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 18.0, -6.0]) {
							rotate(a = [0, 180, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [-5.303300858899107, 5.303300858899107, 6.0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 45.0]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
										}
									}
									union();
								}
							}
						}
						translate(v = [5.303300858899107, -5.303300858899107, -6.0]) {
							rotate(a = [0, 180, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -12.0]) {
											rotate(a = [0, 0, 45.0]) {
												difference() {
													union() {
														linear_extrude(height = 2.5) {
															polygon(points = [[3.1734999999999998, 0.0], [1.5867500000000003, 2.7483316189099156], [-1.5867499999999992, 2.748331618909916], [-3.1734999999999998, 3.886416617094125e-16], [-1.5867500000000012, -2.748331618909915], [1.5867499999999977, -2.748331618909917]]);
														}
														translate(v = [0, 0, -100.0]) {
															cylinder(h = 200, r = 1.5);
														}
													}
													union();
												}
											}
										}
										translate(v = [0, 0, -1.7]) {
											cylinder(h = 1.7, r1 = 1.5, r2 = 2.9);
										}
										translate(v = [0, 0, -12.0]) {
											cylinder(h = 12, r = 1.5);
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
						translate(v = [-7.5, 0, -6.0]) {
							cylinder(h = 6, r = 2.1);
						}
						translate(v = [-7.5, 0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [7.5, 0, -6.0]) {
							cylinder(h = 6, r = 2.1);
						}
						translate(v = [7.5, 0, -7.0]) {
							cylinder(h = 14, r = 1.5);
						}
						translate(v = [0, 0, -6.0]) {
							cylinder(h = 3, r1 = 2.5, r2 = 2.4);
						}
						translate(v = [0, 0, -7.0]) {
							cylinder(h = 14, r = 1.0);
						}
					}
				}
			}
		}
	}
	union();
}
