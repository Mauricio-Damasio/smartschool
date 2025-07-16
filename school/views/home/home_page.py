from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from school.models.academico.turma import Turma
from school.models.academico.aluno import Aluno
from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from django.db.models import Count



@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_superAdmin(request):
  #  curso_id = request.GET.get('curso')
    turmas = Turma.objects.all()

  ##  if curso_id:
       # turmas = turmas.filter(curso_id=curso_id)

    alunos_por_turma = turmas.annotate(total_alunos=Count('aluno'))

    context = {
        'total_alunos': Aluno.objects.count(),
        'total_professores': Professor.objects.count(),
        'total_turmas': Turma.objects.count(),
        'total_disciplinas': Disciplina.objects.count(),
        'alunos_por_turma': alunos_por_turma,
     #   'cursos': Curso.objects.all(),
    }
    return render(request,  "apps/home/home_page.html", context)