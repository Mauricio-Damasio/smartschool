
from school.models.academico.turma import Turma
from school.models.academico.disciplina import Disciplina
from school.models.relatorio.minipauta import MiniPauta
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render,redirect,get_object_or_404
from school.models.academico.diretor_pedagogico import Pedagogico
from school.models.academico.professor import Professor
from django.contrib import messages
from school.models.academico.escola import Escola
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
from io import BytesIO
import datetime



#@permission_required('pedagogico.ver_relatorios', raise_exception=True)
@login_required
def desempenho(request):
    #
    pedagogico = Pedagogico.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()
    if not escola:
        messages.error(request, "Nenhuma escola vinculada ao seu perfil pedagógico.")
        return redirect('school:dashboard_pedagogico')
    
    turmas = Turma.objects.filter(curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)
    pauta = []

    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')
    trimestre = request.GET.get('trimestre')

    if turma_id and disciplina_id and trimestre:
        pauta = MiniPauta.objects.filter(
            turma_id=turma_id,
            disciplina_id=disciplina_id,
            trimestre=trimestre
        ).select_related('aluno')

    context = {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'pauta': pauta,
        'turma_id': turma_id,
        'disciplina_id': disciplina_id,
        'trimestre': trimestre
    }
    return render(request, 'apps/instituicao/pedagogico/relatorios/desempenho.html', context)



#Desempenho pdf


def desempenho_pdf(request):
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    turma_id = request.GET.get('turma')
    disciplina_id = request.GET.get('disciplina')
    trimestre = request.GET.get('trimestre')

    pauta = MiniPauta.objects.filter(
        turma_id=turma_id,
        disciplina_id=disciplina_id,
        trimestre=trimestre
    ).select_related('aluno')

    turma = Turma.objects.get(id=turma_id)
    disciplina = Disciplina.objects.get(id=disciplina_id)
    

    #Acessando professor de uma determinada disciplina 
    professor = Professor.objects.filter(disciplina=disciplina).first()
    nome_professor = professor.nome if professor else 'Não atribuído'

   

    html_string = render_to_string('apps/instituicao/pedagogico/relatorios/desempenho_pdf.html', {
        'pauta': pauta,
        'turma': turma,
        'disciplina': disciplina,
        'trimestre': trimestre,
        'escola': escola,
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
        'professor': nome_professor,
        'dia':  datetime.date.today().strftime("%d de %B de %Y"),
        'pedagogico': request.user.pedagogico,
    })

    # Geração em memória
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(pdf_file)
    pdf_file.seek(0)

    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="desempenho.pdf"'
    return response
