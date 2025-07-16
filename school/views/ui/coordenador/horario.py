from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from school.models.academico.aluno import Aluno
from school.models.academico.turma import Turma
from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from school.models.relatorio.minipauta import MiniPauta 
from school.models.relatorio.horario import Horario
from school.models.academico.coordenador import Coordenador
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
import tempfile
from io import BytesIO

from django.contrib import messages




@login_required
def gerenciar_horarios(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
        turmas = Turma.objects.filter(curso=curso)
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    turma_id = request.GET.get('turma_id')
    turma_selecionada = None
    horarios = []

    if turma_id:
        turma_selecionada = Turma.objects.filter(id=turma_id, curso=curso).first()
        if turma_selecionada:
            horarios = Horario.objects.filter(turma=turma_selecionada).order_by('dia_semana', 'hora_inicio')

    if request.method == 'POST':
        turma_id = request.POST.get('turma')
        disciplina_id = request.POST.get('disciplina')
        professor_id = request.POST.get('professor')
        tipo = request.POST.get('tipo')
        dia = request.POST.get('dia_semana')
        inicio = request.POST.get('hora_inicio')
        fim = request.POST.get('hora_fim')

        try:
            turma = Turma.objects.get(id=turma_id)
            disciplina = Disciplina.objects.get(id=disciplina_id)
            professor = Professor.objects.get(id=professor_id)

            # Verifica se já existe horário igual
            conflito = Horario.objects.filter(
                turma=turma,
                disciplina=disciplina,
                tipo=tipo,
                dia_semana=dia,
                hora_inicio=inicio
            ).exists()

            if conflito:
                messages.error(request, "Já existe um horário com esses dados.")
            else:
                Horario.objects.create(
                    turma=turma,
                    disciplina=disciplina,
                    professor=professor,
                    tipo=tipo,
                    dia_semana=dia,
                    hora_inicio=inicio,
                    hora_fim=fim
                )
                messages.success(request, "Horário cadastrado com sucesso.")
                return redirect(f"{request.path}?turma_id={turma_id}")

        except (Turma.DoesNotExist, Disciplina.DoesNotExist, Professor.DoesNotExist):
            messages.error(request, "Dados inválidos. Verifique as seleções.")

    disciplinas_lecionadas = DisciplinaLecionada.objects.filter(turma__in=turmas).select_related('disciplina', 'professor', 'turma')

    dados = {
        'curso': curso,
        'turmas': turmas,
        'turma_selecionada': turma_selecionada,
        'horarios': horarios,
        'disciplinas_lecionadas': disciplinas_lecionadas,
    }
    return render(request, 'apps/ui/coordenador/horarios/gerenciar.html', dados)









#
#
#


@login_required
def gerar_pdf_horario_turma(request):
    try:
        coordenador = Coordenador.objects.get(user=request.user)
        curso = coordenador.curso
    except Coordenador.DoesNotExist:
        return HttpResponse("Coordenador não encontrado.", status=404)

    turma_id = request.GET.get('turma_id')
    turma = Turma.objects.filter(id=turma_id, curso=curso).first()

    if not turma:
        return HttpResponse("Turma inválida ou não pertence ao seu curso.", status=400)

    horarios = Horario.objects.filter(turma=turma).select_related('disciplina', 'professor').order_by('dia_semana', 'hora_inicio')

    html_string = render_to_string('apps/ui/coordenador/horarios/horario_pdf.html', {
        'curso': curso,
        'turma': turma,
        'horarios': horarios,
    })

    html = HTML(string=html_string)
    result = BytesIO()
    html.write_pdf(target=result)
    result.seek(0)

    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=horario_{turma.nome}.pdf'
    return response
