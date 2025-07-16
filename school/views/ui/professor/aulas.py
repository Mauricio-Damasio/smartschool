from django.shortcuts import render,get_object_or_404
from ....models.academico.professor import Professor
from django.contrib.auth.decorators import login_required
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.disciplina import Disciplina
from ....models.academico.escola import Escola
from django.contrib import messages
import re
from datetime import date
from school.models.academico.turma import Turma
from school.models.academico.aluno import Aluno
from school.models.documento.aula_elaborada import AulaElaborada
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from django.template.loader import get_template
from weasyprint import HTML
from django.http import HttpResponse





#
# AULAS DO PROFESSOR
#
@login_required
def aulas_do_professor(request):
    professor = get_object_or_404(Professor, user=request.user)

    relacoes = DisciplinaLecionada.objects.filter(professor=professor).select_related('disciplina', 'turma')

    return render(request, 'apps/ui/professor/aula/listar_aulas.html', {
        'relacoes': relacoes,
        'professor': professor,
    })




#
# ELABORAR AULAS
#


@login_required
def elaborar_aula(request, disciplina_id, turma_id):
  
    professor = get_object_or_404(Professor, user=request.user)
    disciplina = get_object_or_404(Disciplina, id=disciplina_id)
    turma = get_object_or_404(Turma, id=turma_id)

    # Verifica se o professor tem permissão
    if not DisciplinaLecionada.objects.filter(
        professor=professor,
        disciplina=disciplina,
        turma=turma
    ).exists():
        messages.error(request, "Você não tem permissão para lecionar essa disciplina nesta turma.")
        return redirect('school:aulas_do_professor')

    if request.method == 'POST':
        tema = request.POST.get('tema')
        subtema = request.POST.get('subtema')
        objetivos = request.POST.get('objetivos')
        conteudo = request.POST.get('conteudo')
        metodologia = request.POST.get('metodologia')
        recursos = request.POST.get('recursos')
        avaliacao = request.POST.get('avaliacao')

        aula = AulaElaborada.objects.create(
            professor=professor,
            disciplina=disciplina,
            turma=turma,
            tema=tema,
            subtema=subtema,
            objetivos=objetivos,
            conteudo=conteudo,
            metodologia=metodologia,
            recursos=recursos,
            avaliacao=avaliacao,
        )

        messages.success(request, "Aula elaborada com sucesso.")
        return redirect('school:exportar_aula_pdf', aula_id=aula.id)

    return render(request, 'apps/ui/professor/aula/elaborar_aula.html', {
        'professor': professor,
        'disciplina': disciplina,
        'turma': turma,
    })



#
#  PDF AULA
#


@login_required
def exportar_aula_pdf(request, aula_id):
    # Garante que a aula pertence ao professor logado
    aula = get_object_or_404(AulaElaborada, id=aula_id, professor__user=request.user)

    # Obtém o professor logado
    professor = get_object_or_404(Professor, user=request.user)


    escola = professor.departamento.curso.escola

    #PDF
    template = get_template('apps/ui/professor/aula/aula_pdf.html')
    html = template.render({'aula': aula, 'escola': escola})

    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=aula_{aula.id}.pdf'
    return response






#
#
#
#VISUALIZAR ALUNOS 
#
#







@login_required
def visualizar_alunos_professor(request):
    professor = Professor.objects.get(user=request.user)

    # Turmas que o professor leciona
    turmas_ids = DisciplinaLecionada.objects.filter(professor=professor).values_list('turma_id', flat=True).distinct()
    turmas = Turma.objects.filter(id__in=turmas_ids)

    turma_id = request.GET.get('turma')  # Parâmetro da filtragem
    alunos_por_turma = []

    if turma_id:
        turma = Turma.objects.filter(id=turma_id, id__in=turmas_ids).first()
        if turma:
            alunos = Aluno.objects.filter(turma=turma)
            alunos_por_turma.append({'turma': turma, 'alunos': alunos})
    else:
        # Mostrar todas as turmas
        for turma in turmas:
            alunos = Aluno.objects.filter(turma=turma)
            alunos_por_turma.append({'turma': turma, 'alunos': alunos})

    context = {
        'professor': professor,
        'turmas': turmas,
        'alunos_por_turma': alunos_por_turma,
        'turma_selecionada': int(turma_id) if turma_id else None,
    }
    return render(request, 'apps/ui/professor/alunos/alunos_por_turma.html', context)





#
#
#


@login_required
def exportar_alunos_pdf(request, turma_id):
    professor = get_object_or_404(Professor, user=request.user)

    # Garantir que essa turma pertence ao professor
    turmas_ids = DisciplinaLecionada.objects.filter(professor=professor).values_list('turma_id', flat=True)
    turma = get_object_or_404(Turma, id=turma_id, id__in=turmas_ids)

    alunos = Aluno.objects.filter(turma=turma)
    
    escola = professor.departamento.curso.escola
    
    dados = {
      'turma': turma, 
      'alunos': alunos, 
      'professor': professor,
      'escola': escola,
      'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
      'data_hoje': date.today().strftime('%d/%m/%Y'),
    }

    template = get_template('apps/ui/professor/alunos/alunos_pdf.html')
    html = template.render(dados)

    pdf_file = HTML(string=html).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=alunos_turma_{turma.nome}.pdf'
    return response
