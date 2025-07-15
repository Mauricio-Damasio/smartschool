# views.py
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from datetime import datetime
from school.models.academico.turma import Turma
from school.models.academico.disciplina import Disciplina
from school.models.academico.professor import Professor
from school.models.academico.aluno import Aluno
from school.models.relatorio.minipauta import MiniPauta

def gerar_pdf_mini_pauta(request, turma_id, disciplina_id):
    turma = Turma.objects.get(id=turma_id)
    disciplina = Disciplina.objects.get(id=disciplina_id)
    professor = Professor.objects.get(disciplinas=disciplina, turmas=turma)

    pautas = MiniPauta.objects.filter(turma=turma, disciplina=disciplina).select_related('aluno')
    
    # Lógica de classificação
    aprovados = pautas.filter(mt__gte=10).count()
    reprovados = pautas.filter(mt__lt=10, mt__gt=0).count()
    nao_avaliados = pautas.filter(mt=0).count()

    html_string = render_to_string('mini_pauta/mini_pauta_pdf.html', {
        'turma': turma,
        'disciplina': disciplina,
        'professor': professor,
        'ano': datetime.now().year,
        'pautas': pautas,
        'aprovados': aprovados,
        'reprovados': reprovados,
        'nao_avaliados': nao_avaliados,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Mini_Pauta.pdf"'
    HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(response)
    return response
