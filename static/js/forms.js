function mostrarDadosAcesso() {
	document.getElementById("secao-dados-pessoais").classList.add("d-none");
	document.getElementById("secao-dados-acesso").classList.remove("d-none");
}

function mostrarDadosPessoais() {
	document.getElementById("secao-dados-acesso").classList.add("d-none");
	document.getElementById("secao-dados-pessoais").classList.remove("d-none");
}

// Exibir loading ao clicar em Salvar
document.getElementById("btnSalvar").addEventListener("click", function () {
	document.getElementById("iconSalvar").classList.add("d-none");
	document.getElementById("loadingSalvar").classList.remove("d-none");
});

document
	.getElementById("btnSalvarCadastrar")
	.addEventListener("click", function () {
		document.getElementById("iconSalvarCadastrar").classList.add("d-none");
		document
			.getElementById("loadingSalvarCadastrar")
			.classList.remove("d-none");
	});
