// Trilinearly interpolate.
Munsell.interpolate = function (i, j, k) {
	// modified multiplication to return 0 for 0 * NaN and 0 * Infinity.
	function mul(factor, maybe_number) {
		if (factor == 0) { return 0; }
		else { return factor * maybe_number; }
	}
	// Insert gray
	var i0 = Math.floor(i);
	var j0 = Math.floor(j);
	var k0 = Math.floor(k);
	var i1 = (i0 + 1) % 40;
	var j1 = j0 + 1;
	var k1 = k0 + 1;
	var a1 = i - i0;
	var b1 = j - j0;
	var c1 = k - k0;
	var a0 = 1 - a1;
	var b0 = 1 - b1;
	var c0 = 1 - c1;
	var ans = [0, 0, 0];
	for (var t in ans) {
		ans[t] =
			mul(a0 * b0 * c0, Munsell[i0][j0][k0][t]) +
			mul(a1 * b0 * c0, Munsell[i1][j0][k0][t]) +
			mul(a0 * b1 * c0, Munsell[i0][j1][k0][t]) +
			mul(a1 * b1 * c0, Munsell[i1][j1][k0][t]) +
			mul(a0 * b0 * c1, Munsell[i0][j0][k1][t]) +
			mul(a1 * b0 * c1, Munsell[i1][j0][k1][t]) +
			mul(a0 * b1 * c1, Munsell[i0][j1][k1][t]) +
			mul(a1 * b1 * c1, Munsell[i1][j1][k1][t]);
	}
	return ans;
}
