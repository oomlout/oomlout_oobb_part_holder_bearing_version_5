$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, -6.0]) {
							hull() {
								translate(v = [-32.5, 32.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [32.5, 32.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [-32.5, -32.5, 0]) {
									cylinder(h = 12, r = 5);
								}
								translate(v = [32.5, -32.5, 0]) {
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
						translate(v = [30.0, 0, 6.0]) {
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
						translate(v = [0, -30.0, -6.0]) {
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
						translate(v = [-30.0, 0, 6.0]) {
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
						translate(v = [0, 30.0, -6.0]) {
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
						translate(v = [-10.606601717798213, 10.606601717798213, 6.0]) {
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
						translate(v = [10.606601717798213, -10.606601717798213, -6.0]) {
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
						translate(v = [0, -7.375, -6.0]) {
							rotate(a = [0, 180, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -1.3]) {
											cylinder(h = 1.3, r = 2.5);
										}
										translate(v = [0, 0, -13.3]) {
											cylinder(h = 12, r = 1.0);
										}
									}
									union();
								}
							}
						}
						translate(v = [0, 7.375, -6.0]) {
							rotate(a = [0, 180, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -1.3]) {
											cylinder(h = 1.3, r = 2.5);
										}
										translate(v = [0, 0, -13.3]) {
											cylinder(h = 12, r = 1.0);
										}
									}
									union();
								}
							}
						}
						translate(v = [-30.0, -30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-30.0, -15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-30.0, 15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-30.0, 30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-15.0, -30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [-15.0, 30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [15.0, -30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [15.0, 30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [30.0, -30.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [30.0, -15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [30.0, 15.0, -100.0]) {
							cylinder(h = 200, r = 3.0);
						}
						translate(v = [30.0, 30.0, -100.0]) {
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
							cylinder(h = 4, r1 = 2.9, r2 = 2.8);
						}
						translate(v = [0, 0, -7.0]) {
							cylinder(h = 14, r = 1.25);
						}
					}
				}
			}
		}
	}
	union();
}
