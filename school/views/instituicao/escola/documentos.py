from django.shortcuts import render, get_object_or_404
from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from school.models.academico.aluno import Aluno
from school.models.relatorio.minipauta import MiniPauta
import datetime
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from ....models.academico.turma import Turma
from django.contrib import messages


#Filtar alunos
@login_required
def filtrar_aluno(request: HttpRequest):

    # Obter a escola do usuário logado
    escola = request.user.escola

    # Carregar turmas pertencentes à escola
    turmas = Turma.objects.filter(curso__escola=escola).order_by('nome')

    # Obter o ID da turma selecionada no filtro
    turma_id = request.GET.get('turma')
    nome = request.GET.get('nome')

    # Inicializar alunos da escola
    alunos = Aluno.objects.filter(turma__curso__escola=escola)

    # Aplicar filtro
    if turma_id and nome:
        alunos = alunos.filter(turma_id=turma_id, nome=nome)
    else:
        messages.error(request, 'Selecione a turma e preencha o nome!')
        alunos = Aluno.objects.none()

    # Dados enviados para o template
    dados = {
        'alunos': alunos,
        'turmas': turmas,
    }

    return render(request, 'apps/instituicao/escola/documentos/aluno_filtrado.html', dados)


def gerar_certificado(request, aluno_id):
    aluno = get_object_or_404(Aluno, pk=aluno_id)
    notas = MiniPauta.objects.filter(aluno=aluno)
    
    disciplinas = []
    soma = 0
    for nota in notas:
        disciplinas.append({
            'disciplina': nota.disciplina,
            'nota_final': nota.mt  
        })
        soma += nota.mt or 0
    
    media_final = round(soma / len(notas), 1) if notas else 0
    situacao = "Aprovado" if media_final >= 10 else "Reprovado"

    html_string = render_to_string("apps/instituicao/escola/documentos/certificados.html", {
        'aluno': aluno,
        'curso': aluno.turma.curso,
        'turma': aluno.turma,
        'ano_letivo': "2024/2025",
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
        'notas': disciplinas,
        'media_final': media_final,
        'situacao': situacao,
        'data_emissao': datetime.date.today().strftime("%d de %B de %Y"),
        'escola': request.user.escola,
    })

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="certificado_{aluno.nome}.pdf"'
    return response
