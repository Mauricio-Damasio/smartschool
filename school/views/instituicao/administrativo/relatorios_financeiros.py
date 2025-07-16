from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpRequest
from django.db.models import Count
from school.models.relatorio.pagamento import Pagamento
from django.utils.dateparse import parse_date
from school.models.academico.aluno import Aluno
from school.models.academico.curso import Curso
from school.models.academico.turma import Turma
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from school.models.academico.escola import Escola
from weasyprint import HTML
from datetime import date
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages




#
@login_required
def relatorio_dashboard(request):
    alunos_por_curso = Aluno.objects.values('curso__nome').annotate(total=Count('id'))
    alunos_por_turma = Aluno.objects.values('turma__nome').annotate(total=Count('id'))
    pagamentos_atrasados = Pagamento.objects.filter(status='Pendente')

    context = {
        'alunos_por_curso': alunos_por_curso,
        'alunos_por_turma': alunos_por_turma,
        'pagamentos_atrasados': pagamentos_atrasados,
    }

    return render(request, 'administrativo/relatorios/dashboard.html', context)




@login_required
def alunos_por_curso_pdf(request):
    # Obtem o Diretor Administrativo logado
    diretor = DiretorAdministrativo.objects.get(user=request.user)

    # Busca a escola associada a esse diretor
    escola = Escola.objects.filter(direitor_administrativo=diretor).first()

    # Agrupa os alunos por curso da escola
    alunos_por_curso = (
        Aluno.objects
        .filter(turma__curso__escola=escola)
        .values('turma__curso__nome')
        .annotate(total=Count('id'))
        .order_by('turma__curso__nome')
    )
    
    alunos_por_turma = (
        Aluno.objects
        .filter(turma__curso__escola=escola)
        .values('turma__nome')
        .annotate(total=Count('id'))
        .order_by('turma__nome')
    )
    
    dados = {
      
        'alunos_por_curso': alunos_por_curso, 
        'escola': escola, 
        'alunos_por_turma':alunos_por_turma,
        'data_hoje': date.today().strftime('%d/%m/%Y'),
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
    }

    html_string = render_to_string(
        'apps/instituicao/administrativo/RH/financas/relatorio_alunos.html',
       dados
    )

  
    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_alunos_por_curso.pdf"'
    return response






#
#  CASTRO DE PAGAMENTO
#


@login_required
def cadastrar_pagamento(request: HttpRequest):
    
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
    #
    alunos = Aluno.objects.filter(turma__curso__escola=escola)

    if request.method == 'POST':
        aluno_id = request.POST.get('aluno')
        data_pagamento = request.POST.get('data_pagamento')
        valor = request.POST.get('valor')
        mes_referente = request.POST.get('mes_referente')
        status = request.POST.get('status')

        if not all([aluno_id, valor, mes_referente, status]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/administrativo/RH/financas/cadastrar_pagamento.html', {'alunos': alunos})

        aluno = get_object_or_404(Aluno, pk=aluno_id)
        
        Pagamento.objects.create(
            aluno=aluno,
            data_pagamento=data_pagamento if data_pagamento else None,
            valor=valor,
            mes_referente=mes_referente,
            status=status,
        )

        messages.success(request, f'Pagamento de {aluno.nome} cadastrado com sucesso!')
        return redirect('school:cadastrar_pagamento')

    return render(request, 'apps/instituicao/administrativo/RH/financas/cadastrar_pagamento.html', {'alunos': alunos})






#
# PAGAMENTOS PAGOS
#


@login_required
def filtro_pagamento_pdf_view(request):
    return render(request, 'apps/instituicao/administrativo/RH/financas/filtro_pagamento_pdf.html')





#
@login_required
def pagamentos_pdf(request):
    
    
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
    #
    if request.method == 'POST':
        data_inicio = parse_date(request.POST.get('data_inicio'))
        data_fim = parse_date(request.POST.get('data_fim'))

        pagamentos = Pagamento.objects.select_related('aluno').filter(
            status='Pago',
            data_pagamento__range=(data_inicio, data_fim)
        ).order_by('aluno__nome', 'mes_referente')

        html_string = render_to_string(
            'apps/instituicao/administrativo/RH/financas/pagamento_pdf.html',
            {
                'pagamentos': pagamentos,
                'data_hoje': date.today(),
                'data_inicio': data_inicio,
                'data_fim': data_fim,
                'escola':escola,
                'administrativo':administrativo,
                'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
            }
        )

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio_pagamentos.pdf"'
        return response
    return redirect('school:filtro_pagamento_pdf')




#
# PAGAMENTOS EM ATRSO
#


@login_required
def filtro_pagamento_atraso_pdf(request):
    return render(request, 'apps/instituicao/administrativo/RH/financas/filtrar_pagamentos_atraso.html')

@login_required
def pagamentos_em_atraso_pdf(request):
    
    
        #Administrativo logado
     administrativo = DiretorAdministrativo.objects.get(user=request.user)
        
     escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
     #
     if request.method == 'POST':
            data_inicio = parse_date(request.POST.get('data_inicio'))
            data_fim = parse_date(request.POST.get('data_fim'))

            pagamentos = Pagamento.objects.select_related('aluno').filter(
                status='Pendente',
                data_pagamento__range=(data_inicio, data_fim)
            ).order_by('aluno__nome', 'mes_referente')

            html_string = render_to_string(
                'apps/instituicao/administrativo/RH/financas/relatorio_pagamento.html',
                {
                    'pagamentos': pagamentos,
                    'data_hoje': date.today(),
                    'data_inicio': data_inicio,
                    'data_fim': data_fim,
                    'escola':escola,
                    'administrativo':administrativo,
                    'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
                }
            )

            pdf_file = HTML(string=html_string).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="pagamentos_em_atraso.pdf"'
            return response
     return redirect('school:filtro_pagamento_atraso_pdf')



