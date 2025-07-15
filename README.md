{% extends "base/_dashboard_.html" %} {% load static %}

<!---->

{% block title%}

<!---->

Preencher Pauta{% endblock %}

<!---->

{% block content %}

<!---->

<div class="row filtragem mb-5">
	<div class="header mt-2 mb-4">
		<h4 class="col mt-5">Preenchimento da Mini Pauta</h4>
	</div>

    <div class="header-2 mt-3 mb-4">
    	<h4>Listar alunos</h4>
    	<hr />
    </div>

    <!--Begin::filtro -->
    {% include "apps/instituicao/pautas/minipauta/preencher/filtrar.html" %}
    <!--End::Listagem de  -->

    <!--Begin::Messages-->
    {% include "layout/message.html" %}
    <!--End::Messages-->

    {% if alunos.exists %}

    <!---->

    <h6 class="ms-2 mt-4 titulo">Mini Pauta do <strong>{{trimestre}}</strong></h6>
    <h6 class="titulo ms-2">
    	Disciplina: <strong>{{ disciplina.nome }}</strong>
    </h6>
    <h6 class="titulo mb-5 ms-2">
    	Total de alunos: <strong>{{alunos.count}}</strong>
    </h6>

    <!---->
    <!---->

    <form method="post">
    	{% csrf_token %} {% for aluno in alunos %}
    	<div class="list-item mb-2">
    		<div class="item-nota">
    			<!--Preenchimento-->

    			{% include "apps/instituicao/pautas/minipauta/preencher/nota.html" %}
    			<!--End::Preenchimento-->

    			<!--Resultado-->
    			{% load static %}

    			<div class="resultado">
    				<div class="me-4 ms-4">
    					<div class="label-nota">
    						<label for="" class="ms-2">Faltas</label>
    					</div>
    					<div class="input-nota">
    						<input
    							type="number"
    							class=""
    							data-id="{{ pauta.id }}"
    							data-campo="faltas"
    							value="{{ pauta.faltas }}"
    						/>
    					</div>
    				</div>
    				<!---->
    				<div class="me-4 ms-4 mb-3">
    					<div class="label-nota">
    						<label for="" class="ms-3">Comp.</label>
    					</div>
    					<div class="input-nota">
    						<select name="" id="" class="comportamento">
    							<option value="" class="text-danger" id="selecione">
    								Selecione
    							</option>
    							<option value="E" class="text-dark">Excelente</option>
    							<option value="B" class="text-dark">Bom</option>
    							<option value="R" class="text-dark">Razoável</option>
    							<option value="I" class="text-dark">Insatisfatório</option>
    						</select>
    					</div>
    				</div>
    				<!---->

    				<!---->
    				<div class="me-4 ms-4 mb-3">
    					<div class="label-nota">
    						<label for="" class="ms-3">Assid.</label>
    					</div>
    					<div class="input-nota">
    						<select name="" id="" class="assiduidade">
    							<option value="" class="text-danger" id="selecione">
    								Selecione
    							</option>
    							<option value="M" class="text-dark">Muito Boa</option>
    							<option value="B" class="text-dark">Boa</option>
    							<option value="R" class="text-dark">Razoável</option>
    							<option value="F" class="text-dark">Fraca</option>
    						</select>
    						<!--Resultado final-->

    						<span class="ms-1" id="icon_resultado_{{ aluno.id }}"></span>
    					</div>
    				</div>
    				<!---->
    			</div>

    			<!---->
    		</div>
    	</div>

    	{% endfor %}

    	<div class="text-center mb-3">
    		<button type="submit" class="btn btn-primary">Salvar Notas</button>
    	</div>
    </form>

    {% else %}
    <div class="alert alert-danger">Não existe nenhum aluno cadastrado!</div>
    {% endif %}

    <!---->
    <!---->

    {% endblock %}

</div>

<script>
	function calcularLinha(id) {
		const get = (name) =>
			parseFloat(document.querySelector(`[name="${name}_${id}"]`)?.value) || 0;

		const avs = [get("av1"), get("av2"), get("av3"), get("av4")];
		const mac =
			avs.filter((n) => n > 0).reduce((a, b) => a + b, 0) /
			(avs.filter((n) => n > 0).length || 1);
		document.querySelector(`[name="mac_${id}"]`).value = mac.toFixed(1);

		const npp = get("npp");
		const npt = get("npt");
		const mt = (mac + npp + npt) / 3;
		document.querySelector(`[name="mt_${id}"]`).value = mt.toFixed(1);

		const exame = parseFloat(document.querySelector(`#exame_${id}`).value) || 0;
		const mf = ((mac + exame) / 2).toFixed(1);
		document.querySelector(`#media_final_${id}`).value = mf;

		const icon = document.querySelector(`#icon_resultado_${id}`);
		if (mf >= 10) {
			icon.innerHTML = '<i class="bi bi-check-circle-fill text-success"></i>';
		} else {
			icon.innerHTML = '<i class="bi bi-x-circle-fill text-danger"></i>';
		}

		salvarNotas(id, avs, mac, npp, npt, mt, exame, mf);
	}

	function salvarNotas(id, avs, mac, npp, npt, mt, exame, mf) {
		const spinner = document.querySelector(`#spinner_${id}`);
		spinner.classList.remove("d-none");

		fetch("{% url 'school:salvar_mini_pauta' %}", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": "{{ csrf_token }}",
			},
			body: JSON.stringify({
				aluno_id: id,
				disciplina_id: document.querySelector("#disciplina_id").value,
				trimestre: document.querySelector("#trimestre").value,
				av1: avs[0],
				av2: avs[1],
				av3: avs[2],
				av4: avs[3],
				mac: mac,
				npp: npp,
				npt: npt,
				mt: mt,
				exame: exame,
				mf: mf,
			}),
		})
			.then((res) => res.json())
			.then((data) => {
				spinner.classList.add("d-none");
			})
			.catch((err) => {
				spinner.classList.add("d-none");
				alert("Erro ao salvar nota!");
			});
	}
</script>

///////////////////PERSONALIZANDO NAVBAR//////////////////////////////////////////

<div class="nav-item mt-10">
<a
							class="nav-link"
							href="#"
							data-bs-toggle="modal"
							data-bs-target="#customNavbarModal"
						>
<i class="bi bi-palette me-1"></i> Personalizar Navbar
</a>
</div>

css:

.color-option:hover {
outline: 3px solid #000;
}

def home*page(request:HttpRequest):
cores = ["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]
return render(request, "base/\_dashboard*.html", {"cores": cores})

          Abaixo o menu de opções de  cores

/////////////////MODAL/////////////////////////////////////////////////////////////

<!--Modal-->
<div
    		class="modal fade"
    		id="customNavbarModal"
    		tabindex="-1"
    		aria-labelledby="customNavbarLabel"
    		aria-hidden="true"
    	>
<div class="modal-dialog modal-dialog-centered">
<div class="modal-content">
<div class="modal-header">
<h5 class="modal-title" id="customNavbarLabel">
Personalizar Navbar
</h5>
<button
    						type="button"
    						class="btn-close"
    						data-bs-dismiss="modal"
    						aria-label="Fechar"
    					></button>
</div>
<div class="modal-body">
<div class="d-flex flex-wrap gap-2">
<!-- Cores disponíveis -->
<!---->

    						{% for color in cores%}
    						<!---->
    						<div
    							class="color-option rounded-circle border border-dark"
    							data-color="{{ color }}"
    							style="width: 40px; height: 40px; background-color: var(--bs-{{ color }}); cursor: pointer;"
    						></div>
    						{% endfor %}
    					</div>
    				</div>
    			</div>
    		</div>
    	</div>
    	<!--script-->
    	<script>
    		document.addEventListener("DOMContentLoaded", function () {
    			const navbar = document.querySelector("nav.navbar");
    			const colorOptions = document.querySelectorAll(".color-option");

    			// Aplica a cor salva (se existir)
    			const savedColor = localStorage.getItem("navbarColor");
    			if (savedColor) {
    				navbar.classList.add("bg-" + savedColor);
    			} else {
    				navbar.classList.add("bg-primary"); // cor padrão
    			}

    			// Ao clicar em uma cor
    			colorOptions.forEach((option) => {
    				option.addEventListener("click", () => {
    					const color = option.getAttribute("data-color");

    					// Remove classes bg- anteriores
    					navbar.classList.forEach((cls) => {
    						if (cls.startsWith("bg-")) {
    							navbar.classList.remove(cls);
    						}
    					});

    					// Adiciona nova cor
    					navbar.classList.add("bg-" + color);

    					// Salva no localStorage
    					localStorage.setItem("navbarColor", color);

    					// Fecha o modal
    					const modal = bootstrap.Modal.getInstance(
    						document.getElementById("customNavbarModal")
    					);
    					modal.hide();
    				});
    			});
    		});
    	</script>

//////////////////////////////////////////////////////////////////////////////////////////////////////////

    	<!--SCRIPT FULL SCREAN -->

    	<script>
    		document.addEventListener("DOMContentLoaded", function () {
    			const toggleBtn = document.getElementById("fullscreenToggle");
    			const iconMaximize = document.getElementById("icon-maximize");
    			const iconMinimize = document.getElementById("icon-minimize");

    			toggleBtn.addEventListener("click", function (e) {
    				e.preventDefault();

    				if (!document.fullscreenElement) {
    					document.documentElement
    						.requestFullscreen()
    						.then(() => {
    							iconMaximize.classList.add("d-none");
    							iconMinimize.classList.remove("d-none");
    						})
    						.catch((err) => {
    							console.error(`Erro ao entrar em tela cheia: ${err.message}`);
    						});
    				} else {
    					document
    						.exitFullscreen()
    						.then(() => {
    							iconMaximize.classList.remove("d-none");
    							iconMinimize.classList.add("d-none");
    						})
    						.catch((err) => {
    							console.error(`Erro ao sair da tela cheia: ${err.message}`);
    						});
    				}
    			});
    		});
    	</script>

---

AUTENTICAÇÃO

import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpRequest
from django.contrib.auth import authenticate, login

def home_page(request:HttpRequest):
return render(request, 'apps/home/home_page.html')

def sobre_nos(request:HttpRequest):
return render(request, 'apps/webpage/webpage.html')
#######################################################

