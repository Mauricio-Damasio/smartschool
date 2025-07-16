import json
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from school.models.academico.aluno import Aluno
from school.models.academico.professor import Professor
from school.models.academico.turma import Turma
from school.models.academico.disciplina import Disciplina
from school.models.relatorio.minipauta import MiniPauta
from django.views.decorators.http import require_POST

#
#PDF 
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from django.http import HttpResponse, HttpResponseBadRequest
import datetime
# #
from django.contrib import messages
from school.models.relatorio.trimestre_liberado import TrimestreLiberado

#
#
#
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from school.models.academico.disciplinaLecionada import DisciplinaLecionada



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q


TRIMESTRES = [
    (1, "1º Trimestre"),
    (2, "2º Trimestre"),
    (3, "3º Trimestre"),
]

@login_required
def mini_pauta_preencher(request):
    professor = get_object_or_404(Professor, user=request.user)

    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')
    trimestre = request.GET.get('trimestre')

    # Buscar turmas que o professor leciona via DisciplinaLecionada
    turmas = Turma.objects.filter(
        id__in=DisciplinaLecionada.objects.filter(
            professor=professor
        ).values_list('turma__id', flat=True)
    ).distinct()

    # Buscar disciplinas que ele leciona 'por turma associada'
    disciplinas = Disciplina.objects.filter(
        id__in=DisciplinaLecionada.objects.filter(
            professor=professor
        ).values_list('disciplina__id', flat=True)
    ).distinct()

    alunos = []
    pauta_dict = {}
    trimestre_liberado = False

    if turma_id and disciplina_id and trimestre:
        # Verificar se o professor realmente leciona esta disciplina nesta turma
        relacao = DisciplinaLecionada.objects.filter(
            professor=professor,
            turma__id=turma_id,
            disciplina__id=disciplina_id
        ).first()

        if relacao:
            # Verificar se o trimestre está desbloqueado
            desbloqueio = TrimestreLiberado.objects.filter(
                turma__id=turma_id,
                disciplina__id=disciplina_id,
                trimestre=int(trimestre)
            ).first()

            if desbloqueio and desbloqueio.liberado:
                trimestre_liberado = True
                alunos = Aluno.objects.filter(turma__id=turma_id).order_by('nome')
                pautas = MiniPauta.objects.filter(
                    aluno__in=alunos,
                    disciplina_id=disciplina_id,
                    trimestre=trimestre,
                    professor=professor
                )
                pauta_dict = {pauta.aluno_id: pauta for pauta in pautas}
            else:
                messages.error(request, "Este trimestre está bloqueado para esta turma e disciplina.")
        else:
            messages.error(request, "Você não leciona esta disciplina nesta turma.")

    context = {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'trimestres': TRIMESTRES,
        'alunos': alunos,
        'pauta_dict': pauta_dict,
        'turma_id': turma_id,
        'disciplina_id': disciplina_id,
        'trimestre': trimestre,
        'trimestre_liberado': trimestre_liberado,
    }

    return render(request, 'apps/ui/professor/notas/preencher_minipauta.html', context)









#
# Salvar mini pauta
#
@csrf_protect  
@require_POST
def salvar_mini_pauta(request):
    print(">>> Salvar_mini_pauta com método:", request.method)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    aluno_id = data.get("aluno_id")
    disciplina_id = data.get("disciplina_id")
    trimestre = data.get("trimestre")
    turma_id = request.GET.get("turma")

    try:
        professor = Professor.objects.get(user=request.user)
    except Professor.DoesNotExist:
        return JsonResponse({'erro': 'Professor não encontrado.'}, status=404)

    if not all([aluno_id, disciplina_id, trimestre, turma_id]):
        return JsonResponse({"error": "Dados incompletos"}, status=400)

    try:
        aluno = Aluno.objects.get(id=aluno_id)
        disciplina = Disciplina.objects.get(id=disciplina_id)
        turma = Turma.objects.get(id=turma_id)
    except:
        return JsonResponse({"error": "Aluno, Disciplina ou Turma inválidos"}, status=400)

    campos_validos = ["av1", "av2", "av3", "av4", "mac", "npp", "npt", "mt", "exame", "mf"]
    defaults = {k: data.get(k) for k in campos_validos if data.get(k) not in [None, '']}

    MiniPauta.objects.update_or_create(
        aluno=aluno,
        disciplina=disciplina,
        turma=turma,
        trimestre=trimestre,
        professor=professor,
        defaults=defaults
    )

    return JsonResponse({"mensagem": "Notas salvas com sucesso!"})










#




def mini_pauta_pdf(request):
    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')

    if not turma_id or not disciplina_id:
        return HttpResponseBadRequest("Parâmetros ausentes.")

    try:
        turma = Turma.objects.get(id=turma_id)
        disciplina = Disciplina.objects.get(id=disciplina_id)
    except (Turma.DoesNotExist, Disciplina.DoesNotExist):
        return HttpResponseBadRequest("Turma ou Disciplina inválida.")

    alunos = Aluno.objects.filter(turma=turma).order_by('nome')
    pautas = MiniPauta.objects.filter(turma=turma, disciplina=disciplina)

    # Debug: Verificar pautas existentes
    for p in pautas:
        print(p.aluno.nome, p.trimestre, p.mt)

    alunos_dados = []
    aprovados = 0
    reprovados = 0
    nao_avaliados = 0

    for numero, aluno in enumerate(alunos, start=1):
        trimestres_data = {}
        medias_trimestrais = []

        for idx in range(1, 4):  # Trimestres: 1, 2, 3
            pauta = pautas.filter(aluno=aluno, trimestre=idx).first()
            if pauta:
                mt = pauta.mt or 0
                trimestres_data[str(idx)] = pauta
                medias_trimestrais.append(mt)
            else:
                trimestres_data[str(idx)] = None

        # Calcular Média Final (MF)
        if medias_trimestrais:
            mf = round(sum(medias_trimestrais) / len(medias_trimestrais), 1)
        else:
            mf = None

        # Atualizar contagens
        if mf is None:
            nao_avaliados += 1
        elif mf >= 10:
            aprovados += 1
        else:
            reprovados += 1

        alunos_dados.append({
            'numero': numero,
            'aluno': aluno,
            'trimestres': trimestres_data,
            'mf': mf
        })

    context = {
        'turma': turma,
        'disciplina': disciplina,
        'ano_letivo': "2024-2025",
        'alunos_dados': alunos_dados,
        'trimestres': ['1', '2', '3'],  # usado no template
        'aprovados': aprovados,
        'reprovados': reprovados,
        'nao_avaliados': nao_avaliados,
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
        'professor': getattr(request.user.professor, 'nome', '---'),
        'escola': request.user.professor.departamento.curso.escola,
         'dia':  datetime.date.today().strftime("%d de %B de %Y"),
    }

    html_string = render_to_string('apps/ui/professor/notas/mini_pauta_pdf.html', context)
    pdf_file = HTML(string=html_string).write_pdf()

    return HttpResponse(pdf_file, content_type='application/pdf')
