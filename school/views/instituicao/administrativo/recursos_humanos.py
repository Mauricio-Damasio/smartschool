from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from school.models.academico.professor import Professor
from school.models.academico.coordenador import Coordenador
from school.models.relatorio.desempenho import Desempenho
from school.models.relatorio.ponto import Ponto
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template

from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from school.models.academico.escola import Escola
from datetime import date


import tempfile



#
@login_required
def registrar_ponto(request):
    
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
    
    #
    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        data = request.POST.get('data')
        hora_entrada = request.POST.get('hora_entrada')
        hora_saida = request.POST.get('hora_saida')
        observacao = request.POST.get('observacoes')

        usuario_id = None
        if tipo == 'P':
            usuario_id = request.POST.get('usuario_prof_id')
        elif tipo == 'C':
            usuario_id = request.POST.get('usuario_coord_id')

        if not usuario_id:
            messages.error(request, 'Por favor, selecione um usuário válido.')
            return redirect('school:registrar_ponto')

        ponto = Ponto.objects.create(
            tipo=tipo,
            usuario_id=usuario_id,
            data=data,
            hora_entrada=hora_entrada,
            hora_saida=hora_saida,
            observacao=observacao
        )

        messages.success(request, 'Ponto registrado com sucesso.')
        return redirect('school:gerar_pdf_ponto', ponto_id=ponto.id)

    professores = Professor.objects.filter(departamento__curso__escola=escola)
    coordenadores = Coordenador.objects.filter(curso__escola=escola)

    return render(request, 'apps/instituicao/administrativo/RH/recursos_humanos/ponto.html', {
        'professores': professores,
        'coordenadores': coordenadores,
       
    })




#
# DESEMPENHO
#




#

@login_required
def listar_desempenhos(request):
    desempenhos = Desempenho.objects.all().order_by('-data_avaliacao')

    # Criando um dicionário para associar o nome ao ID e tipo
    lista = []
    for d in desempenhos:
        if d.tipo == 'P':
            try:
                usuario = Professor.objects.get(id=d.usuario_id)
                nome = usuario.nome
            except Professor.DoesNotExist:
                nome = "Professor não encontrado"
        elif d.tipo == 'C':
            try:
                usuario = Coordenador.objects.get(id=d.usuario_id)
                nome = usuario.nome
            except Coordenador.DoesNotExist:
                nome = "Coordenador não encontrado"
        else:
            nome = "Tipo desconhecido"

        lista.append({
            'desempenho': d,
            'nome_usuario': nome,
        })

    return render(request, 'apps/instituicao/administrativo/RH/recursos_humanos/listar_desempenhos.html', {
        'desempenhos': lista
    })


#Cadastrar
@login_required
def avaliar_desempenho(request):
    
    #
    if request.method == 'POST':
        
        #
        tipo = request.POST.get('tipo')
        usuario_id = request.POST.get('usuario_id')
        data_avaliacao = request.POST.get('data_avaliacao')
        nota = request.POST.get('nota')
        comentario = request.POST.get('comentario')
        
        
        
        #
        
        usuario_id = None
        
        if tipo == 'P':
            usuario_id = request.POST.get('usuario_prof_id')
        elif tipo == 'C':
            usuario_id = request.POST.get('usuario_coord_id')

        if not usuario_id:
            messages.error(request, 'Por favor, selecione um usuário válido.')
            return redirect('school:registrar_ponto')

        Desempenho.objects.create(
            tipo=tipo,
            usuario_id=usuario_id,
            data_avaliacao=data_avaliacao,
            nota=nota,
            comentario=comentario
        )
        messages.success(request, 'Avaliação salva com sucesso.')
        return redirect('school:listar_desempenhos')

    professores = Professor.objects.all()
    coordenadores = Coordenador.objects.all()
    return render(request, 'apps/instituicao/administrativo/RH/recursos_humanos/desempenho.html', {
        'professores': professores,
        'coordenadores': coordenadores
    })


#Eliminar
def eliminar_desempenho(request, id):
    
    desempenho = Desempenho.objects.get(pk=id)
   
    if request.method == 'POST':
    
        desempenho.delete()
    
        return redirect('school:listar_desempenhos')  
      
    return render(request, 'apps/instituicao/administrativo/RH/recursos_humanos/eliminar_desempenho.html', {' desempenho':  desempenho})
   


#PDF 

def gerar_pdf_desempenho(request, pk):
    
    
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
    #
    desempenho = get_object_or_404(Desempenho, pk=pk)
    
    if desempenho.tipo == 'P':
       
        usuario = Professor.objects.filter(id=desempenho.usuario_id).first()
    else:
       
        usuario = Coordenador.objects.filter(id=desempenho.usuario_id).first()
    
    html_string = render_to_string(
        'apps/instituicao/administrativo/RH/recursos_humanos/pdf_desempenho.html',
        {
            'desempenho': desempenho,
            'usuario': usuario,
            'escola':escola,
            'administrativo':administrativo,
            'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
                    'data_hoje': date.today().strftime('%d/%m/%Y'),
        }
    )

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="desempenho_{desempenho.id}.pdf"'
    return response







#pdfs











# PDF Pontos
@login_required
def gerar_pdf_ponto(request, ponto_id):
    
    
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()
    
    
    
    ponto = get_object_or_404(Ponto, id=ponto_id)
    
    if ponto.tipo == 'P':
        usuario = Professor.objects.filter(id=ponto.usuario_id).first()
    elif ponto.tipo == 'C':
        usuario = Coordenador.objects.filter(id=ponto.usuario_id).first()
    else:
        usuario = None

    nome_usuario = usuario.nome if usuario else "Usuário não encontrado"
    
    
    template = get_template('apps/instituicao/administrativo/RH/recursos_humanos/ponto_pdf.html')  
    html_content = template.render({
        'ponto': ponto,
        'nome_usuario': nome_usuario,
        'data_hoje': date.today().strftime('%d/%m/%Y'),
        'escola':escola,
        'administrativo':administrativo,
        'logo_url': request.build_absolute_uri('/static/img/insignia.jpg'),
    })

    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="registro_ponto_{ponto.id}.pdf"'
    return response