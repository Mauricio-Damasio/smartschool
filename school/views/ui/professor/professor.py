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
from school.models.academico.escola import Escola
from school.models.academico.diretor_geral import Diretor
from school.models.academico.aluno import Aluno
from school.models.documento.aula_elaborada import AulaElaborada
from school.models.relatorio.minipauta import MiniPauta
from django.db.models import Count
from ....utils.utils_email import enviar_dados_acesso_professor
from school.models.academico.disciplinaLecionada import DisciplinaLecionada

from django.contrib.auth.decorators import login_required

from django.db.models import Avg, Count




#
#DASHBOARD
#




@login_required
def dashboard_professor(request):
    professor = request.user.professor  # Acessa o professor logado

    # Disciplinas que ele leciona
    disciplinas_lecionadas = DisciplinaLecionada.objects.filter(professor=professor)

    # Turmas únicas
    turmas = disciplinas_lecionadas.values_list('turma', flat=True).distinct()

    # Total de alunos nas turmas do professor
    
    total_alunos = Aluno.objects.filter(turma__in=turmas).count()

    # Total de disciplinas lecionadas
    total_disciplinas = disciplinas_lecionadas.count()

    # Total de aulas no mês atual
    from datetime import datetime
    agora = datetime.now()
    total_aulas_mes = AulaElaborada.objects.filter(
        professor=professor,
        data__month=agora.month,
        data__year=agora.year
    ).count()

    # Presença geral
    pautas = MiniPauta.objects.filter(
        professor=professor,
        turma__in=turmas
    )

    total_registros = pautas.count()
    frequencia_geral = 0
    if total_registros > 0:
        frequencia_geral = int(pautas.aggregate(avg=Avg('aluno'))['avg'] or 0)

    # Presença por turma
    nomes_turmas = []
    presencas_turmas = []
    for t_id in turmas:
        nome = disciplinas_lecionadas.filter(turma=t_id).first().turma.nome
        nomes_turmas.append(nome)
        media_turma = pautas.filter(turma_id=t_id).aggregate(avg=Avg('aluno'))['avg'] or 0
        presencas_turmas.append(int(media_turma))

    # Médias por disciplina
    nomes_disciplinas = []
    medias_disciplinas = []
    for dl in disciplinas_lecionadas:
        nome = dl.disciplina.nome
        nomes_disciplinas.append(nome)
        media = pautas.filter(disciplina=dl.disciplina).aggregate(avg=Avg('mt'))['avg'] or 0
        medias_disciplinas.append(round(media, 1))

    dados = {
        'total_alunos': total_alunos,
        'total_disciplinas': total_disciplinas,
        'total_aulas_mes': total_aulas_mes,
        'frequencia_geral': frequencia_geral,
        'nomes_turmas': nomes_turmas,
        'presencas_turmas': presencas_turmas,
        'nomes_disciplinas': nomes_disciplinas,
        'medias_disciplinas': medias_disciplinas,
    }

    return render(request,  'apps/ui/professor/perfil/home.html', dados)







# Listar professores
@login_required
def index(request: HttpRequest):
  
  
  #escola logada
  
  #Admin logado
  diretor = Diretor.objects.get(user=request.user)

  escola = Escola.objects.filter(direitor=diretor).first()
  
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
def visualizar(request: HttpRequest, id: int):
    professor = get_object_or_404(Professor, pk=id)

    #Escola logada
    #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()

    if not professor.departamento.curso.escola == escola:
        messages.error(request, "Você não tem permissão para visualizar este professor.")
        return redirect('school:listar_atribuicao')

    atribuicoes = DisciplinaLecionada.objects.filter(
        professor=professor,
        turma__curso__escola=escola
    ).select_related('disciplina', 'turma', 'turma__classe', 'turma__curso')

    return render(request,  'apps/ui/professor/visualizar.html', {
        'professor': professor,
        'atribuicoes': atribuicoes
    })









  

# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)




# Cadastrar

@login_required
def cadastrar(request:HttpRequest):
   
   #Escola logada
   #Admin logado
   diretor = Diretor.objects.get(user=request.user)

   escola = Escola.objects.filter(direitor=diretor).first()
   
   # Carregar dados para os seletes
   departamentos = Departamento.objects.filter(curso__escola=escola)
  

   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image')
        numAgente = request.POST.get('numAgente')        
        departamento_id = request.POST.get('departamento')
    
   
        
        
          # Validações
        if not all([nome, genero, numAgente, departamento_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos })

       

       # Verificar se o número de agente já existe
        if Professor.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})

       
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
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})
        
        
        
        
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
        

        
        
        
         ####
        # 
        # Enviar e-mail com dados de acesso
        #
        email_enviado = enviar_dados_acesso_professor(nome, username, senha, user.email)

        if email_enviado:
            messages.success(request, f'Professor(a) {nome} cadastrado com sucesso! Dados de acesso enviados para {user.email}.')
        else:
            messages.error(request, f'Professor(a) {nome} cadastrado com sucesso, mas o envio de e-mail falhou.')

        messages.success(request, f'Professor (a) {nome} cadastrado com sucesso!')
        return redirect('school:listar_professores')

   return render(request, 'apps/ui/professor/cadastrar.html', {'departamentos':departamentos})




# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    professor = get_object_or_404(Professor, pk=id)
    
    
    #Escola logada
    #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
   
    # Carregar dados para os seletes
    departamentos = Departamento.objects.filter(curso__escola=escola)


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or professor.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
        departamento_id = request.POST.get('departamento')

       
    
        dados = {
            'professor': professor,
            'departamentos': departamentos,
           
        }

        if not all([nome, numAgente, genero, departamento_id]):
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
  

        messages.success(request, f'Professor(a) {nome} atualizado com sucesso!')
        return redirect('school:listar_professores')

    # Requisição GET
    dados = {
        'professor': professor,
        'departamentos': departamentos,
       
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
   
   
   
   
   
   
   
   
   
   
   
   