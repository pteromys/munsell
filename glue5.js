// Glue code for doing various HTML5-ish things.

function mouse_coords(e) {
	// Given an event object, fetch mouse coordinates; cribbed from quirksmode
	// http://www.quirksmode.org/js/events_properties.html
	if (e.pageX || e.pageY) { return [e.pageX, e.pageY]; }
	else if (e.clientX || e.clientY) {
		return [
			e.clientX + document.body.scrollLeft +
				document.documentElement.scrollLeft,
			e.clientY + document.body.scrollTop +
				document.documentElement.scrollTop
			];
	}
	return [0, 0];
}

window.requestAnimFrame =
	window.requestAnimationFrame ||
	window.webkitRequestAnimationFrame ||
	window.mozRequestAnimationFrame ||
	window.oRequestAnimationFrame ||
	window.msRequestAnimationFrame ||
	function (callback, element) {
		window.setTimeout(callback, 1000 / 60);
	};

