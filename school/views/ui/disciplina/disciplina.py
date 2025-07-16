from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.disciplina import Disciplina
from school.models.academico.curso import Curso
from school.models.academico.classe import Classe
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Listar coordenadores
@login_required
def index(request: HttpRequest):
  
  #Escola logada
  escola = request.user.escola
  
  # Carregar todos os dados para os selects
  disciplinas = Disciplina.objects.filter(curso__escola=escola).order_by('-id')
  cursos = Curso.objects.filter(escola=escola)
    # Filtrar classes conforme o tipo da escola
  if escola.tipo_escola == 'EP':
        classes = Classe.objects.filter(ensino_primario__isnull=False)
  elif escola.tipo_escola == 'PC':
        classes = Classe.objects.filter(primeiro_ciclo__isnull=False)
  elif escola.tipo_escola == 'SC':
        classes = Classe.objects.filter(segundo_ciclo__isnull=False)
  else:
        classes = Classe.objects.none()
  
  
  dados = {
        'disciplinas':disciplinas,
        'classes':classes,
        'cursos':cursos,      
  }
  
  return render(request , 'apps/ui/disciplina/index.html',dados)
  

  
# Visualizar disciplina 
@login_required
def visualizar(request:HttpRequest,id:int):
    #
    escola = request.user.escola
    #
    disciplina  = get_object_or_404(Disciplina, id=id)
    curso =  disciplina .curso
    
            
   

    dados = {
        'disciplina': disciplina,
        'curso': curso,
      
    
    }
    return render(request, 'apps/ui/disciplina/visualizar.html', dados)
  






# Cadastrar

@login_required
def cadastrar(request:HttpRequest):
   
   #Escola logada
   escola = request.user.escola
   
   # Carregar dados para os seletes
   cursos = Curso.objects.filter(escola=escola)
    # Filtrar classes conforme o tipo da escola
   if escola.tipo_escola == 'EP':
            classes = Classe.objects.filter(ensino_primario__isnull=False)
   elif escola.tipo_escola == 'PC':
            classes = Classe.objects.filter(primeiro_ciclo__isnull=False)
   elif escola.tipo_escola == 'SC':
            classes = Classe.objects.filter(segundo_ciclo__isnull=False)
   else:
            classes = Classe.objects.none()
  
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        classe_id = request.POST.get('classe')
        curso_id = request.POST.get('curso')
       
       
   
        
        
          # Validações
        if not all([nome, curso_id, classe_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/disciplina/cadastrar.html', {'cursos':cursos, 'classes':classes })

      
       
        curso = get_object_or_404(Curso, pk=curso_id)
        classe = get_object_or_404(Classe, pk=classe_id)
      
        
        # Cadastrar
        Disciplina.objects.create(
            nome=nome,
            curso= curso,
            classe = classe,
            descricao=descricao,
           
        )
        

        messages.success(request, f'Disciplina {nome} cadastrada com sucesso!')
        return redirect('school:listar_disciplinas')

   return render(request, 'apps/ui/disciplina/cadastrar.html', {'cursos':cursos, 'classes':classes })

# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    
    #
    disciplina = get_object_or_404(Disciplina, pk=id)
   #Escola logada
    escola = request.user.escola
   
    # Carregar dados para os seletes
    cursos = Curso.objects.filter(escola=escola)
    # Filtrar classes conforme o tipo da escola
    if escola.tipo_escola == 'EP':
            classes = Classe.objects.filter(ensino_primario__isnull=False)
    elif escola.tipo_escola == 'PC':
            classes = Classe.objects.filter(primeiro_ciclo__isnull=False)
    elif escola.tipo_escola == 'SC':
            classes = Classe.objects.filter(segundo_ciclo__isnull=False)
    else:
            classes = Classe.objects.none()


    if request.method == 'POST':
      
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        curso_id = request.POST.get('curso')
        classe_id = request.POST.get('classe')
        
       


        dados = {
            'disciplina': disciplina,
            'classes': classes,
            'cursos': cursos,
            
        }

        if not all([nome, descricao, classe_id,curso_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/disciplina/atualizar.html', dados)

        classe = get_object_or_404(Classe, pk=classe_id)
        curso = get_object_or_404(Curso, pk=curso_id)

        disciplina.nome = nome
        disciplina.descricao = descricao
        disciplina.classe = classe
        disciplina.curso = curso
       
        disciplina.save(force_update=True)
  

        messages.success(request, f'Disciplina {nome} atualizada com sucesso!')
        return redirect('school:listar_disciplinas')

    # Requisição GET
    dados = {
            'disciplina': disciplina,
            'classes': classes,
            'cursos': cursos,
    }

    return render(request, 'apps/ui/disciplina/atualizar.html', dados)
 
 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    disciplina = get_object_or_404(Disciplina, id=id)
    classe = disciplina.classe
    curso = disciplina.curso
    
    if request.method == 'POST':
      
        disciplina.delete()
        return redirect('school:listar_disciplinas')  
    
    dados ={
        'disciplina': disciplina, 
        'classe':classe, 
        'curso':curso,
        }
      
    return render(request, 'apps/ui/disciplina/eliminar.html', dados )
   
   
   
   
   
   
   
   
   
   
   
   