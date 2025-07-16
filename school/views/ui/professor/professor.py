from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.disciplina import Disciplina
from ....models.academico.professor import Professor
from school.models.academico.departamento import Departamento
from django.contrib import messages
import re
from datetime import date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from school.models.academico.turma import Turma
from school.models.academico.aluno import Aluno
from django.db.models import Count



@login_required
def dashboard_professor(request):
    professor = Professor.objects.get(user=request.user)
    disciplinas = professor.disciplina.all() 
    
    turmas = Turma.objects.all()
    alunos_por_turma = turmas.annotate(total_alunos=Count('aluno'))

    dados = {
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'alunos_por_turma': alunos_por_turma,
        'professor': professor, 'disciplinas':disciplinas
   
    }
    return render(request, 'apps/ui/professor/perfil/home.html', dados)



# Listar professores
@login_required
def index(request: HttpRequest):
  
  
  #escola logada
  
  escola = request.user.escola
  
  # Carregar todos os dados para os selects
  departamentos = Departamento.objects.filter(curso__escola=escola)
  

  
  professores = Professor.objects.filter(departamento__curso__escola=escola)
  
  
  #Obter filtros    
  departamento = request.GET.get('departamento')
  
  if departamento:
      
      professores =Professor.objects.filter(departamento=departamento)
  
  dados = {
        'professores':professores,
        'departamentos':departamentos,
  
       
        
  }
  
  return render(request , 'apps/ui/professor/index.html',dados)
  
  
#Perfil
  
# Visualizar professor
@login_required  
def perfil(request:HttpRequest,id:int):
    professor = get_object_or_404(Professor, id=id)
    disciplinas = professor.disciplina.all()  # Porque é ManyToMany
    departamento = professor.departamento

    dados = {
        'professor': professor,
        'disciplinas': disciplinas,
        'departamento': departamento,
    }
    return render(request, 'apps/ui/professor/perfil/perfil.html', dados)

  
  
# Visualizar professor
@login_required  
def visualizar(request:HttpRequest,id:int):
    professor = get_object_or_404(Professor, id=id)
    disciplinas = professor.disciplina.all()  # Porque é ManyToMany
    departamento = professor.departamento

    dados = {
        'professor': professor,
        'disciplinas': disciplinas,
        'departamento': departamento,
    }
    return render(request, 'apps/ui/professor/visualizar.html', dados)
  

# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)



# Cadastrar

@login_required
def cadastrar(request:HttpRequest):
   
   #Escola logada
   escola = request.user.escola
   
   # Carregar dados para os seletes
   departamentos = Departamento.objects.filter(curso__escola=escola)
   disciplinas = Disciplina.objects.filter(curso__escola=escola)
  
  
   disciplinas_selecionadas = [] 

   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image')
        numAgente = request.POST.get('numAgente')
        disciplina_id = request.POST.getlist('disciplina')
        departamento_id = request.POST.get('departamento')
        
        disciplinas_selecionadas = [int(d) for d in disciplina_id]
   
        
        
          # Validações
        if not all([nome, genero, numAgente, disciplina_id,departamento_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas, })

       

       # Verificar se o número de agente já existe
        if Professor.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})

       
        departamento = get_object_or_404(Departamento, pk=departamento_id)
       
        
        
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
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/ui/professor/cadastrar.html',  {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})
        
        
        
        
        #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Professor')
        user.groups.add(grupo)
        
        
        
        
        # Cadastrar
        professor = Professor.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            departamento= departamento,
            user=user,
           
        )
        
         # Adicionar disciplinas (ManyToMany)
        professor.disciplina.set(disciplinas_selecionadas)
        professor.save()
        
        
        
        
           # Enviar e-mail com dados de acesso
        '''send_mail(
            'Dados de Acesso ao Sistema SmartSchool',
            f'Olá {nome},\n\nSeu cadastro como professor(a) foi realizado com sucesso!\n\nUsuário: {username}\nSenha: {password}\n\nAcesse o sistema usando suas credenciais.\n\nObrigado.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email if user.email else f'{username}@smartschool.com'],  
            fail_silently=False,
        )'''

        messages.success(request, f'Professor (a) {nome} cadastrado com sucesso!')
        return redirect('school:listar_professores')

   return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos, 'disciplinas':disciplinas,'disciplinas_selecionadas': disciplinas_selecionadas})


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    professor = get_object_or_404(Professor, pk=id)
    
    
    #Escola logada
    escola = request.user.escola
   
    # Carregar dados para os seletes
    departamentos = Departamento.objects.filter(curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)

    # Pré-selecionar disciplinas já atribuídas
    disciplinas_selecionadas = list(professor.disciplina.values_list('id', flat=True))

    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or professor.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
        disciplina_id = request.POST.getlist('disciplina')
        departamento_id = request.POST.get('departamento')

       
        disciplinas_selecionadas = [int(d) for d in disciplina_id ]

        dados = {
            'professor': professor,
            'departamentos': departamentos,
            'disciplinas': disciplinas,
            'disciplinas_selecionadas': disciplinas_selecionadas,
        }

        if not all([nome, numAgente, genero, departamento_id, disciplinas_selecionadas]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/professor/atualizar.html', dados)

        departamento = get_object_or_404(Departamento, pk=departamento_id)

        professor.nome = nome
        professor.genero = genero
        professor.numAgente = numAgente
        professor.departamento = departamento
       
        if image:
           professor.image = image

        professor.save(force_update=True)
        professor.disciplina.set(disciplinas_selecionadas)

        messages.success(request, f'Professor(a) {nome} atualizado com sucesso!')
        return redirect('school:listar_professores')

    # Requisição GET
    dados = {
        'professor': professor,
        'departamentos': departamentos,
        'disciplinas': disciplinas,
        'disciplinas_selecionadas': disciplinas_selecionadas,
    }

    return render(request, 'apps/ui/professor/atualizar.html', dados)


 
 
#Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    professor = get_object_or_404(Professor, id=id)
    departamento = professor.departamento
    
    if request.method == 'POST':
      
        professor.delete()
        return redirect('school:listar_professores')  
      
    return render(request, 'apps/ui/professor/eliminar.html', {'professor': professor, 'departamento':departamento})
   
   
   
   
   
   
   
   
   
   
   
   