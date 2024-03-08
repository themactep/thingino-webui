<div class="motor justify-content-center mt-4">
<button class="btn btn-secondary" data-dir="ul">↖</button>
<button class="btn btn-secondary" data-dir="uc">↑</button>
<button class="btn btn-secondary" data-dir="ur">↗</button>
<button class="btn btn-secondary" data-dir="lc">←</button>
<button class="btn btn-secondary" data-dir="cc">⟴</button>
<button class="btn btn-secondary" data-dir="rc">→</button>
<button class="btn btn-secondary" data-dir="dl">↙</button>
<button class="btn btn-secondary" data-dir="dc">↓</button>
<button class="btn btn-secondary" data-dir="dr">↘</button>
</div>

<script>
function moveMotor(dir) {
	const steps = 100;
	const x_max=<% echo -n $(fw_printenv -n motor_maxstep_h) %>;
	const y_max=<% echo -n $(fw_printenv -n motor_maxstep_v) %>;
	const x_step = x_max / steps;
	const y_step = y_max / steps;
	let y = dir.includes("u") ? -y_step : dir.includes("d") ? y_step : 0;
	let x = dir.includes("l") ? -x_step : dir.includes("r") ? x_step : 0;
	xhrGet("/cgi-bin/j/motor.cgi?x=" + x + "&y=" + y);
}
$$(".motor button").forEach(el => el.addEventListener("click", ev => moveMotor(ev.target.dataset.dir)));
</script>
