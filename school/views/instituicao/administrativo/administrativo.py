from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.diretor_administrativo import DiretorAdministrativo
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
  administrativos = DiretorAdministrativo.objects.all().order_by('-id')
  escolas = Escola.objects.all()
  
  
  # Obter filtros
  escola = request.GET.get('escola')
  
  if escola:
    
    administrativos = DiretorAdministrativo.objects.filter(escola=escola)
  
  
  return render(request , 'apps/instituicao/administrativo/index.html',{'administrativos':administrativos, 'escolas': escolas})
  
  
  
# Visualizar administrativo
@login_required  
def visualizar(request:HttpRequest,id:int):
    administrativo = get_object_or_404(DiretorAdministrativo, id=id)
   

    dados = {
        'administrativo': administrativo,
       
    }
    return render(request, 'apps/instituicao/administrativo/visualizar.html', dados)
 

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
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       

       # Verificar se o número de agente já existe
        if DiretorAdministrativo.objects.filter(numAgente=numAgente).exists():
            messages.error(request, 'O número de agente já existe!')
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

    
       
    
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
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        #
        if  not email_valido(email):
          
            messages.error(request, "E-mail inválido.")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        #
        if  not username:
          
            messages.error(request, "Insira o nome do usuário!")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       

        #
        if senha != senha_confirmar:
            messages.error(request, "As senhas não correspondem!")
            return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       
        
        
        #  # #
        user = User.objects.create_user(username=username, email=email,password=senha)
        grupo = Group.objects.get(name='Administrativo')
        user.groups.add(grupo)
        
        
    
        
        # Cadastrar
        administrativo = DiretorAdministrativo.objects.create(
            nome=nome,
            genero=genero,
            image=image,
            numAgente=numAgente,
            user=user,
       
           
        )
        
       
        administrativo.save()

        messages.success(request, f'Direitor (a) administrativo {nome} cadastrado com sucesso!')
        return redirect('school:listar_administrativos')

   return render(request, 'apps/instituicao/administrativo/cadastrar.html')

       


# Atualizar

@login_required
def atualizar(request: HttpRequest, id: int):
    administrativo = get_object_or_404(DiretorAdministrativo, pk=id)
   


    if request.method == 'POST':
        nome = request.POST.get('nome')
        genero = request.POST.get('genero')
        image = request.FILES.get('image') or administrativo.image  # Mantém a imagem se não for alterada
        numAgente = request.POST.get('numAgente')
       
        

        if not all([nome, numAgente, genero]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituica/administrativo/atualizar.html', {'administrativo':administrativo})



        administrativo.nome = nome
        administrativo.genero = genero
        administrativo.numAgente = numAgente
       
       
        if image:
           administrativo.image = image

        administrativo.save(force_update=True)
       

        messages.success(request, f'Direitor(a) administrativo {nome} atualizado com sucesso!')
        return redirect('school:listar_administrativos')

    return render(request, 'apps/instituicao/administrativo/atualizar.html', {'administrativo':administrativo})


 
 
#Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    administrativo = get_object_or_404(DiretorAdministrativo, id=id)

    
    if request.method == 'POST':
      
        administrativo.delete()
        return redirect('school:listar_administrativos')  
      
    return render(request, 'apps/instituicao/administrativo/eliminar.html', {'administrativo': administrativo})
   
   
      
   
   
   
   
   
   
   
   