
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from datetime import datetime

from school.models.academico.aluno import Aluno  
from school.models.relatorio.frequencia import Frequencia 




#
#
#
@login_required
def frequencia_aluno(request):
    try:
        aluno = Aluno.objects.select_related('turma__curso__escola').get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')

    total = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    faltas = total - presencas

    dados = {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'frequencias': frequencias,
        'total': total,
        'presencas': presencas,
        'faltas': faltas,
    }

    return render(request, 'apps/ui/aluno/perfil/frequencia.html', dados)
  
  
  
  
  
  #
  #
  #
@login_required
def frequencia_pdf_aluno(request):
    try:
        aluno = Aluno.objects.select_related('turma__curso__escola').get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    frequencias = Frequencia.objects.filter(aluno=aluno).order_by('-data')
    total = frequencias.count()
    presencas = frequencias.filter(presente=True).count()
    faltas = total - presencas

    html_string = render_to_string('apps/ui/aluno/perfil/pdf_frequencia.html', {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'frequencias': frequencias,
        'total': total,
        'presencas': presencas,
        'faltas': faltas,
        'hoje': datetime.today(),
    })

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    return HttpResponse(pdf_file, content_type='application/pdf')

