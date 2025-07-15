from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.coordenador import Coordenador
from school.models.academico.curso import Curso
from school.models.academico.escola import Escola
from school.models.academico.diretor_geral import Diretor
from school.models.academico.departamento import Departamento
from django.contrib import messages
import re
from datetime import date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from ....utils.utils_email import enviar_dados_acesso_coordenador

from school.models.academico.professor import Professor
from school.models.academico.aluno import Aluno
from school.models.relatorio.minipauta import MiniPauta
from school.models.relatorio.horario import Horario
from django.db import models

# Perfil coordenador
def dashboard_coordenador(request):
    


    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_pautas = MiniPauta.objects.count()
    total_horarios = Horario.objects.count()

    # Exemplo: Alunos por curso (para gráfico de pizza)
    alunos_por_curso = (
        Aluno.objects.values('turma__curso__nome')
        .order_by('turma__curso__nome')
        .annotate(total=models.Count('id'))
    )

    dados = {
        'total_alunos': total_alunos,
        'total_professores': total_professores,
        'total_pautas': total_pautas,
        'total_horarios': total_horarios,
        'alunos_por_curso': alunos_por_curso,
    }
    return render(request, 'apps/ui/coordenador/perfil/home.html',dados)




# Listar coordenadores
@login_required
def index(request: HttpRequest):
  
   #Admin logado
  diretor = Diretor.objects.get(user=request.user)

  escola = Escola.objects.filter(direitor=diretor).first()
  
  # Carregar todos os dados para os selects
  coordenadores = Coordenador.objects.filter(curso__escola=escola).order_by('-id')
  cursos = Curso.objects.filter(escola=escola)
  departamentos = Departamento.objects.filter(curso__escola=escola)
  
  # Obter filtros
  curso = request.GET.get('curso')
  departamento = request.GET.get('departamento')
  
  # Filtrar
  if curso:
      
      coordenadores = Coordenador.objects.filter(curso=curso)
   
  if departamento:
      
      coordenadores = Coordenador.objects.filter(departamento=departamento)
  
  
  dados = {
        'coordenadores':coordenadores,
        'departamentos':departamentos,
        'cursos':cursos,      
  }
  
  return render(request , 'apps/ui/coordenador/index.html',dados)
  

  
# Visualizar coordenador  
@login_required
def visualizar(request:HttpRequest,id:int):
    coordenador = get_object_or_404(Coordenador, id=id)
    curso = coordenador.curso
    departamento = coordenador.departamento

    dados = {
        'coordenador': coordenador,
        'departamento': departamento,
        'curso': curso,
    
    }
    return render(request, 'apps/ui/coordenador/visualizar.html', dados)
  

# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)




# Cadastrar
@login_required
def cadastrar(request:HttpRequest):
   
  
    #Admin logado
   diretor = Diretor.objects.get(user=request.user)

   escola = Escola.objects.filter(direitor=diretor).first()
    
   # Carregar todos os dados para os selects

   cursos = Curso.objects.filter(escola=escola)
   departamentos = Departamento.objects.filter(curso__escola=escola)
  
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image')
        numAgente = request.POST.get('numAgente')
        curso_id = request.POST.get('curso')
        departamento_id = request.POST.get('departamento')
       
   
        
        
          # Validações
        if not all([nome, genero, numAgente, curso_id, departamento_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })

       

       # Verificar se o número de agente já existe
        if Coordenador.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })

        if Coordenador.objects.filter(curso_id=curso_id).exists():
            messages.error(request, 'Já existe um coordenador nesse curso!')
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })
            
            
            
        curso = get_object_or_404(Curso, pk=curso_id)
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
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })
        
        
        # #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Coordenador')
        user.groups.add(grupo)
        
        
        
        
        # Cadastrar
        Coordenador.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            curso= curso,
            departamento= departamento,
            user=user,
           
        )
        
         ####
        # 
        # Enviar e-mail com dados de acesso
        #
        email_enviado = enviar_dados_acesso_coordenador(nome, username, senha, user.email)

        if email_enviado:
            messages.success(request, f'Coordenador(a) {nome} cadastrado(a) com sucesso! Dados de acesso enviados para {user.email}.')
        else:
            messages.error(request, f'Coordenador(a) {nome} cadastrado(a)  com sucesso, mas o envio de e-mail falhou.')
    

        messages.success(request, f'Coordenador (a) {nome} cadastrado com sucesso!')
        return redirect('school:listar_coordenadores')

   return render(request, 'apps/ui/coordenador/cadastrar.html', {'cursos':cursos, 'departamentos':departamentos })


# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    
    #
    coordenador = get_object_or_404(Coordenador, pk=id)
    
     #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    
    departamentos = Departamento.objects.filter(curso__escola= escola)
    cursos = Curso.objects.filter(escola=escola)


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or coordenador.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
        curso_id = request.POST.get('curso')
        departamento_id = request.POST.get('departamento')
        
       


        dados = {
            'coordenador': coordenador,
            'departamentos': departamentos,
            'cursos': cursos,
            
        }

        if not all([nome, numAgente, genero, departamento_id, curso_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/coordenador/atualizar.html', dados)
        
        

        departamento = get_object_or_404(Departamento, pk=departamento_id)
        curso = get_object_or_404(Curso, pk=curso_id)
        
        # Verifica se o curso já possui um coordenador diferente do atual
        coordenador_existente = Coordenador.objects.filter(curso=curso).exclude(id=coordenador.id).first()
        if coordenador_existente:
            messages.error(request, f"O curso '{curso.nome}' já possui um coordenador registrado.")
            return render(request, 'apps/ui/coordenador/atualizar.html', dados)


        coordenador.nome = nome
        coordenador.genero = genero
        coordenador.numAgente = numAgente
        coordenador.departamento = departamento
        coordenador.curso = curso
       
        if image:
           coordenador.image = image

        coordenador.save(force_update=True)
  

        messages.success(request, f'Coordenador(a) {nome} atualizado com sucesso!')
        return redirect('school:listar_coordenadores')

    # Requisição GET
    dados = {
            'coordenador': coordenador,
            'departamentos': departamentos,
            'cursos': cursos,
    }

    return render(request, 'apps/ui/coordenador/atualizar.html', dados)
 
 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    coordenador = get_object_or_404(Coordenador, id=id)
    departamento = coordenador.departamento
    curso =   coordenador.curso
    
    if request.method == 'POST':
      
        coordenador.delete()
        return redirect('school:listar_coordenadores')  
    
    dados ={
        'coordenador': coordenador, 
        'departamento':departamento, 
        'curso':curso,
        }
      
    return render(request, 'apps/ui/coordenador/eliminar.html', dados )
   
   
   
   
   
   
   
   
   
   
   
   