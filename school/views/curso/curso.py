from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators  import login_required

from ...models.academico.curso import Curso


@login_required
def index(request:HttpRequest):
  
  cursos = Curso.objects.all()
  
  #
  num_visits = request.session.get('num_visits', 0)
  num_visits += 1
  request.session['num_visits'] = num_visits
  
  return render(request , 'apps/curso/index.html', {'cursos':cursos, 'num_visits':num_visits})
  