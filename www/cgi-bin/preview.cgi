#!/usr/bin/haserl
<%in p/common.cgi %>
<% page_title="Camera preview" %>
<%in p/header.cgi %>

<div class="row preview">
<div class="col-md-8 col-xl-9 col-xxl-9 position-relative mb-3">
<% preview 1 %>
<p class="small text-body-secondary">The image above refreshes once per second and may appear choppy.
To see a smooth video feed from the camera use one of the <a href="majestic-endpoints.cgi" target="_blank">video endpoints</a>.
</div>
<div class="col-md-4 col-xl-3 col-xxl-3">
<div class="d-grid gap-2 mb-3">
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="email">Send to email</button>
<div class="input-group-text">
<a href="plugin-send2email.cgi" title="Email settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="ftp">Send to FTP</button>
<div class="input-group-text">
<a href="plugin-send2ftp.cgi" title="FTP Storage settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="telegram">Send to Telegram</button>
<div class="input-group-text">
<a href="plugin-send2telegram.cgi" title="Telegram bot settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="mqtt">Send to MQTT</button>
<div class="input-group-text">
<a href="plugin-send2mqtt.cgi" title="MQTT settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="webhook">Send to webhook</button>
<div class="input-group-text">
<a href="plugin-send2webhook.cgi" title="Webhook settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button class="form-control btn btn-primary text-start" type="button" data-sendto="yadisk">Send to Yandex Disk</button>
<div class="input-group-text">
<a href="plugin-send2yadisk.cgi" title="Yandex Disk bot settings"><img src="/a/gear.svg" alt="Gear"></a>
</div>
</div>
<div class="input-group">
<button type="button" class="form-control btn btn-primary text-start" id="toggle-night" data-bs-toggle="button">Day/Night Mode</button>
<div class="input-group-text">
<a href="#night-buttons" data-bs-toggle="collapse" data-bs-target="#night-buttons"><img src="/a/chevron-compact-down.svg" alt="Open"></a>
</div>
</div>

<div class="collapse collapsed" id="night-buttons">
<div class="btn-group d-flex" role="group" aria-label="IR LEDs">
<input type="checkbox" class="btn-check" id="toggle-color" value="1">
<label class="btn btn-outline-primary" for="toggle-color" title="ISP Color Mode"><img src="/a/palette.svg" alt="Icon: Color mode"></label>
<input type="checkbox" class="btn-check" id="toggle-ircut" value="1"<% fw_printenv -n gpio_ircut >/dev/null || echo " disabled" %>>
<label class="btn btn-outline-primary" for="toggle-ircut" title="IRCUT Filter"><img src="/a/shadows.svg" alt="Icon: IRCUT filter"></label>
<input type="checkbox" class="btn-check" id="toggle-ir850" value="1"<% fw_printenv -n gpio_ir850 >/dev/null || echo " disabled" %>>
<label class="btn btn-outline-primary" for="toggle-ir850" title="IR LEDs 850 nm"><img src="/a/ir850.svg" alt="Icon: IR 850 LED"></label>
<input type="checkbox" class="btn-check" id="toggle-ir940" value="1"<% fw_printenv -n gpio_ir940 >/dev/null || echo " disabled" %>>
<label class="btn btn-outline-primary" for="toggle-ir940" title="IR LEDs 940 nm"><img src="/a/ir940.svg" alt="Icon: IR 940 LED"></label>
<input type="checkbox" class="btn-check" id="toggle-white" value="1"<% fw_printenv -n gpio_whled >/dev/null || echo " disabled" %>>
<label class="btn btn-outline-primary" for="toggle-white" title="White Light LEDs"><img src="/a/light-on.svg" alt="Icon: White light"></label>
</div>
</div>
</div>
<div class="motor-controls mt-3">
<div class="d-grid gap-2">
	<button class="btn btn-secondary" id="motor-up">Up</button>
	<div class="btn-group" role="group">
		<button class="btn btn-secondary" id="motor-left">Left</button>
		<button class="btn btn-secondary" id="motor-center">Center</button>
		<button class="btn btn-secondary" id="motor-right">Right</button>
	</div>
	<button class="btn btn-secondary" id="motor-down">Down</button>
</div>
</div>
</div>
<script>
const network_address = "<%= $network_address %>";

<% [ "true" != "$email_enabled"    ] && echo "\$('button[data-sendto=email]').disabled = true;" %>
<% [ "true" != "$ftp_enabled"      ] && echo "\$('button[data-sendto=ftp]').disabled = true;" %>
<% [ "true" != "$mqtt_enabled"     ] && echo "\$('button[data-sendto=mqtt]').disabled = true;" %>
<% [ "true" != "$webhook_enabled"  ] && echo "\$('button[data-sendto=webhook]').disabled = true;" %>
<% [ "true" != "$telegram_enabled" ] && echo "\$('button[data-sendto=telegram]').disabled = true;" %>
<% [ "true" != "$yadisk_enabled"   ] && echo "\$('button[data-sendto=yadisk]').disabled = true;" %>

function sendToApi(endpoint) {
	const xhr = new XMLHttpRequest();
	xhr.addEventListener("load", reqListener);
	xhr.open("GET", 'http://' + network_address + endpoint);
	xhr.setRequestHeader("Authorization", "Basic " + btoa("admin:"));
	xhr.send();
}

function reqListener(data) {
	console.log(data.responseText);
}

function xhrGet(url) {
	const xhr = new XMLHttpRequest();
	xhr.open('GET', url);
	xhr.send();
}

$$("a[id^=pan-],a[id^=zoom-]").forEach(el => {
	el.addEventListener("click", ev => {
		ev.preventDefault();
		alert("Sorry, this feature does not work, yet!");
	});
});

$$("button[data-sendto]").forEach(el => {
	el.addEventListener("click", ev => {
		ev.preventDefault();
		if (!confirm("Are you sure?")) return false;
		const tgt = ev.target.dataset["sendto"];
		xhrGet("/cgi-bin/send.cgi?to=" + tgt);
	});
});

["color", "ircut"].forEach(n => {
	$("#toggle-" + n).addEventListener("change", ev => {
		mode = (ev.target.checked) ? "on" : "off";
		xhrGet("/cgi-bin/j/" + n + ".cgi?mode=" + mode);
	});
});

[ "ir850", "ir940", "white" ].forEach(n => {
	$("#toggle-" + n).addEventListener("change", ev => {
		mode = (ev.target.checked) ? "on" : "off";
		xhrGet("/cgi-bin/j/irled.cgi?type=" + n + "&mode=" + mode);
	});
});

$("#toggle-night").addEventListener("click", ev => {
	if (ev.target.classList.contains('active')) {
		$("#toggle-color").checked = false;
		$("#toggle-ircut").checked = false;
		["ir850", "ir940", "white"].forEach(n => $("#toggle-" + n).checked = true)
		ev.target.classList.toggle('btn-secondary')
		ev.target.textContent = 'night mode on'
		mode = "night";
	} else {
		$("#toggle-color").checked = true;
		$("#toggle-ircut").checked = true;
		["ir850", "ir940", "white"].forEach(n => $("#toggle-" + n).checked = false)
		ev.target.classList.toggle('btn-secondary')
		ev.target.textContent = 'night mode off'
		mode = "day";
	}
	xhrGet("/cgi-bin/j/night.cgi?mode=" + mode);
});

document.getElementById("motor-up").addEventListener("click", () => moveMotor("up"));
document.getElementById("motor-down").addEventListener("click", () => moveMotor("down"));
document.getElementById("motor-left").addEventListener("click", () => moveMotor("left"));
document.getElementById("motor-right").addEventListener("click", () => moveMotor("right"));
document.getElementById("motor-center").addEventListener("click", () => moveMotor("center"));

function moveMotor(direction) {
    // Define step size and direction for each motor movement
    let xStep = 0, yStep = 0;
    switch(direction) {
        case "up":
            yStep = -100; // Adjust step size as needed
            break;
        case "down":
            yStep = 100;
            break;
        case "left":
            xStep = -100;
            break;
        case "right":
            xStep = 100;
            break;
        case "center":
            // Implement centering logic, possibly resetting to a default position
            xStep = 0; // Example: Reset steps
            yStep = 0;
            break;
    }

    // Construct the endpoint URL with the desired X and Y steps
    const endpoint = `/cgi-bin/motor-control.cgi?x=${xStep}&y=${yStep}`;
    xhrGet(endpoint); // Reuse the existing xhrGet function for simplicity
}
</script>

<%in p/footer.cgi %>
