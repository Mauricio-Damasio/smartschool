from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from weasyprint import HTML
from io import BytesIO
from django.template.loader import render_to_string
from school.models.academico.aluno import Aluno
from school.models.relatorio.minipauta import MiniPauta




#
#Notas
#
@login_required
def minhas_notas(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    notas = MiniPauta.objects.filter(aluno=aluno).select_related('disciplina', 'professor').order_by('trimestre')

    dados = {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'notas': notas
    }
    return render(request, 'apps/ui/aluno/perfil/minhas_notas.html', dados)



#
# NOTAS PDF
#

@login_required
def gerar_pdf_notas_aluno(request):
    try:
        aluno = Aluno.objects.get(user=request.user)
    except Aluno.DoesNotExist:
        return HttpResponse("Aluno não encontrado.", status=404)

    notas = MiniPauta.objects.filter(aluno=aluno).select_related('disciplina', 'professor').order_by('trimestre')

    html_string = render_to_string('apps/ui/aluno/perfil/notas_pdf.html', {
        'aluno': aluno,
        'turma': aluno.turma,
        'curso': aluno.turma.curso,
        'escola': aluno.turma.curso.escola,
        'notas': notas
    })

    html = HTML(string=html_string)
    result = BytesIO()
    html.write_pdf(target=result)
    result.seek(0)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=notas_{aluno.nome}.pdf'
    return response
