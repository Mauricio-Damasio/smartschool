from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ....models.academico.ano_lectivo import AnoLetivo 
from ....models.academico.turma import Turma 
from ....models.academico.aluno import Aluno
from weasyprint import HTML
from django.template.loader import render_to_string
import tempfile
import os
from collections import Counter
import datetime


# Selecionando o ano lectivo e ver alunos
@login_required
def relatorio_alunos_por_ano(request: HttpRequest):
    anos = AnoLetivo.objects.all()
    alunos = []
    ano_selecionado = None
    genero_count = {}

    if request.method == 'POST':
        ano_id = request.POST.get('ano_letivo')
        print("Recebido do POST:", ano_id)

        if ano_id:
            try:
                ano_selecionado = get_object_or_404(AnoLetivo, id=ano_id)
                print("Ano selecionado (objeto):", ano_selecionado, type(ano_selecionado))
            except Exception as e:
                print("ERRO ao buscar AnoLetivo:", e)
                raise

            alunos = Aluno.objects.filter(turma__ano_lectivo=ano_selecionado)

    # Contagem por gênero
    genero_count = Counter(aluno.genero for aluno in alunos)
    
    return render(request, 'apps/ui/aluno/relatorio/relatorio_alunos.html', {
        'anos': anos,
        'alunos': alunos,
        'ano_selecionado': ano_selecionado,
        'genero_labels': list(genero_count.keys()),
        'genero_data': list(genero_count.values()),
    })



# Alunos de um determinado ano lectivo

@login_required
def relatorio_alunos_pdf(request: HttpRequest, ano_id: int):
    
    escola = request.user.escola.nome
    
    ano = get_object_or_404(AnoLetivo, id=ano_id)
    alunos = Aluno.objects.filter(turma__ano_lectivo=ano)

    html_string = render_to_string('apps/ui/aluno/relatorio/relatorio_alunos_pdf.html', {
        'alunos': alunos,
        'ano': ano,
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
        'escola': escola,
        'data_emissao': datetime.date.today().strftime("%d de %B de %Y"),
    })

    # 
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    temp_file_path = temp_file.name
    temp_file.close()  

    try:
        HTML(string=html_string).write_pdf(target=temp_file_path)
        with open(temp_file_path, 'rb') as pdf_file:
            pdf = pdf_file.read()
    finally:
        os.remove(temp_file_path) 

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=relatorio_alunos_{ano.nome}.pdf'
    return response

    


