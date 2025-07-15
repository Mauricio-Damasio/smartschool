from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from weasyprint import HTML
from django.http import HttpResponse
from datetime import datetime
from school.models.academico.turma import Turma
from school.models.academico.classe import Classe
from school.models.academico.curso import Curso

from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from school.models.academico.aluno import Aluno
from school.models.relatorio.minipauta import MiniPauta
from django.contrib import messages
from school.models.relatorio.trimestre_liberado import TrimestreLiberado



from django.http import JsonResponse,HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json



#################################################

'''def salvar_notas(request):
    if request.method == 'POST':
        for key in request.POST:
            if key.startswith('aluno_'):
                id_aluno = key.split('_')[1]
                aluno = Aluno.objects.get(id=id_aluno)
                turma_id = request.POST.get('turma_id')
                disciplina_id = request.POST.get('disciplina_id')
                trimestre = request.POST.get('trimestre')

                pauta, created = MiniPauta.objects.get_or_create(
                    aluno=aluno,
                    disciplina_id=disciplina_id,
                    turma_id=turma_id,
                    trimestre=trimestre
                )

                av1 = float(request.POST.get(f'av1_{id_aluno}', 0))
                av2 = float(request.POST.get(f'av2_{id_aluno}', 0))
                av3 = float(request.POST.get(f'av3_{id_aluno}', 0))
                av4 = float(request.POST.get(f'av4_{id_aluno}', 0))
                npp = float(request.POST.get(f'npp_{id_aluno}', 0))
                npt = float(request.POST.get(f'npt_{id_aluno}', 0))

                lista_mac = [av1, av2, av3, av4]
                notas_validas = [n for n in lista_mac if n > 0]
                mac = sum(notas_validas) / len(notas_validas) if notas_validas else 0

                mt = round((mac + npp + npt) / 3, 1)

                pauta.av1 = av1
                pauta.av2 = av2
                pauta.av3 = av3
                pauta.av4 = av4
                pauta.npp = npp
                pauta.npt = npt
                pauta.mac = round(mac, 1)
                pauta.mt = mt
                pauta.save()

        return HttpResponse("Notas salvas com sucesso.")
'''





# views.py




#Método que recebe as notas para o salvamento
'''@csrf_exempt
def salvar_mini_pauta(request):
	if request.method == "POST":
		data = json.loads(request.body)
		aluno_id = data.get("aluno_id")
		av1 = data.get("av1") or 0
		av2 = data.get("av2") or 0
		av3 = data.get("av3") or 0
		av4 = data.get("av4") or 0
		npp = data.get("npp") or 0
		npt = data.get("npt") or 0
		mac = data.get("mac") or 0
		mt = data.get("mt") or 0
		exame = data.get("exame") or 0
		mf = data.get("mf") or 0

		aluno = Aluno.objects.get(pk=aluno_id)
		
		# Ajuste para incluir filtros de disciplina, trimestre, etc.
		MiniPauta.objects.update_or_create(
			aluno=aluno,
			trimestre="1º Trimestre",  # Ex: usar dinamicamente depois
			defaults={
				"av1": av1, "av2": av2, "av3": av3, "av4": av4,
				"mac": mac, "npp": npp, "npt": npt, "mt": mt,
				"exame": exame, "media_final": mf,
			}
		)

		return JsonResponse({"status": "ok"})

	return JsonResponse({"error": "Método não permitido"}, status=405)

'''


def mini_pauta_preencher(request):
    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')
    trimestre = request.GET.get('trimestre')

    turmas = Turma.objects.all()
    disciplinas = Disciplina.objects.all()

    alunos = []
    pauta_dict = {}

    if turma_id and disciplina_id and trimestre:
        alunos = Aluno.objects.filter(turma_id=turma_id).order_by('nome')

        pautas = MiniPauta.objects.filter(
            aluno__in=alunos,
            disciplina_id=disciplina_id,
            trimestre=trimestre
        )

        # Dicionário: { aluno_id: pauta }
        pauta_dict = {pauta.aluno_id: pauta for pauta in pautas}

    context = {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'alunos': alunos,
        'pauta_dict': pauta_dict,
        'turma_id': turma_id,
        'disciplina_id': disciplina_id,
        'trimestre': trimestre,
    }

    return render(request, 'apps/instituicao/pautas/minipauta/preencher/preencher_pauta.html', context)




@csrf_exempt
def salvar_mini_pauta(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            aluno_id = data.get("aluno_id")
            disciplina_id = data.get("disciplina_id")
            trimestre = data.get("trimestre")

            MiniPauta.objects.update_or_create(
                aluno_id=aluno_id,
                disciplina_id=disciplina_id,
                trimestre=trimestre,
                defaults={
                    "av1": data.get("av1") or 0,
                    "av2": data.get("av2") or 0,
                    "av3": data.get("av3") or 0,
                    "av4": data.get("av4") or 0,
                    "mac": data.get("mac") or 0,
                    "npp": data.get("npp") or 0,
                    "npt": data.get("npt") or 0,
                    "mt": data.get("mt") or 0,
                    "exame": data.get("exame") or 0,
                    "mf": data.get("mf") or 0,
                }
            )
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)



#################################################

'''def mini_pauta_preencher(request):
    
    pautas = MiniPauta.objects.all()
    
    if request.method == "POST":
        if "filtrar" in request.POST:
            turma_id = request.POST.get("turma")
            disciplina_id = request.POST.get("disciplina")
            trimestre = request.POST.get("trimestre")

            if not (turma_id and disciplina_id and trimestre):
                messages.error(request, "Preencha todos os campos para filtrar.")
                return redirect("school:preenchimento_mini_pauta")

            turma = get_object_or_404(Turma, id=turma_id)
            disciplina = get_object_or_404(Disciplina, id=disciplina_id)
            alunos = Aluno.objects.filter(turma=turma)

          #  try:
               # liberado = TrimestreLiberado.objects.get(
              #      turma=turma, disciplina=disciplina, trimestre=trimestre
             #   ).liberado
            #except TrimestreLiberado.DoesNotExist:
              #  liberado = False

           #if not liberado:
           #     messages.warning(request, f"O {trimestre}º trimestre ainda não está liberado.")
           #     return redirect("school:preenchimento_mini_pauta")

            return render(request, 'apps/instituicao/pautas/minipauta/preencher/preencher_pauta.html', {
                'turma': turma,
                'disciplina': disciplina,
                'trimestre': trimestre,
                'alunos': alunos,
                'modo_preenchimento': True,
                'pautas':pautas,
            })

        elif "salvar_notas" in request.POST:
            turma_id = request.POST.get("turma_id")
            disciplina_id = request.POST.get("disciplina_id")
            trimestre = request.POST.get("trimestre")

            turma = get_object_or_404(Turma, id=turma_id)
            disciplina = get_object_or_404(Disciplina, id=disciplina_id)
            alunos = Aluno.objects.filter(turma=turma)

            for aluno in alunos:
                av1 = request.POST.get(f"av1_{aluno.id}")
                av2 = request.POST.get(f"av2_{aluno.id}")
                av3 = request.POST.get(f"av3_{aluno.id}")
                av4 = request.POST.get(f"av4_{aluno.id}")

                # Validação e conversão
                try:
                    av1 = float(av1) if av1 else 0.0
                    av2 = float(av2) if av2 else 0.0
                    av3 = float(av3) if av3 else 0.0
                    av4 = float(av4) if av4 else 0.0
                except ValueError:
                    messages.error(request, f"Erro nos dados do aluno {aluno.nome}.")
                    continue

                # Cálculo da MAC (média das avaliações contínuas)
                mac = round((av1 + av2 + av3 + av4) / 4, 1)

                # Criar ou atualizar a nota
                nota, created = MiniPauta.objects.update_or_create(
                    aluno=aluno,
                    disciplina=disciplina,
                    trimestre=trimestre,
                    defaults={
                        'av1': av1,
                        'av2': av2,
                        'av3': av3,
                        'av4': av4,
                        'mac': mac,
                    }
                )

            messages.success(request, "Notas salvas com sucesso!")
            return redirect("school:preenchimento_mini_pauta")

    # Primeira exibição: tela de filtro
    turmas = Turma.objects.all()
    disciplinas = Disciplina.objects.all()

    return render(request, 'apps/instituicao/pautas/minipauta/preencher/preencher_pauta.html', {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'pautas':pautas,
    })

   
   '''
   
   
   


'''def mini_pauta_preencher(request):
    turmas = Turma.objects.all()
   
    classes = Classe.objects.all()
    cursos = Curso.objects.all()
    professores = Professor.objects.all()
    disciplinas = Disciplina.objects.all() 
    alunos = Aluno.objects.all()

    trimestre = 1
    # Verifica se o trimestre está liberado
   

    return render(request, 'apps/instituicao/pautas/minipauta/preencher_notas.html', {
        'turmas': turmas, 'disciplinas': disciplinas,'classes':classes, 'cursos':cursos, 'professores':professores, 'alunos': alunos, 'trimestre': trimestre
    })'''

# views.py
'''def mini_pauta_preencher(request, turma_id, disciplina_id, trimestre):
    turma = get_object_or_404(Turma, id=turma_id)
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    alunos = Aluno.objects.filter(turma=turma)

    # Verifica se o trimestre está liberado
    try:
        liberado = TrimestreLiberado.objects.get(
            turma=turma, disciplina=disciplina, trimestre=trimestre
        ).liberado
    except TrimestreLiberado.DoesNotExist:
        liberado = False

    if not liberado:
        messages.warning(request, f"O {trimestre}º trimestre ainda não está liberado para preenchimento.")
        return redirect('painel_professor')

    # Preenchimento e salvamento normal
    if request.method == "POST":
        for aluno in alunos:
            # captura e salva dados como antes
            ...
        return redirect('mini_pauta_visualizar', turma_id=turma.id, disciplina_id=disciplina.id)

    return render(request, 'apps/instituicao/pautas/minipauta/minipauta_preencher.html', {
        'turma': turma, 'disciplina': disciplina, 'alunos': alunos, 'trimestre': trimestre
    })
'''