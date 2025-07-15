from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from weasyprint import HTML
import csv
import datetime
from datetime import date
from django.shortcuts import render
from school.models.academico.professor import Professor
from school.models.academico.coordenador import Coordenador
from school.models.academico.escola import Escola
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from school.models.relatorio.assiduidade import Assiduidade
from django.contrib import messages
from django.shortcuts import redirect,get_object_or_404


#Registro de assiduidade
@login_required
def cadastrar_assiduidade(request):
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_administrativo=administrativo).first()
    professores = Professor.objects.filter(departamento__curso__escola=escola)
    coordenadores = Coordenador.objects.filter(curso__escola=escola)

    if request.method == 'POST':
        data = request.POST.get('data')
        hora_entrada = request.POST.get('hora_entrada')
        hora_saida = request.POST.get('hora_saida')
        cargo = request.POST.get('cargo')
        pessoa_id = request.POST.get('pessoa_id')
        observacoes = request.POST.get('observacoes')

        if not all([data, hora_entrada, hora_saida, cargo, pessoa_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/administrativo/RH/cadastrar.html', {
                'professores': professores,
                'coordenadores': coordenadores
            })

        if cargo == 'Professor':
            professor = get_object_or_404(Professor, pk=pessoa_id)
            assiduidade = Assiduidade.objects.create(
                data=data,
                hora_entrada=hora_entrada,
                hora_saida=hora_saida,
                cargo=cargo,
                professor=professor,
                observacoes=observacoes
            )
        else:
            coordenador = get_object_or_404(Coordenador, pk=pessoa_id)
            assiduidade = Assiduidade.objects.create(
                data=data,
                hora_entrada=hora_entrada,
                hora_saida=hora_saida,
                cargo=cargo,
                coordenador=coordenador,
                observacoes=observacoes
            )

        messages.success(request, "Registro de assiduidade cadastrado com sucesso!")
        return redirect('school:assiduidade_relatorio')

    return render(request, 'apps/instituicao/administrativo/RH/cadastrar.html', {
        'professores': professores,
        'coordenadores': coordenadores
    })

    

#Relatório
@login_required
def assiduidade_relatorio(request):
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_administrativo=administrativo).first()

    professores = Professor.objects.filter(departamento__curso__escola=escola)
    coordenadores = Coordenador.objects.filter(curso__escola=escola)

    registros = []
    selecionado = None
    tipo = None

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        pessoa_id = request.POST.get('pessoa_id')
        data_inicio_raw = request.POST.get('data_inicio')
        data_fim_raw = request.POST.get('data_fim')

        # Verifica se as datas são válidas
        try:
            data_inicio = datetime.datetime.strptime(data_inicio_raw, "%Y-%m-%d").date()
            data_fim = datetime.datetime.strptime(data_fim_raw, "%Y-%m-%d").date()

        except (ValueError, TypeError):
            messages.error(request, "Por favor, insira datas válidas no formato AAAA-MM-DD.")
            return render(request, 'apps/instituicao/administrativo/RH/relatorio.html', {
                'professores': professores,
                'coordenadores': coordenadores,
                'registros': registros,
                'selecionado': selecionado,
                'tipo': tipo,
            })

        if data_inicio > data_fim:
            messages.error(request, "A data de início não pode ser posterior à data final.")
            return render(request, 'apps/instituicao/administrativo/RH/relatorio.html', {
                'professores': professores,
                'coordenadores': coordenadores,
                'registros': registros,
                'selecionado': selecionado,
                'tipo': tipo,
            })

        try:
            if tipo == 'professor':
                selecionado = Professor.objects.get(id=pessoa_id)
                registros = Assiduidade.objects.filter(
                    professor=selecionado,
                    data__range=[data_inicio, data_fim]
                )
            elif tipo == 'coordenador':
                selecionado = Coordenador.objects.get(id=pessoa_id)
                registros = Assiduidade.objects.filter(
                    coordenador=selecionado,
                    data__range=[data_inicio, data_fim]
                )
        except Exception as e:
            messages.error(request, "Erro ao buscar dados de assiduidade.")
            print(f"Erro: {e}")

        # Exportar PDF
        if 'export_pdf' in request.POST:
            html_string = render_to_string('apps/instituicao/administrativo/RH/pdf.html', {
                'registros': registros,
                'pessoa': selecionado,
                'tipo': tipo,
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
                'escola': escola,
                'dia': date.today().strftime("%d de %B de %Y"),
            })
            html = HTML(string=html_string)
            pdf = html.write_pdf()
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = f'filename="relatorio_assiduidade_{selecionado.nome}.pdf"'
            return response

        # Exportar CSV
        if 'export_excel' in request.POST:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="relatorio_assiduidade_{selecionado.nome}.csv"'
            writer = csv.writer(response)
            writer.writerow(['Data', 'Entrada', 'Saída', 'Cargo'])
            for r in registros:
                writer.writerow([r.data, r.hora_entrada, r.hora_saida, r.cargo])
            return response

    return render(request, 'apps/instituicao/administrativo/RH/relatorio.html', {
        'professores': professores,
        'coordenadores': coordenadores,
        'registros': registros,
        'selecionado': selecionado,
        'tipo': tipo,
    })
