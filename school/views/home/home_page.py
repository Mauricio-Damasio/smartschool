from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from school.models.academico.escola import Escola
from school.models.academico.curso import Curso
from school.models.academico.classe import Classe
from school.models.academico.diretor_geral import Diretor
from school.models.academico.diretor_pedagogico import Pedagogico
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from school.models.localizacao.provincia import Provincia
from school.models.localizacao.municipio import Municipio
from school.models.localizacao.bairro import Bairro

from django.db.models import Count



@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard_superAdmin(request):
    dados = {
        'total_escolas': Escola.objects.count(),
        'total_cursos': Curso.objects.count(),
        'total_classes': Classe.objects.count(),
        'total_diretores': Diretor.objects.count(),
        'total_pedagogicos': Pedagogico.objects.count(),
        'total_administrativos': DiretorAdministrativo.objects.count(),
        'total_provincias': Provincia.objects.count(),
        'total_municipios': Municipio.objects.count(),
        'total_bairros': Bairro.objects.count(),
    }
    return render(request,  "apps/home/home_page.html", dados)
