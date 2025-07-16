from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.turma import Turma
from school.models.academico.curso import Curso
from school.models.academico.classe import Classe
from school.models.academico.ano_lectivo import AnoLetivo
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Listar turmas
@login_required
def index(request: HttpRequest):
 
  escola = request.user.escola
  

  
  # Carregar apenas os dados da escola logada
  cursos = Curso.objects.filter(escola=escola)
  turmas = Turma.objects.filter(curso__escola=escola)

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
        'turmas':turmas,
        'classes':classes,
        'cursos':cursos,      
  }
  
  return render(request , 'apps/ui/turma/index.html',dados)
  

  
# Visualizar turma
@login_required 
def visualizar(request:HttpRequest,id:int):
    

         
    # Escola logada
    escola = request.user.escola
    

        # Carregar apenas os cursos da escola logada
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
            
    #
    turma  = get_object_or_404(Turma, id=id)

    dados = {
        'turma': turma,
        'cursos': cursos,
        'classes': classes,
    
    }
    return render(request, 'apps/ui/turma/visualizar.html', dados)
  






# Cadastrar

@login_required
def cadastrar(request:HttpRequest):
   
  
   # Escola logada
   escola = request.user.escola
   

    # Carregar apenas os cursos da escola logada
   cursos = Curso.objects.filter(escola=escola)
   ano_lectivos = AnoLetivo.objects.all()
   
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
        turno = request.POST.get('turno')
        ano_lectivo_id = request.POST.get('ano_lectivo')
        classe_id = request.POST.get('classe')
        curso_id = request.POST.get('curso')
       
       
   
        
        
          # Validações
        if not all([nome, curso_id, classe_id, turno, ano_lectivo_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/turma/cadastrar.html', {'cursos':cursos, 'classes':classes, 'ano_lectivos': ano_lectivos })

        if Turma.objects.filter(nome=nome,classe=classe_id,curso=curso_id).exists():
            messages.error(request, "Os dados da turma já existem.")
            return render(request, 'apps/ui/turma/cadastrar.html', {'cursos':cursos, 'classes':classes, 'ano_lectivos': ano_lectivos })
             
       
        curso = get_object_or_404(Curso, pk=curso_id)
        classe = get_object_or_404(Classe, pk=classe_id)
        ano_lectivo = get_object_or_404(AnoLetivo, pk=ano_lectivo_id)
      
        
        # Cadastrar
        Turma.objects.create(
            nome=nome,
            curso= curso,
            classe = classe,
            turno=turno,
            ano_lectivo=ano_lectivo,
           
        )
        

        messages.success(request, f'Turma {nome} cadastrada com sucesso!')
        return redirect('school:listar_turmas')

   return render(request, 'apps/ui/turma/cadastrar.html', {'cursos':cursos, 'classes':classes, 'ano_lectivos': ano_lectivos })


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):

      
   # Escola logada
   escola = request.user.escola
   

    # Carregar apenas os cursos da escola logada
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

    #
   turma = get_object_or_404(Turma, pk=id)
  
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        turno = request.POST.get('turno')
        ano_lectivo = request.POST.get('ano_lectivo')
        classe_id = request.POST.get('classe')
        curso_id = request.POST.get('curso')
        
       


        dados = {
            'turma': turma,
            'classes': classes,
            'cursos': cursos,
            
        }

        if not all([nome, turno,ano_lectivo, classe_id,curso_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/ui/turma/atualizar.html', dados)

        classe = get_object_or_404(Classe, pk=classe_id)
        curso = get_object_or_404(Curso, pk=curso_id)

        turma.nome = nome
        turma.turno = turno
        turma.ano_lectivo = ano_lectivo
        turma.classe = classe
        turma.curso = curso
       
        turma.save(force_update=True)
  

        messages.success(request, f'Turma {nome} atualizada com sucesso!')
        return redirect('school:listar_turmas')

    # Requisição GET
   dados = {
            'turma': turma,
            'classes': classes,
            'cursos': cursos,
    }

   return render(request, 'apps/ui/turma/atualizar.html', dados)
 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    turma = get_object_or_404(Turma, id=id)
    classe = turma.classe
    curso = turma.curso
    
    if request.method == 'POST':
      
        turma.delete()
        return redirect('school:listar_turmas')  
    
    dados ={
        'turma': turma, 
        'classe':classe, 
        'curso':curso,
        }
      
    return render(request, 'apps/ui/turma/eliminar.html', dados )
   
   
   
 
   
   
   
   
   
   
   