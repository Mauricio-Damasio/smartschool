from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from school.models.academico.aluno import Aluno
from school.models.academico.turma import Turma
from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from school.models.academico.coordenador import Coordenador
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from io import BytesIO



##

#


@login_required
def professores_do_curso_coordenado(request):
    turma_selecionada = None
    professores_com_disciplinas = {}

    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
        turmas = Turma.objects.filter(curso=curso)
    except Coordenador.DoesNotExist:
        curso = None
        turmas = []

    if request.method == 'GET' and request.GET.get('turma_id'):
        turma_id = request.GET.get('turma_id')
        turma_selecionada = Turma.objects.filter(id=turma_id, curso=curso).first()
        if turma_selecionada:
            # Buscar as relações professor-turma-disciplina da turma selecionada
            relacoes = DisciplinaLecionada.objects.select_related('professor', 'disciplina') \
                        .filter(turma=turma_selecionada)

            for rel in relacoes:
                if rel.professor not in professores_com_disciplinas:
                    professores_com_disciplinas[rel.professor] = []
                professores_com_disciplinas[rel.professor].append(rel.disciplina)

    dados = {
        'curso': curso,
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'professores_com_disciplinas': professores_com_disciplinas,
    }
    return render(request, 'apps/ui/coordenador/funcoes/professores_do_curso.html', dados)



##
#PDF

@login_required
def gerar_pdf_professores(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    turma_id = request.GET.get('turma_id')
    turma = Turma.objects.filter(id=turma_id, curso=curso).first()

    if not turma:
        return HttpResponse("Turma inválida ou não pertence ao seu curso.", status=400)

    # Buscar todas as disciplinas lecionadas da turma
    disciplinas_lecionadas = DisciplinaLecionada.objects.select_related('professor', 'disciplina').filter(
        turma=turma
    )

    # Organizar os dados em um dicionário: {professor: [disciplinas]}
    professores_com_disciplinas = {}
    for item in disciplinas_lecionadas:
        professor = item.professor
        disciplina = item.disciplina

        if professor not in professores_com_disciplinas:
            professores_com_disciplinas[professor] = []
        professores_com_disciplinas[professor].append(disciplina)

    # Renderizar o HTML
    html_string = render_to_string('apps/ui/coordenador/funcoes/professores_pdf.html', {
        'curso': curso,
        'turma': turma,
        'professores_com_disciplinas': professores_com_disciplinas,
    })

    # Gerar o PDF
    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = BytesIO()
    html.write_pdf(target=result)
    result.seek(0)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=professores_{turma.nome}.pdf'
    return response




#############################################################
#
#Alunos
#

@login_required
def alunos_do_curso_coordenado(request):
    alunos = []
    turma_selecionada = None

    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
        turmas = Turma.objects.filter(curso=curso)
    except Coordenador.DoesNotExist:
        curso = None
        turmas = []

    if request.method == 'GET' and 'turma_id' in request.GET and request.GET['turma_id']:
        turma_id = request.GET.get('turma_id')
        turma_selecionada = Turma.objects.filter(id=turma_id, curso=curso).first()
        if turma_selecionada:
            alunos = Aluno.objects.filter(turma=turma_selecionada).select_related('turma')

    dados = {
        'curso': curso,
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'alunos': alunos,
    }
    return render(request, 'apps/ui/coordenador/funcoes/alunos_do_curso.html', dados)




#
#PDF Alunos
#

@login_required
def gerar_pdf_alunos_filtrados(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    turma_id = request.GET.get('turma_id')
    turma = Turma.objects.filter(id=turma_id, curso=curso).first()

    if not turma:
        return HttpResponse("Turma inválida ou não pertence ao seu curso.", status=400)

    alunos = Aluno.objects.filter(turma=turma).select_related('turma')

    html_string = render_to_string('apps/ui/coordenador/funcoes/alunos_pdf.html', {
        'curso': curso,
        'turma': turma,
        'alunos': alunos,
    })

    html = HTML(string=html_string)
    result = BytesIO()
    html.write_pdf(target=result)
    result.seek(0)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=alunos_{turma.nome}.pdf'

    return response
