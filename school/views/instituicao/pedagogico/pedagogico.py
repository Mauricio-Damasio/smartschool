from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.diretor_pedagogico import Pedagogico
from django.contrib import messages
import re
from datetime import date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from school.models.academico.escola import Escola
from school.models.academico.professor import Professor
from school.models.academico.aluno import Aluno
from school.models.academico.turma import Turma
from school.models.academico.disciplina import Disciplina
from django.db.models import Count

# Email
from school.utils.utils_email import enviar_dados_acesso_pedagogico
from school.models.academico.disciplinaLecionada import DisciplinaLecionada
from school.models.relatorio.trimestre_liberado import TrimestreLiberado

from school.models.relatorio.minipauta import MiniPauta
import json

#Dashboard



@login_required
def dashboard_pedagogico(request):
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    # Total de atribuições de disciplinas a professores
    total_atribuicoes = DisciplinaLecionada.objects.filter(
        professor__departamento__curso__escola=escola
    ).count()

    # Trimestres desbloqueados na escola
    trimestres_desbloqueados = TrimestreLiberado.objects.filter(
        turma__curso__escola=escola,
        liberado=True
    ).count()

    # Alunos da escola
    alunos = Aluno.objects.filter(turma__curso__escola=escola)

    # Mini pautas dos alunos
    minipautas = MiniPauta.objects.filter(aluno__in=alunos)

    alunos_aprovados = minipautas.filter(mf__gte=10).values('aluno').distinct().count()
    alunos_reprovados = minipautas.filter(mf__lt=10).values('aluno').distinct().count()

    # Obtemos a string representativa de cada classe com str()
    classes_objs = sorted(set(aluno.turma.classe for aluno in alunos), key=lambda c: str(c))
    classes = [str(cls) for cls in classes_objs]

    dados_aprovados = [
        minipautas.filter(
            mf__gte=10, aluno__turma__classe=cls_obj
        ).values('aluno').distinct().count()
        for cls_obj in classes_objs
    ]

    dados_reprovados = [
        minipautas.filter(
            mf__lt=10, aluno__turma__classe=cls_obj
        ).values('aluno').distinct().count()
        for cls_obj in classes_objs
    ]

    # Gráfico de disciplinas mais atribuídas
    atribuicoes = DisciplinaLecionada.objects.filter(
        professor__departamento__curso__escola=escola
    )
    disciplinas_dict = {}
    for atrib in atribuicoes:
        nome = atrib.disciplina.nome
        disciplinas_dict[nome] = disciplinas_dict.get(nome, 0) + 1

    # Dados a enviar ao template
    dados = {
        'total_atribuicoes': total_atribuicoes,
        'trimestres_desbloqueados': trimestres_desbloqueados,
        'alunos_aprovados': alunos_aprovados,
        'alunos_reprovados': alunos_reprovados,
        'classes': json.dumps(classes),  # strings 
        'dados_aprovados': json.dumps(dados_aprovados),
        'dados_reprovados': json.dumps(dados_reprovados),
        'disciplinas': json.dumps(list(disciplinas_dict.keys())),
        'atribuicoes_por_disciplina': json.dumps(list(disciplinas_dict.values())),
    }

    return render(request, 'apps/instituicao/pedagogico/perfil/home.html', dados)




#Perfil
@login_required  
def perfil(request:HttpRequest):
    pedagogico = request.user.pedagogico
   

    dados = {
        'pedagogico': pedagogico,
       
    }
    return render(request, 'apps/instituicao/pedagogico/perfil/perfil.html', dados)

# index
@login_required
def index(request: HttpRequest):
  
  # Carregar todos os dados para os selects
  pedagogicos = Pedagogico.objects.all().order_by('-id')
  escolas = Escola.objects.all()
  
  
  # Obter filtros
  escola = request.GET.get('escola')
  
  if escola:
    
    pedagogicos = Pedagogico.objects.filter(escola=escola)
  
  
  return render(request , 'apps/instituicao/pedagogico/index.html',{'pedagogicos':pedagogicos, 'escolas': escolas})
  
  
  
# Visualizar pedagogico
@login_required  
def visualizar(request:HttpRequest,id:int):
    pedagogico = get_object_or_404(Pedagogico, id=id)
   

    dados = {
        'pedagogico': pedagogico,
       
    }
    return render(request, 'apps/instituicao/pedagogico/visualizar.html', dados)
 

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
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       

       # Verificar se o número de agente já existe
        if Pedagogico.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

    
       
    
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
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       
        
        
        #  # #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Pedagogico')
        user.groups.add(grupo)
        
        
        
        
        # Cadastrar
        pedagogico = Pedagogico.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            user=user,
       
           
        )
        
       
        pedagogico.save()
        
        ####
        # 
        # Enviar e-mail com dados de acesso
        #
        email_enviado = enviar_dados_acesso_pedagogico(nome, username, senha, user.email)

        if email_enviado:
            messages.success(request, f'Diretor(a) pedagógico {nome} cadastrado com sucesso! Dados de acesso enviados para {user.email}.')
        else:
            messages.error(request, f'Diretor(a) pedagógico {nome} cadastrado com sucesso, mas o envio de e-mail falhou.')

        

        messages.success(request, f'Direitor(a) pedagogico {nome} cadastrado com sucesso!')
        return redirect('school:listar_pedagogicos')

   return render(request, 'apps/instituicao/pedagogico/cadastrar.html')

       


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    pedagogico = get_object_or_404(Pedagogico, pk=id)
   


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or pedagogico.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
       
        

        if not all([nome, numAgente, genero]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituica/pedagogico/atualizar.html', {'pedagogico':pedagogico})



        pedagogico.nome = nome
        pedagogico.genero = genero
        pedagogico.numAgente = numAgente
       
       
        if image:
           pedagogico.image = image

        pedagogico.save(force_update=True)
       

        messages.success(request, f'Direitor(a) pedagógico {nome} atualizado com sucesso!')
        return redirect('school:listar_pedagogicos')

    return render(request, 'apps/instituicao/pedagogico/atualizar.html', {'pedagogico':pedagogico})


 
 
#Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    pedagogico = get_object_or_404(Pedagogico, id=id)

    
    if request.method == 'POST':
      
        pedagogico.delete()
        return redirect('school:listar_pedagogicos')  
      
    return render(request, 'apps/instituicao/pedagogico/eliminar.html', {'pedagogico': pedagogico})
   
   
      
   
   
   
   
   
   
   
   