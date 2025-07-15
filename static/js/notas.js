document.addEventListener("DOMContentLoaded", () => {
	document.querySelectorAll(".nota").forEach((input) => {
		input.addEventListener("input", calcularLinha);
	});
});

function calcularLinha(e) {
	const row = e.target.closest("tr");
	const alunoId = e.target.dataset.id;
	const inputs = row.querySelectorAll("input");

	const av1 = parseFloat(inputs[0].value) || 0;
	const av2 = parseFloat(inputs[1].value) || 0;
	const av3 = parseFloat(inputs[2].value) || 0;
	const av4 = parseFloat(inputs[3].value) || 0;

	const mac = ((av1 + av2 + av3 + av4) / 4).toFixed(1);
	inputs[4].value = mac;

	const npp = parseFloat(inputs[5].value) || 0;
	const npt = parseFloat(inputs[6].value) || 0;

	const mt = (parseFloat(mac) * 0.4 + npp * 0.2 + npt * 0.4).toFixed(1);
	inputs[7].value = mt;

	const exame = parseFloat(inputs[8].value) || 0;
	const mf = ((parseFloat(mt) + exame) / 2).toFixed(1);
	inputs[9].value = mf;

	const data = {
		aluno_id: alunoId,
		disciplina_id: getParam("disciplina"),
		trimestre: getParam("trimestre"),
		av1,
		av2,
		av3,
		av4,
		mac,
		npp,
		npt,
		mt,
		exame,
		mf,
	};

	fetch("school/salvar-mini-pauta/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": getCookie("csrftoken"),
		},
		body: JSON.stringify(data),
	});
}

function getParam(name) {
	const url = new URL(window.location.href);
	return url.searchParams.get(name);
}

function getCookie(name) {
	let cookie = document.cookie
		.split(";")
		.find((c) => c.trim().startsWith(name + "="));
	return cookie ? decodeURIComponent(cookie.split("=")[1]) : null;
}
