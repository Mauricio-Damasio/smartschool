from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.curso import Curso
from school.models.academico.escola import Escola
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Listar coordenadores
@login_required
def index(request: HttpRequest):
  
  
  cursos = Curso.objects.all().order_by('-id')
  
  # Carregar dados para o select
  escolas = Escola.objects.all()
  
  
  # obter filtro
  escola = request.GET.get('escola')
  
  
  if escola:
    
     cursos = Curso.objects.filter(escola=escola)
    
  
  dados = {
        'cursos':cursos,
        'escolas':escolas,
             
  }
  
  return render(request , 'apps/instituicao/curso/index.html',dados)
  

  
# Visualizar disciplina 
@login_required
def visualizar(request:HttpRequest,id:int):
    
    #
    curso  = get_object_or_404(Curso, id=id)
    escola =   curso.escola
   

    dados = {
       
        'curso': curso,
        'escola': escola,
    
    }
    return render(request, 'apps/instituicao/curso/visualizar.html', dados)
  



# Cadastrar

@login_required
def cadastrar(request:HttpRequest):
   
   # Carregar dados para os seletes
   escolas = Escola.objects.all()
  
  
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        modalidade = request.POST.get('modalidade')
        nivel = request.POST.get('nivel')
        ativo = request.POST.get('ativo') == 'on'
        escola_id = request.POST.get('escola')
       
       
   
        
        
          # Validações
        if not all([nome, modalidade, nivel, ativo,escola_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/curso/cadastrar.html', {'escolas':escolas})
        
        # Verifica se já existe um curso com o mesmo nome nessa escola
        if Curso.objects.filter(nome__iexact=nome, escola_id=escola_id).exists():
            messages.error(request, "Já existe um curso com esse nome cadastrado nessa escola.")
            return render(request, 'apps/instituicao/curso/cadastrar.html', {'escolas': escolas})
         
   
        escola = get_object_or_404(Escola, pk= escola_id)
      
        
        # Cadastrar
        Curso.objects.create(
            nome=nome,
            modalidade = modalidade,
            escola = escola,
            descricao=descricao,
            nivel=nivel,
            ativo=ativo,
           
        )
        

        messages.success(request, f'Curso {nome} cadastrado com sucesso!')
        return redirect('school:listar_cursos')

   return render(request, 'apps/instituicao/curso/cadastrar.html', {'escolas':escolas})
 
      

# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    
    #
    curso = get_object_or_404(Curso, pk=id)
    escolas = Escola.objects.all()
    


    if request.method == 'POST':
      
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        modalidade = request.POST.get('modalidade')
        nivel = request.POST.get('nivel')
        ativo = request.POST.get('ativo') == 'on'
        escola_id = request.POST.get('escola')
       
       
   
        
        
          # Validações
        if not all([nome, modalidade, nivel, ativo,escola_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/curso/atualizar.html', {'escolas':escolas, 'curso':curso})

         
   
        escola = get_object_or_404(Escola, pk= escola_id)

        curso.nome=nome
        curso.modalidade = modalidade
        curso.escola = escola
        curso.descricao=descricao
        curso.nivel=nivel
        curso.ativo=ativo
        curso.save(force_update=True)
  

        messages.success(request, f'Curso {nome} atualizado com sucesso!')
        return redirect('school:listar_cursos')

  
    return render(request, 'apps/instituicao/curso/atualizar.html',{'escolas':escolas, 'curso':curso})
 
 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    curso = get_object_or_404(Curso, id=id)
    escola = curso.escola

    
    if request.method == 'POST':
      
        curso.delete()
        return redirect('school:listar_cursos')  
    
    dados ={
       
        'curso':curso,
        'escola':escola ,
        }
      
    return render(request, 'apps/instituicao/curso/eliminar.html', dados )
  
   
   
   
   
   
   
   
   
   