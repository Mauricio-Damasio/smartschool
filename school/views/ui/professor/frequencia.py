# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from school.models.academico.aluno import Aluno
from school.models.academico.professor import Professor
from school.models.academico.turma import Turma
from school.models.relatorio.frequencia import Frequencia
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.utils import timezone

from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Q
from django.utils.dateparse import parse_date
from weasyprint import HTML
from django.http import HttpResponse
from django.template.loader import render_to_string
import datetime






##
#
#
@login_required
def registrar_frequencia(request):
    professor = Professor.objects.get(user=request.user)
    turmas_ids = DisciplinaLecionada.objects.filter(professor=professor).values_list('turma_id', flat=True).distinct()
    turmas = Turma.objects.filter(id__in=turmas_ids)

    turma_selecionada = request.GET.get('turma')
    alunos = []

    if turma_selecionada:
        alunos = Aluno.objects.filter(turma_id=turma_selecionada)

    if request.method == 'POST':
        data = timezone.now().date()
        turma_id = request.POST.get('turma')
        for aluno in alunos:
            status = request.POST.get(f'presente_{aluno.id}') == 'on'
            Frequencia.objects.create(
                aluno=aluno,
                turma_id=turma_id,
                professor=professor,
                data=data,
                presente=status
            )
        return redirect('school:registrar_frequencia')  

    context = {
        'turmas': turmas,
        'alunos': alunos,
        'turma_selecionada': turma_selecionada,
    }
    return render(request, 'apps/ui/professor/frequencia/frequencia.html', context)






#
##
#PDF
#



@login_required
def relatorio_frequencia(request):
    professor = Professor.objects.get(user=request.user)
    turmas_ids = DisciplinaLecionada.objects.filter(professor=professor).values_list('turma_id', flat=True).distinct()
    turmas = Turma.objects.filter(id__in=turmas_ids)

    turma_id = request.GET.get('turma')
    data_inicio_str = request.GET.get('inicio')
    data_fim_str = request.GET.get('fim')
    exportar_pdf = request.GET.get('pdf') == '1'

    relatorio = []
    turma = None
    data_inicio = data_fim = None

    if turma_id and data_inicio_str and data_fim_str:
        try:
            data_inicio = datetime.datetime.strptime(data_inicio_str, "%Y-%m-%d").date()
            data_fim = datetime.datetime.strptime(data_fim_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Formato de data inválido. Use AAAA-MM-DD.")
            return redirect(request.path)

        try:
            turma = Turma.objects.get(id=turma_id)
        except Turma.DoesNotExist:
            messages.error(request, "Turma não encontrada.")
            return redirect(request.path)

        alunos = Aluno.objects.filter(turma=turma)

        for aluno in alunos:
            total = Frequencia.objects.filter(
                aluno=aluno,
                data__range=(data_inicio, data_fim)
            ).count()

            presentes = Frequencia.objects.filter(
                aluno=aluno,
                data__range=(data_inicio, data_fim),
                presente=True
            ).count()

            porcentagem = (presentes / total) * 100 if total > 0 else 0

            relatorio.append({
                'aluno': aluno,
                'total': total,
                'presentes': presentes,
                'porcentagem': round(porcentagem, 2)
            })

    context = {
        'turmas': turmas,
        'relatorio': relatorio,
        'data_inicio': data_inicio_str,
        'data_fim': data_fim_str,
        'turma_id': turma_id,
        'turma': turma
    }

    if exportar_pdf and turma:
        html_string = render_to_string("apps/ui/professor/frequencia/pdf_frequencia.html", context)
        html = HTML(string=html_string)
        pdf = html.write_pdf()
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"Relatorio_Frequencia_{turma.nome}.pdf"
        response['Content-Disposition'] = f'inline; filename="{filename}"'
        return response

    return render(request, "apps/ui/professor/frequencia/frequencia_relatorio.html", context)
