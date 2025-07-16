from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.aluno import Aluno
from ....models.academico.curso import Curso
from ....models.academico.classe import Classe
from ....models.academico.turma import Turma
from ....models.academico.professor import Professor
from ....models.academico.disciplina import Disciplina
from ....models.relatorio.minipauta import MiniPauta
from django.contrib import messages
import re
from datetime import datetime, date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count

# Email
from school.utils.utils_email import enviar_dados_acesso_aluno

#
@login_required
def dashboard_aluno(request):
    
    #estatisticas
    turmas = Turma.objects.all()
    
    aluno = Aluno.objects.get(user=request.user)
    mini_pautas = MiniPauta.objects.filter(aluno=aluno)

    alunos_por_turma = turmas.annotate(total_alunos=Count('aluno'))

    dados = {
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'alunos_por_turma': alunos_por_turma,
        'aluno': aluno, 'mini_pautas': mini_pautas
    }
    #
  
    return render(request, 'apps/ui/aluno/perfil/home.html', dados)



# Listar alunos

@login_required
def index(request: HttpRequest):

    # Obter a escola do usuário logado
    escola = request.user.escola

    # Carregar turmas pertencentes à escola
    turmas = Turma.objects.filter(curso__escola=escola).order_by('nome')

    # Obter o ID da turma selecionada no filtro
    turma_id = request.GET.get('turma')

    # Inicializar alunos da escola
    alunos = Aluno.objects.filter(turma__curso__escola=escola)

    # Aplicar filtro se uma turma foi selecionada
    if turma_id:
        alunos = alunos.filter(turma_id=turma_id)
    else:
        messages.error(request, 'Selecione a turma!')
        alunos = Aluno.objects.none()

    # Dados enviados para o template
    dados = {
        'alunos': alunos,
        'turmas': turmas,
    }

    return render(request, 'apps/ui/aluno/index.html', dados)





  
#Perfil
  
# Visualizar professor
@login_required  
def perfil(request:HttpRequest,id:int):
    
    aluno = get_object_or_404(Aluno, id=id)
    turma = aluno.turma

    dados = {
        'aluno': aluno,
        'turma': turma,
       
    }
    return render(request, 'apps/ui/aluno/perfil/perfil.html', dados)

  
 # Visualizar professor
@login_required  
def visualizar(request:HttpRequest,id:int):
    aluno = get_object_or_404(Aluno, id=id)
    turma = aluno.turma

    dados = {
        'aluno': aluno,
        'turma': turma,
       
    }
    return render(request, 'apps/ui/aluno/visualizar.html', dados)


 

# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)


def calcular_idade(data_nascimento):
    hoje = date.today()
    return hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))



# Cadastrar


def cadastrar(request:HttpRequest):
   
  
    # Obter a escola do usuário logado
   escola = request.user.escola

    # Carregar turmas pertencentes à escola
   turmas = Turma.objects.filter(curso__escola=escola).order_by('nome')
   
   
   
   if request.method == 'POST':
   
        # Dados do aluno
        nome = request.POST.get('nome')
        data_nascimento_str = request.POST.get('data_nascimento')
        idade_str = request.POST.get('idade')
        genero = request.POST.get('genero')
        image = request.FILES.get('image')
        bilhete = request.POST.get('bilhete')
        telefone = request.POST.get('telefone')
        turma_id = request.POST.get('turma')
    
        
        #############
        # Validações
        #############
        if not all([nome, data_nascimento_str, idade_str, genero, bilhete, telefone, turma_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})

        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Data de nascimento inválida.")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})

        try:
            idade = int(idade_str)
        except ValueError:
            messages.error(request, "Idade inválida.")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})

        idade_real = calcular_idade(data_nascimento)
        
        if idade != idade_real:
            messages.error(request, f"Idade informada ({idade}) não corresponde à data de nascimento ({data_nascimento}). A idade correta seria {idade_real}.")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})


       # Verificar se o usuário já existe
        if Aluno.objects.filter(bilhete=bilhete).exists():
            messages.error(request, 'O bilhete já existe!')
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})

        turma = get_object_or_404(Turma, pk=turma_id)
        
       
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
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas': turmas})
        
        
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Aluno')
        user.groups.add(grupo)

      
         
        # Cadastrar aluno
        Aluno.objects.create(
            nome=nome,
            data_nascimento=data_nascimento,
            idade=idade,
            genero=genero,
            image=image,
            bilhete=bilhete,
            telefone=telefone,
            turma=turma,
            user=user
        )
        

        ####
        # Enviar e-mail
        email_enviado = enviar_dados_acesso_aluno(nome, username, senha, user.email)

        if email_enviado:
            messages.success(request, f'Aluno(a) {nome} cadastrado com sucesso! Dados de acesso enviados para {user.email}.')
        else:
            messages.warning(request, f'Aluno(a) {nome} cadastrado com sucesso, mas o envio de e-mail falhou.')

        
        
        messages.success(request, f'Aluno (a) {nome} cadastrado com sucesso!')
        return redirect('school:listar_alunos')

   return render(request, 'apps/ui/aluno/cadastrar.html', {'turmas':turmas}) 



# Atualizar
def atualizar(request:HttpRequest, id:int):
   
  
    # Obter a escola do usuário logado
   escola = request.user.escola

    # Carregar turmas pertencentes à escola
   turmas = Turma.objects.filter(curso__escola=escola).order_by('nome')
   
   #Aluno específico
   aluno = get_object_or_404(Aluno, pk=id)
   
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        data_nascimento_str = request.POST.get('data_nascimento')
        idade_str = request.POST.get('idade')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or aluno.image
        bilhete = request.POST.get('bilhete')
        telefone = request.POST.get('telefone')
        turma_id = request.POST.get('turma')
        
        
          # Validações
        if not all([nome, data_nascimento_str, idade_str, genero, bilhete, telefone, turma_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/aluno/atualizar.html', {'turmas': turmas})

        try:
            data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Data de nascimento inválida.")
            return render(request, 'apps/ui/aluno/atualizar.html', {'turmas': turmas})

        try:
            idade = int(idade_str)
        except ValueError:
            messages.error(request, "Idade inválida.")
            return render(request, 'apps/ui/aluno/atualizar.html', {'turmas': turmas})

        idade_real = calcular_idade(data_nascimento)
        
        if idade != idade_real:
            messages.error(request, f"Idade informada ({idade}) não corresponde à data de nascimento ({data_nascimento}). A idade correta seria {idade_real}.")
            return render(request, 'apps/ui/aluno/atualizar.html', {'turmas': turmas})

      

        turma = get_object_or_404(Turma, pk=turma_id)
        
        
        
        
        
        # Receber os dados para atualizar
        aluno.nome=nome
        aluno.data_nascimento=data_nascimento
        aluno.idade=idade
        aluno.genero=genero
        aluno.bilhete=bilhete
        aluno.telefone=telefone
        aluno.turma=turma
        
        if image:
             aluno.image=image
             
        aluno.save(force_update=True)
        
           

        messages.success(request, f'Aluno (a) {nome} atualizado com sucesso!')
        return redirect('school:listar_alunos')



   return render(request, 'apps/ui/aluno/atualizar.html', {'turmas':turmas, 'aluno':aluno}) 
 
 
 
 
 #Eliminar
def eliminar(request:HttpRequest, id:int):

   #Aluno específico
   aluno = get_object_or_404(Aluno, pk=id)
   turma =  aluno.turma
   
   if request.method == 'POST':
     
     
     aluno.delete()
     
     return redirect('school:listar_alunos')

   
   return render(request, 'apps/ui/aluno/eliminar.html', {'aluno':aluno, 'turma':turma}) 
     
     
    