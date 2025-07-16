from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.diretor_geral import Diretor
from django.contrib import messages
import re
from datetime import date
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from school.models.academico.escola import Escola

# Listar professores
@login_required
def index(request: HttpRequest):
  
  # Carregar todos os dados para os selects
  direitores = Diretor.objects.all().order_by('-id')
  escolas = Escola.objects.all()
  
  
  # Obter filtros
  escola = request.GET.get('escola')
  
  if escola:
    
    direitores = Diretor.objects.filter(escola=escola)
  
  
  return render(request , 'apps/instituicao/direitor/index.html',{'direitores':direitores, 'escolas': escolas})
  
  
  
# Visualizar professor
@login_required  
def visualizar(request:HttpRequest,id:int):
    direitor = get_object_or_404(Diretor, id=id)
   

    dados = {
        'direitor': direitor,
       
    }
    return render(request, 'apps/instituicao/direitor/visualizar.html', dados)
 

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
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

       

       # Verificar se o número de agente já existe
        if Diretor.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

    
       
        
        
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
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

       
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

       
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

       

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/instituicao/direitor/cadastrar.html')

       
        
        
        # # #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Direitor')
        user.groups.add(grupo)
        
        
        
        
        # Cadastrar
        direitor = Diretor.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            user=user,
       
           
        )
        
       
        direitor.save()

        messages.success(request, f'Direitor (a) {nome} cadastrado com sucesso!')
        return redirect('school:listar_direitores')

   return render(request, 'apps/instituicao/direitor/cadastrar.html')

       


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    direitor = get_object_or_404(Diretor, pk=id)
   


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or direitor.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
       
        

        if not all([nome, numAgente, genero]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/direitor/atualizar.html', {'direitor':direitor})



        direitor.nome = nome
        direitor.genero = genero
        direitor.numAgente = numAgente
       
       
        if image:
           direitor.image = image

        direitor.save(force_update=True)
       

        messages.success(request, f'Direitor(a) {nome} atualizado com sucesso!')
        return redirect('school:listar_direitores')

    return render(request, 'apps/instituicao/direitor/atualizar.html', {'direitor':direitor})


 
 
#Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    direitor = get_object_or_404(Diretor, id=id)

    
    if request.method == 'POST':
      
        direitor.delete()
        return redirect('school:listar_direitores')  
      
    return render(request, 'apps/instituicao/direitor/eliminar.html', {'direitor': direitor})
   
   
      
   
   
   
   
   
   
   
   