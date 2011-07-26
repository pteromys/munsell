// Coloring functions
Color = new Object();

Color.cssrgb = function (c) {
	return 'rgb(' + c[0] + ',' + c[1] + ',' + c[2] + ')';
}

Color.complex = function (z) {
	var ans = [0, 0, 0];
	var inv_scale = 2;
	var a = z.abs();
	if (a == 0) { return ans; }
	var x = z.x / a;
	var y = z.y / a;
	a = 1 - 1 / ((a * inv_scale) + 1);
	ans[0] = 0.6 + 0.3 * x + 0.35 * (1 - a) *
		Math.pow(0.5 + 0.4 * y + 0.3 * x, 2);
	ans[1] = 0.5 + (0.45 + 0.05 * a) * (-0.8 * x + 0.6 * y) +
		0.05 * x * x * (1 - a);
	ans[1] = a * (1 - Math.pow(1 - ans[1], 2)) + (1 - a) * ans[1];
	ans[1] = 0.92 * ans[1] - 0.08 * x * y;
	ans[2] = 0.5 + 0.5 * (-0.95 * y - 0.3122499 * x);
	ans[2] *= (0.8 + 0.2 * ans[2]);
	ans[2] = 0.92 * ans[2] + 0.08;
	for (var i in ans) { ans[i] = Math.min(Math.max(0, ans[i]), 1); }
	var l = 0.11 * ans[0] + 0.55 * ans[1] + 0.06 * ans[2] +
		0.34 * ans[1] * ans[2] + 0.19 * ans[0] * ans[2] +
		0.12 * ans[0] * ans[1];
	var kthresh = 0.26 + 0.74 * l;
	if (a < kthresh) {
		var k = a / kthresh;
		k = (Math.pow(2.5 - 2 * l + k, 2) - Math.pow(2.5 - 2 * l, 2)) /
			(Math.pow(3.5 - 2 * l, 2) - Math.pow(2.5 - 2 * l, 2));
		k = slow_top(k);
		for (var i in ans) { ans[i] *= k; }
	}
	if (a > l) {
		var w = (a - l)/(1 - l);
		w = (Math.pow(1.1 - l + w, 2) - Math.pow(1.1 - l, 2)) /
			(Math.pow(2.1 - l, 2) - Math.pow(1.1 - l, 2));
		w = 1 - slow_top(1 - w);
		for (var i in ans) { ans[i] = w + (1 - w) * ans[i]; }
	}
	for (var i in ans) { ans[i] = (4 - Math.pow(2 - ans[i], 2)) * 0.333333; }
	for (var i in ans) { ans[i] = Math.round(ans[i] * 255); }
	return ans;
};

Color.tinter = function (base) {
	return function (c) {
		// Start with base color
		var t = [0, 0, 0];
		for (var i in t) { t[i] = base[i]; }
		// Use position variable only
		var a = c.x * 3;
		if (a < 0) {
			for (var i in t) { t[i] *= 1/(1 - a); }
		} else {
			for (var i in t) { t[i] = 1 - (1 - t[i]) / (1 + a); }
		}
		for (var i in t) { t[i] = Math.round(t[i] * 255); }
		return t;
	};
};

