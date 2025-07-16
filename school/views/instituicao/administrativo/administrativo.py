from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from django.contrib import messages
import re
from datetime import date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from school.models.academico.escola import Escola
from ....utils.utils_email import enviar_dados_acesso_administrativo

#
from django.shortcuts import render
from django.db.models import Count, Q
from django.utils.timezone import now
from datetime import datetime, timedelta
from collections import OrderedDict
from school.models.academico.aluno import Aluno
from school.models.relatorio.pagamento import Pagamento
from school.models.relatorio.assiduidade import Assiduidade
from school.models.relatorio.minipauta import MiniPauta
from school.models.relatorio.desempenho import Desempenho



#
#
#


@login_required
def dashboard_administrativo(request):
    #Administrativo logado
    administrativo = DiretorAdministrativo.objects.get(user=request.user)
    
    escola =Escola.objects.filter(direitor_administrativo=administrativo).first()

    # Totais
    total_alunos = Aluno.objects.filter(turma__curso__escola=escola).count()
    total_pagamentos_pagos = Pagamento.objects.filter(aluno__turma__curso__escola=escola, status='Pago').count()
    total_pagamentos_pendentes = Pagamento.objects.filter(aluno__turma__curso__escola=escola, status='Pendente').count()

    # Assiduidade atual
    assid_professores = Assiduidade.objects.filter(professor__departamento__curso__escola=escola, cargo='Professor').count()
    assid_coordenadores = Assiduidade.objects.filter(coordenador__curso__escola=escola, cargo='Coordenador').count()

    # Desempenho (MiniPauta)
    desempenho = {
        'excelente': MiniPauta.objects.filter(aluno__turma__curso__escola=escola, mt__gte=17).count(),
        'bom': MiniPauta.objects.filter(aluno__turma__curso__escola=escola, mt__gte=14, mt__lt=17).count(),
        'regular': MiniPauta.objects.filter(aluno__turma__curso__escola=escola, mt__gte=10, mt__lt=14).count(),
        'fraco': MiniPauta.objects.filter(aluno__turma__curso__escola=escola, mt__lt=10).count(),
    }

    # Assiduidade últimos 6 meses
    hoje = now().date()
    meses_labels = []
    professores_assid = []
    coordenadores_assid = []

    for i in range(5, -1, -1):
        mes = (hoje.replace(day=1) - timedelta(days=i * 30))
        label = mes.strftime('%b/%Y')
        professores = Assiduidade.objects.filter(
            professor__departamento__curso__escola=escola,
            data__year=mes.year,
            data__month=mes.month,
            cargo='Professor'
        ).count()
        coordenadores = Assiduidade.objects.filter(
            coordenador__curso__escola=escola,
            data__year=mes.year,
            data__month=mes.month,
            cargo='Coordenador'
        ).count()

        meses_labels.append(label)
        professores_assid.append(professores)
        coordenadores_assid.append(coordenadores)

    dados = {
        'total_alunos': total_alunos,
        'total_pagamentos_pagos': total_pagamentos_pagos,
        'total_pagamentos_pendentes': total_pagamentos_pendentes,
        'assid_professores': assid_professores,
        'assid_coordenadores': assid_coordenadores,
        'desempenho': desempenho,
        'meses_labels': meses_labels,
        'professores_assid': professores_assid,
        'coordenadores_assid': coordenadores_assid,
    }

    return render(request, 'apps/instituicao/administrativo/perfil/home.html', dados)

#
#


# Listar professores
@login_required
def index(request: HttpRequest):
  
  # Carregar todos os dados para os selects
  administrativos = DiretorAdministrativo.objects.all().order_by('-id')
  escolas = Escola.objects.all()
  
  
  # Obter filtros
  escola = request.GET.get('escola')
  
  if escola:
    
    administrativos = DiretorAdministrativo.objects.filter(escola=escola)
  
  
  return render(request , 'apps/instituicao/administrativo/index.html',{'administrativos':administrativos, 'escolas': escolas})
  
  
  
# Visualizar administrativo
@login_required  
def visualizar(request:HttpRequest,id:int):
    administrativo = get_object_or_404(DiretorAdministrativo, id=id)
   

    dados = {
        'administrativo': administrativo,
       
    }
    return render(request, 'apps/instituicao/administrativo/visualizar.html', dados)
 

# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)



# Cadastrar

@login_required
def cadastrar(request:HttpRequest):


   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image')
        numAgente = request.POST.get('numAgente')
       
   
        
        
          # Validações
        if not all([nome, genero, numAgente]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       

       # Verificar se o número de agente já existe
        if DiretorAdministrativo.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

    
       
    
        ####################################################################
        # Dados de perfil
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha') or get_random_string(8)
        senha_confirmar = request.POST.get('senha') or get_random_string(8)
            
        
        ###########################
        # Validando dados de perfil
        ###########################
        
        #
        if User.objects.filter(username=username).exists() :
          
            messages.error(request, "O usuário já existe")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        
        
        #  # #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Administrativo')
        user.groups.add(grupo)
        
        
    
        
        # Cadastrar
        administrativo = DiretorAdministrativo.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            user=user,
       
           
        )
        
       
        administrativo.save()
        print(f'Usuário: {user.username}, Perfil: {hasattr(user, "administrativo")}')

          ####
        # 
        # Enviar e-mail com dados de acesso
        #
        email_enviado = enviar_dados_acesso_administrativo(nome, username, senha, user.email)

        if email_enviado:
            messages.success(request, f'Diretor(a) administrativo {nome} cadastrado com sucesso! Dados de acesso enviados para {user.email}.')
        else:
            messages.error(request, f'Diretor(a) administrativo {nome} cadastrado com sucesso, mas o envio de e-mail falhou.')

        messages.success(request, f'Direitor (a) administrativo {nome} cadastrado com sucesso!')
        return redirect('school:listar_administrativos')

   return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    administrativo = get_object_or_404(DiretorAdministrativo, pk=id)
   


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or administrativo.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
       
        

        if not all([nome, numAgente, genero]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituica/administrativo/atualizar.html', {'administrativo':administrativo})



        administrativo.nome = nome
        administrativo.genero = genero
        administrativo.numAgente = numAgente
       
       
        if image:
           administrativo.image = image

        administrativo.save(force_update=True)
       

        messages.success(request, f'Direitor(a) administrativo {nome} atualizado com sucesso!')
        return redirect('school:listar_administrativos')

    return render(request, 'apps/instituicao/administrativo/atualizar.html', {'administrativo':administrativo})


 
 
#Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    administrativo = get_object_or_404(DiretorAdministrativo, id=id)

    
    if request.method == 'POST':
      
        administrativo.delete()
        return redirect('school:listar_administrativos')  
      
    return render(request, 'apps/instituicao/administrativo/eliminar.html', {'administrativo': administrativo})
   
   
      
   
   
   
   
   
   
   
   