from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.departamento import Departamento
from ....models.academico.escola import Escola
from ....models.academico.diretor_geral import Diretor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from school.models.academico.curso import Curso

# Listar coordenadores
@login_required
def index(request: HttpRequest):
  
   #Admin logado
  diretor = Diretor.objects.get(user=request.user)

  escola = Escola.objects.filter(direitor=diretor).first()

  departamentos = Departamento.objects.filter(curso__escola=escola).order_by('-id')

  
  
  dados = {
        'departamentos':departamentos,
     
  }
  
  return render(request , 'apps/instituicao/departamento/index.html',dados)
  

  
# Visualizar departamento 
@login_required
def visualizar(request:HttpRequest,id:int):
    
    #
    departamento  = get_object_or_404(Departamento, id=id)
    curso = departamento.curso


    dados = {
        'departamento': departamento,
        'curso':curso,
      
    
    }
    return render(request, 'apps/instituicao/departamento/visualizar.html', dados)
  






# Cadastrar

@login_required
def cadastrar(request:HttpRequest):

       
    #Admin logado
   diretor = Diretor.objects.get(user=request.user)

   escola = Escola.objects.filter(direitor=diretor).first()
    
   # Carregar apenas os cursos da escola logada
   cursos = Curso.objects.filter(escola=escola)
   
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        curso_id = request.POST.get('curso')
   
       
       
   
        
        
          # Validações
        if not nome:
            messages.error(request, "O nom deve ser preenchido.")
            return render(request, 'apps/instituicao/departamento/cadastrar.html', {'cursos':cursos})


        curso = Curso.objects.get(pk=curso_id)
        
        # Cadastrar
        Departamento.objects.create(
            nome=nome,
            curso=curso
  
         
        )
        

        messages.success(request, f'Departamento {nome} cadastrado com sucesso!')
        return redirect('school:listar_departamentos')

   return render(request, 'apps/instituicao/departamento/cadastrar.html',{'cursos':cursos})

# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    
    #
    departamento = get_object_or_404(Departamento, pk=id)
         
    #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    
           # Carregar apenas os cursos da escola logada
    cursos = Curso.objects.filter(escola=escola)


    if request.method == 'POST':
      
        nome = request.POST.get('nome')
        curso_id = request.POST.get('curso')

        
    
        dados = {
            'departamento': departamento,
            'cursos':cursos
        
            
        }

        if not nome:
            messages.error(request, "O nome deve ser preenchido.")
            return render(request, 'apps/instituicao/departamento/atualizar.html', dados)


        curso = get_object_or_404(Curso, pk=curso_id)
        
        departamento.nome = nome
        departamento.curso = curso
        
      
        departamento.save(force_update=True)
  

        messages.success(request, f'Departamento {nome} atualizado com sucesso!')
        return redirect('school:listar_departamentos')

    # Requisição GET
    dados = {
            'departamento': departamento,
            'cursos':cursos
          
    }

    return render(request, 'apps/instituicao/departamento/atualizar.html', dados)
 
 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    departamento = get_object_or_404(Departamento, id=id)
    curso = departamento.curso
  
    
    if request.method == 'POST':
      
        departamento.delete()
        return redirect('school:listar_departamentos')  
    
    dados ={
        'departamento': departamento, 
        'curso': curso,
     
        }
      
    return render(request, 'apps/instituicao/departamento/eliminar.html', dados )
   
   
   
   
   
   
   
   
   
   
   
   