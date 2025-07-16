from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from school.models.academico.aluno import Aluno
from school.models.academico.turma import Turma
from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from school.models.relatorio.minipauta import MiniPauta 
from school.models.academico.coordenador import Coordenador
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from io import BytesIO




#
#
#

@login_required
def rendimento_professores(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    # Apenas turmas do curso coordenado
    turmas = Turma.objects.filter(curso=curso)

    turma_id = request.GET.get('turma_id')
    turma_selecionada = turmas.filter(id=turma_id).first() if turma_id else None

    rendimentos = []

    if turma_selecionada:
        # Pega todas as disciplinas lecionadas na turma, com seus professores
        disciplinas_lecionadas = DisciplinaLecionada.objects.filter(
            turma=turma_selecionada
        ).select_related('professor', 'disciplina')

        for item in disciplinas_lecionadas:
            professor = item.professor
            disciplina = item.disciplina

            # Filtra MiniPauta dos alunos da turma e disciplina, com esse professor
            notas = MiniPauta.objects.filter(
                turma=turma_selecionada,
                disciplina=disciplina,
                professor=professor
            ).select_related('aluno')

            rendimentos.append({
                'professor': professor,
                'disciplina': disciplina,
                'notas': notas,
            })

    contexto = {
        'curso': curso,
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'rendimentos': rendimentos,
    }

    return render(request, 'apps/ui/coordenador/relatorio/rendimento_professores.html', contexto)



#
# PDF
#


@login_required
def gerar_pdf_rendimento_professores(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    turma_id = request.GET.get('turma_id')
    turma = Turma.objects.filter(id=turma_id, curso=curso).first()

    if not turma:
        return HttpResponse("Turma inválida ou não pertence ao seu curso.", status=400)

    disciplinas_lecionadas = DisciplinaLecionada.objects.filter(
        turma=turma
    ).select_related('professor', 'disciplina')

    rendimentos = []

    for item in disciplinas_lecionadas:
        professor = item.professor
        disciplina = item.disciplina

        notas = MiniPauta.objects.filter(
            turma=turma,
            disciplina=disciplina,
            professor=professor
        ).select_related('aluno')

        rendimentos.append({
            'professor': professor,
            'disciplina': disciplina,
            'notas': notas,
        })

    html_string = render_to_string('apps/ui/coordenador/relatorio/rendimento_professores_pdf.html', {
        'curso': curso,
        'turma': turma,
        'rendimentos': rendimentos,
    })

    result = BytesIO()
    HTML(string=html_string).write_pdf(target=result)
    result.seek(0)

    response = HttpResponse(result.read(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=rendimento_{turma.nome}.pdf'
    return response
