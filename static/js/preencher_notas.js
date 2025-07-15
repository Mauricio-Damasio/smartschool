document.addEventListener("DOMContentLoaded", () => {
	const inputs = document.querySelectorAll(".nota-input, .exame-input");

	inputs.forEach((input) => {
		input.addEventListener("input", () => {
			const alunoId = input.dataset.id;
			calcularLinha(alunoId);
			salvarNotas(alunoId);
		});
	});
});

function calcularLinha(id) {
	const avs = [1, 2, 3, 4].map(
		(i) =>
			parseFloat(document.querySelector(`[name="av${i}_${id}"]`)?.value) || 0
	);

	const mac =
		avs.filter((n) => n > 0).reduce((a, b) => a + b, 0) /
		(avs.filter((n) => n > 0).length || 1);
	const macField = document.querySelector(`[name="mac_${id}"]`);
	macField.value = mac.toFixed(1);

	const npp =
		parseFloat(document.querySelector(`[name="npp_${id}"]`)?.value) || 0;
	const npt =
		parseFloat(document.querySelector(`[name="npt_${id}"]`)?.value) || 0;

	const mt = (mac + npp + npt) / 3;
	const mtField = document.querySelector(`[name="mt_${id}"]`);
	mtField.value = mt.toFixed(1);

	const exame = parseFloat(document.querySelector(`#exame_${id}`)?.value) || 0;
	const mf = ((mac + exame) / 2).toFixed(1);
	const mfField = document.querySelector(`#media_final_${id}`);
	if (mfField) mfField.value = mf;

	const icon = document.querySelector(`#icon_resultado_${id}`);
	if (icon) {
		icon.innerHTML =
			mf >= 10
				? `<i class="bi bi-check-circle-fill text-success"></i>`
				: `<i class="bi bi-x-circle-fill text-danger"></i>`;
	}

	[
		...avs.map((_, i) => document.querySelector(`[name="av${i + 1}_${id}"]`)),
		document.querySelector(`[name="npp_${id}"]`),
		document.querySelector(`[name="npt_${id}"]`),
		macField,
		mtField,
	].forEach(validarCampo);
}

function validarCampo(input) {
	if (!input) return;
	const valor = parseFloat(input.value);
	if (!isNaN(valor) && valor >= 0 && valor <= 20) {
		input.classList.remove("is-invalid");
		input.classList.add("is-valid");
	} else {
		input.classList.remove("is-valid");
		input.classList.add("is-invalid");
	}
}

// Enviar dados via AJAX
/*function salvarNotas(id) {
	const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

	const spinner = document.querySelector(`#spinner_${id}`);
	if (spinner) spinner.style.display = "inline-block"; // Mostra o spinner

	const data = {
		aluno_id: id,
		av1: document.querySelector(`[name="av1_${id}"]`)?.value,
		av2: document.querySelector(`[name="av2_${id}"]`)?.value,
		av3: document.querySelector(`[name="av3_${id}"]`)?.value,
		av4: document.querySelector(`[name="av4_${id}"]`)?.value,
		npp: document.querySelector(`[name="npp_${id}"]`)?.value,
		npt: document.querySelector(`[name="npt_${id}"]`)?.value,
		mac: document.querySelector(`[name="mac_${id}"]`)?.value,
		mt: document.querySelector(`[name="mt_${id}"]`)?.value,
		exame: document.querySelector(`#exame_${id}`)?.value,
		mf: document.querySelector(`#media_final_${id}`)?.value,
	};

	fetch("/salvar-mini-pauta/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
		body: JSON.stringify(data),
	})
		.then((response) => {
			if (!response.ok) throw new Error("Erro ao salvar!");
			return response.json();
		})
		.then((json) => {
			console.log("✔️ Salvo com sucesso para aluno", id);
		})
		.catch((error) => {
			console.error("❌ Erro ao salvar:", error);
		});
}
*/
function salvarNotas(id) {
	const spinner = document.querySelector(`#spinner_${id}`);
	if (spinner) spinner.style.display = "inline-block"; // Mostra o spinner

	const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;

	const data = {
		aluno_id: id,
		av1: document.querySelector(`[name="av1_${id}"]`)?.value,
		av2: document.querySelector(`[name="av2_${id}"]`)?.value,
		av3: document.querySelector(`[name="av3_${id}"]`)?.value,
		av4: document.querySelector(`[name="av4_${id}"]`)?.value,
		npp: document.querySelector(`[name="npp_${id}"]`)?.value,
		npt: document.querySelector(`[name="npt_${id}"]`)?.value,
		mac: document.querySelector(`[name="mac_${id}"]`)?.value,
		mt: document.querySelector(`[name="mt_${id}"]`)?.value,
		exame: document.querySelector(`#exame_${id}`)?.value,
		mf: document.querySelector(`#media_final_${id}`)?.value,
	};

	fetch("/salvar-mini-pauta/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrftoken,
		},
		body: JSON.stringify(data),
	})
		.then((response) => {
			if (!response.ok) throw new Error("Erro ao salvar!");
			return response.json();
		})
		.then((json) => {
			console.log("✔️ Salvo com sucesso para aluno", id);
		})
		.catch((error) => {
			console.error("❌ Erro ao salvar:", error);
		})
		.finally(() => {
			if (spinner) spinner.style.display = "none"; // Oculta o spinner
		});
}

/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */
/*************************************************************************** */

/*document.addEventListener("DOMContentLoaded", () => {
	const inputs = document.querySelectorAll(".nota-input, .exame-input");

	inputs.forEach((input) => {
		input.addEventListener("input", () => {
			const alunoId = input.dataset.id;

			// Captura notas
			const av1 =
				parseFloat(document.querySelector(`[name="av1_${alunoId}"]`).value) ||
				0;
			const av2 =
				parseFloat(document.querySelector(`[name="av2_${alunoId}"]`).value) ||
				0;
			const av3 =
				parseFloat(document.querySelector(`[name="av3_${alunoId}"]`).value) ||
				0;
			const av4 =
				parseFloat(document.querySelector(`[name="av4_${alunoId}"]`).value) ||
				0;
			const exame =
				parseFloat(document.querySelector(`#exame_${alunoId}`).value) || 0;

			// Calcular MAC e MF
			const mac = ((av1 + av2 + av3 + av4) / 4).toFixed(1);
			const mf = ((parseFloat(mac) + exame) / 2).toFixed(1);

			// Preencher MAC e MF
			document.querySelector(`#mac_${alunoId}`).value = mac;
			document.querySelector(`#media_final_${alunoId}`).value = mf;

			// Exibir ícone colorido
			const icon = document.querySelector(`#icon_resultado_${alunoId}`);
			if (mf >= 10) {
				icon.innerHTML = `<i class="bi bi-check-circle-fill text-success"></i>`;
			} else {
				icon.innerHTML = `<i class="bi bi-x-circle-fill text-danger"></i>`;
			}
		});
	});
});

//
//
//
//
//
//
//
//
//
//
//
//
//
//
//

function calcularLinha(id) {
	const avs = [1, 2, 3, 4].map(
		(i) =>
			parseFloat(document.querySelector(`[name="av${i}_${id}"]`)?.value) || 0
	);

	const mac =
		avs.filter((n) => n > 0).reduce((a, b) => a + b, 0) /
		(avs.filter((n) => n > 0).length || 1);
	document.querySelector(`[name="mac_${id}"]`).value = mac.toFixed(1);

	const npp =
		parseFloat(document.querySelector(`[name="npp_${id}"]`)?.value) || 0;
	const npt =
		parseFloat(document.querySelector(`[name="npt_${id}"]`)?.value) || 0;

	const mt = (mac + npp + npt) / 3;
	document.querySelector(`[name="mt_${id}"]`).value = mt.toFixed(1);
}

//
//
//
//

function calcularLinha(id) {
	const avs = [1, 2, 3, 4].map(
		(i) =>
			parseFloat(document.querySelector(`[name="av${i}_${id}"]`)?.value) || 0
	);

	const mac =
		avs.filter((n) => n > 0).reduce((a, b) => a + b, 0) /
		(avs.filter((n) => n > 0).length || 1);
	const macField = document.querySelector(`[name="mac_${id}"]`);
	macField.value = mac.toFixed(1);

	const npp =
		parseFloat(document.querySelector(`[name="npp_${id}"]`)?.value) || 0;
	const npt =
		parseFloat(document.querySelector(`[name="npt_${id}"]`)?.value) || 0;

	const mt = (mac + npp + npt) / 3;
	const mtField = document.querySelector(`[name="mt_${id}"]`);
	mtField.value = mt.toFixed(1);

	// Validação visual
	validarCampo(macField);
	validarCampo(mtField);

	for (let i = 1; i <= 4; i++) {
		validarCampo(document.querySelector(`[name="av${i}_${id}"]`));
	}

	validarCampo(document.querySelector(`[name="npp_${id}"]`));
	validarCampo(document.querySelector(`[name="npt_${id}"]`));
}

function validarCampo(input) {
	const valor = parseFloat(input.value);
	if (!isNaN(valor) && valor >= 0 && valor <= 20) {
		input.classList.remove("is-invalid");
		input.classList.add("is-valid");
	} else {
		input.classList.remove("is-valid");
		input.classList.add("is-invalid");
	}
}
*/
