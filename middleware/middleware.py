from django.shortcuts import redirect
from django.urls import reverse

class RedirecionaPorPerfilMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.path == reverse('school:dashboard_superAdmin'):
            return self.get_response(request)

        if request.user.is_authenticated and request.path == '/':
            if request.user.is_superuser:
                return redirect('school:dashboard_superAdmin')
            
            #Escola
            elif request.user.groups.filter(name='Direitor').exists():
                return redirect('school:dashboard_admin')
            
            
            #Pedagógico
            elif request.user.groups.filter(name='Pedagogico').exists():
                return redirect('school:dashboard_pedagogico')
            
            #Administrativo
            elif request.user.groups.filter(name='Administrativo').exists():
                return redirect('school:dashboard_administrativo')
            
            #Coordenador
            elif request.user.groups.filter(name='Coordenador').exists():
                return redirect('school:dashboard_coordenador')
            
            #Professor
            elif request.user.groups.filter(name='Professor').exists():
                return redirect('school:dashboard_professor')
            
            #Aluno
            elif request.user.groups.filter(name='Aluno').exists():
                return redirect('school:dashboard_aluno')

        return self.get_response(request)

