from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def personalizar(request):
  return render(request, 'apps/configuracao/personalizacao/index.html')  
  