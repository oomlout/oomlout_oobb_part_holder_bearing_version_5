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
											cylinder(h = 12, r = 12);
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
										translate(v = [0, -7.375, -6.0]) {
											rotate(a = [0, 180, 0]) {
												difference() {
													union() {
														translate(v = [0, 0, -1.25]) {
															cylinder(h = 1.25, r = 2.5);
														}
														translate(v = [0, 0, -13.25]) {
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
														translate(v = [0, 0, -1.25]) {
															cylinder(h = 1.25, r = 2.5);
														}
														translate(v = [0, 0, -13.25]) {
															cylinder(h = 12, r = 1.0);
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
			}
		}
	}
}
