$fn = 50;

difference() {
	union() {
		translate(v = [0, 0, 0]) {
			rotate(a = [0, 0, 0]) {
				difference() {
					union() {
						translate(v = [0, 0, 6.0]) {
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
															cylinder(h = 6, r = 27.7);
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
															cylinder(h = 42, r = 25.6);
														}
													}
													union() {
														translate(v = [0, 0, -21.01]) {
															cylinder(h = 42.02, r = 24.6);
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
										translate(v = [0, -30.0, -6.0]) {
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
										translate(v = [-30.0, 0, 6.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 30]) {
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
										translate(v = [0, 30.0, -6.0]) {
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
										translate(v = [-10.606601717798213, 10.606601717798213, 6.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 45.0]) {
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
										translate(v = [10.606601717798213, -10.606601717798213, -6.0]) {
											rotate(a = [0, 180, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 45.0]) {
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
										translate(v = [-7.75, 0, 0]) {
											rotate(a = [0, 0, 0]) {
												hull() {
													difference() {
														union() {
															translate(v = [-0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
															}
															translate(v = [0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
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
																cylinder(h = 14, r = 1.8);
															}
															translate(v = [0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
															}
														}
														union();
													}
												}
											}
										}
										translate(v = [-30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0, 0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-250, -250, 0]) {
											cube(size = [500, 500, 500]);
										}
									}
								}
							}
						}
						translate(v = [85, 0, 6.0]) {
							rotate(a = [180, 0, 0]) {
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
															cylinder(h = 6, r = 27.7);
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
															cylinder(h = 42, r = 25.6);
														}
													}
													union() {
														translate(v = [0, 0, -21.01]) {
															cylinder(h = 42.02, r = 24.6);
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
										translate(v = [0, -30.0, -6.0]) {
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
										translate(v = [-30.0, 0, 6.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 30]) {
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
										translate(v = [0, 30.0, -6.0]) {
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
										translate(v = [-10.606601717798213, 10.606601717798213, 6.0]) {
											rotate(a = [0, 0, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 45.0]) {
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
										translate(v = [10.606601717798213, -10.606601717798213, -6.0]) {
											rotate(a = [0, 180, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -12.0]) {
															rotate(a = [0, 0, 45.0]) {
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
										translate(v = [-7.75, 0, 0]) {
											rotate(a = [0, 0, 0]) {
												hull() {
													difference() {
														union() {
															translate(v = [-0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
															}
															translate(v = [0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
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
																cylinder(h = 14, r = 1.8);
															}
															translate(v = [0.25, 0, -7.0]) {
																cylinder(h = 14, r = 1.8);
															}
														}
														union();
													}
												}
											}
										}
										translate(v = [-30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, -30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [30.0, 30.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [-15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0.0, -15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0.0, 15.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [15.0, 0.0, -100.0]) {
											cylinder(h = 200, r = 3.25);
										}
										translate(v = [0, 0, -7.0]) {
											cylinder(h = 14, r = 3.25);
										}
										translate(v = [-250, -250, -500]) {
											cube(size = [500, 500, 500]);
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
	union();
}
