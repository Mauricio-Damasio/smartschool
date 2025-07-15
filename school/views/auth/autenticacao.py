from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import re
from django.contrib.auth import authenticate, login,  logout


# Autenticação
def autenticacao(request:HttpRequest):
  return render(request, 'apps/auth/loginAndRegister.html')


# Recebendo o email para ser verificado se é válido
def email_valido(email):
  return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Registro
def registrar(request:HttpRequest):
  
  if request.method == 'POST':
    
    username = request.POST.get('username')
    email = request.POST.get('email')
    senha = request.POST.get('senha')
    
    # Verificar campos vazios
    if not username and not email and not senha:
      messages.error(request, 'Todos os campos são obrigatório!')
      return redirect('school:registrar')
    
    if not username:
      messages.error(request, 'O username é obrigatório!')
      return redirect('school:registrar')
    
    if not email:
      messages.error(request, 'O email é obrigatório!')
      return redirect('school:registrar')
    
    if not senha:
      messages.error(request, 'A senha é obrigatória!')
      return redirect('school:registrar')
    
    # Verificar se o email é válido
    if not email_valido(email):
      messages.error(request, 'Email inválido! Digite um email válido, ex: smartschool@gmail.com')
      return redirect('school:registrar')
      
    # Verificar se a senha tem pelo menos 8 dígitos
    if len(senha) < 8:
      messages.error(request, 'A senha tem que ter pelo menos 8 dígitos!')
      return redirect('school:registrar')
      
    # Verificar se o email já existe
    if User.objects.filter(email=email).exists():
      messages.error(request, f'O email {email}, já existe! Digite um email diferente.')
      return redirect('school:registrar')
      
    # Verificar se o usuário já existe
    if User.objects.filter(username=username).exists():
      messages.error(request, f'O usuário {username}, já existe! Digite um usuário diferente')
      return redirect('school:registrar')
      
    # Cadastrar
    User.objects.create_user(username=username,email=email,password=senha)
    messages.success(request, f'{username}, a sua conta foi criada com sucesso!')
    return redirect('school:autenticacao')
    
    
  return render(request, 'apps/auth/loginAndRegister.html')










# Login


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)

            # Redireciona conforme o perfil
            
            
            #Super Admin
            if user.is_superuser:
                return redirect('school:dashboard_superAdmin')
             
            #Escola Admin  
            elif hasattr(user, 'diretor'):
                return redirect('school:dashboard_admin')
            
            #Aluno  
            elif hasattr(user, 'aluno'):
                return redirect('school:dashboard_aluno')
            
            #Professor  
            elif hasattr(user, 'professor'):
                return redirect('school:dashboard_professor')
            
            #Diretor  
            elif hasattr(user, '#'):
                return redirect('school:dashboard_direitor')
              
            #Pedagógico 
            elif hasattr(user, 'pedagogico'):
                return redirect('school:dashboard_pedagogico')
             
            #Administrativo  
            elif hasattr(user, 'diretoradministrativo'):
                return redirect('school:dashboard_administrativo')
              
            #Coordenador
            elif hasattr(user, 'coordenador'):
                return redirect('school:dashboard_coordenador')
            else:
                messages.error(request, 'Usuário sem perfil associado.')
                return redirect('school:login_view')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return redirect('school:login_view')

    return render(request, 'apps/auth/loginAndRegister.html')


def logout_view(request):
    logout(request)
    return redirect('school:web_page')


'''def login_view(request:HttpRequest):
  
  if request.method == 'POST':
    
    username = request.POST.get('username')
    senha = request.POST.get('senha')
    
    
    # Verificar campos vazios
    if not username and not senha:
      messages.error(request, 'Todos os campos são obrigatórios!')
      return redirect('school:login_view')
    
    if not username:
      messages.error(request, 'O username é obrigatório!')
      return redirect('school:login_view')
    
    if not senha:
      messages.error(request, 'A senha é obrigatória!')
      return redirect('school:login_view')
    
    # Verificar se o usuário existe
    try:
      
      User.objects.get(username=username)
    
    except User.DoesNotExist:
      
      messages.error(request , 'Usuário não encontrado!')
      return redirect('school:login_view')
      
    
    # Autenticando usuário
    user = authenticate(username=username, password=senha)
    
    # Verificar se não é vazio
    if user is not None:
      
      login(request, user)
      messages.success(request, f'Bem-vindo(a), {username}!')
      return redirect('school:home_page')
    
    else:
      messages.error(request, 'Senha incorreta!')
      return redirect('school:login_view')
      
    
  return render(request, 'apps/auth/loginAndRegister.html')
  
  '''