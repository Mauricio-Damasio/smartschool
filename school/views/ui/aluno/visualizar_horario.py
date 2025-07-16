from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from io import BytesIO

from school.models.academico.aluno import Aluno 
from school.models.relatorio.horario import Horario 

##

#
@login_required
def horario_turma_aluno(request):
    try:
        aluno = Aluno.objects.select_related('turma__curso__escola').get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    horarios = Horario.objects.filter(turma=aluno.turma).order_by('dia_semana', 'hora_inicio')

    dados = {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'horarios': horarios,
    }

    return render(request, 'apps/ui/aluno/perfil/horario_turma.html', dados)


#
#
#

@login_required
def horario_pdf_aluno(request):
    try:
        aluno = Aluno.objects.select_related('turma__curso__escola').get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    horarios = Horario.objects.filter(turma=aluno.turma).order_by('dia_semana', 'hora_inicio')

    html_string = render_to_string('apps/ui/aluno/perfil/horario_pdf.html', {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'horarios': horarios,
    })

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    return HttpResponse(pdf_file, content_type='application/pdf')
