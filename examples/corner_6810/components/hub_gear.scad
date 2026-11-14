$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 6.0]) {
			rotate(a = [180, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 0]) {
							rotate(a = [0, 0, 0]) {
								difference() {
									union() {
										translate(v = [0, 0, -6.0]) {
											cylinder(h = 12, r = 28.35);
										}
									}
									union() {
										translate(v = [0, 0, 0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -3.5]) {
															cylinder(h = 7, r = 32.7);
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
															cylinder(h = 42, r = 29.35);
														}
													}
													union() {
														translate(v = [0, 0, -21.01]) {
															cylinder(h = 42.02, r = 28.35);
														}
													}
												}
											}
										}
										translate(v = [-7.5, 7.5, 6.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 0]) {
																difference() {
																	union() {
																		linear_extrude(height = 3) {
																			polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
																		}
																		translate(v = [-1.75, -3.25, -0.3]) {
																			cube(size = [3.5, 6.5, 0.3]);
																		}
																		translate(v = [-1.75, -1.75, -0.6]) {
																			cube(size = [3.5, 3.5, 0.3]);
																		}
																		translate(v = [-1.75, -3.25, 3]) {
																			cube(size = [3.5, 6.5, 0.3]);
																		}
																		translate(v = [-1.75, -1.75, 3.3]) {
																			cube(size = [3.5, 3.5, 0.3]);
																		}
																		translate(v = [0, 0, -100.0]) {
																			cylinder(h = 200, r = 1.8);
																		}
																	}
																	union();
																}
															}
														}
														translate(v = [0, 0, -1.9]) {
															cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
														}
														translate(v = [0, 0, -12.0]) {
															cylinder(h = 12, r = 1.8);
														}
													}
													union();
												}
											}
										}
										translate(v = [7.5, -7.5, -6.0]) {
											rotate(a = [0, 180, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 0]) {
																difference() {
																	union() {
																		linear_extrude(height = 3) {
																			polygon(points = [[3.4619999999999997, 0.0], [1.7310000000000003, 2.9981799479017264], [-1.7309999999999992, 2.9981799479017264], [-3.4619999999999997, 4.2397272186481365e-16], [-1.7310000000000014, -2.998179947901726], [1.7309999999999977, -2.9981799479017277]]);
																		}
																		translate(v = [-1.75, -3.25, -0.3]) {
																			cube(size = [3.5, 6.5, 0.3]);
																		}
																		translate(v = [-1.75, -1.75, -0.6]) {
																			cube(size = [3.5, 3.5, 0.3]);
																		}
																		translate(v = [-1.75, -3.25, 3]) {
																			cube(size = [3.5, 6.5, 0.3]);
																		}
																		translate(v = [-1.75, -1.75, 3.3]) {
																			cube(size = [3.5, 3.5, 0.3]);
																		}
																		translate(v = [0, 0, -100.0]) {
																			cylinder(h = 200, r = 1.8);
																		}
																	}
																	union();
																}
															}
														}
														translate(v = [0, 0, -1.9]) {
															cylinder(h = 1.9, r1 = 1.8, r2 = 3.6);
														}
														translate(v = [0, 0, -12.0]) {
															cylinder(h = 12, r = 1.8);
														}
													}
													union();
												}
											}
										}
										translate(v = [-45.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-45.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-45.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-45.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-45.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-30.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-30.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-15.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-15.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-15.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [0.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [0.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [15.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [15.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [15.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [30.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [30.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [45.0, -30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [45.0, -15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [45.0, 0.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [45.0, 15.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [45.0, 30.0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-45.0, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-45.0, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, -30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, -22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, -15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, 15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, 22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-37.5, 30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-30.0, -22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-30.0, 22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-22.5, -30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-22.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-22.5, 30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-15.0, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-15.0, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-7.5, -15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-7.5, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-7.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [-7.5, 15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [0.0, -22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [0.0, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [0.0, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [0.0, 22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [7.5, -15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [7.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [7.5, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [7.5, 15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [15.0, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [15.0, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [22.5, -30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [22.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [22.5, 30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [30.0, -22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [30.0, 22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, -30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, -22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, -15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, 0.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, 15.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, 22.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [37.5, 30.0, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [45.0, -7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [45.0, 7.5, -7.0]) {
											cylinder(h = 14, r = 1.8);
										}
										translate(v = [0, 0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
									}
								}
							}
						}
					}
					union() {
						translate(v = [-250.0, -250.0, -500.0]) {
							cube(size = [500, 500, 500]);
						}
					}
				}
			}
		}
		translate(v = [-15, -15, -9.712800000000001]) {
			cylinder(h = 9.712800000000001, r = 4.8);
		}
		translate(v = [-15, 15, -9.712800000000001]) {
			cylinder(h = 9.712800000000001, r = 4.8);
		}
		translate(v = [15, -15, -9.712800000000001]) {
			cylinder(h = 9.712800000000001, r = 4.8);
		}
		translate(v = [15, 15, -9.712800000000001]) {
			cylinder(h = 9.712800000000001, r = 4.8);
		}
	}
	union() {
		translate(v = [-15, -15, -10.712800000000001]) {
			cylinder(h = 11.712800000000001, r = 3.25);
		}
		translate(v = [-15, 15, -10.712800000000001]) {
			cylinder(h = 11.712800000000001, r = 3.25);
		}
		translate(v = [15, -15, -10.712800000000001]) {
			cylinder(h = 11.712800000000001, r = 3.25);
		}
		translate(v = [15, 15, -10.712800000000001]) {
			cylinder(h = 11.712800000000001, r = 3.25);
		}
	}
}
