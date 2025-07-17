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
    total_escolas = Escola.objects.count()
    total_cursos = Curso.objects.count()
    total_classes = Classe.objects.count()
    total_diretores = Diretor.objects.count()
    total_pedagogicos = Pedagogico.objects.count()
    total_administrativos = DiretorAdministrativo.objects.count()

    dados = {
        'total_escolas': total_escolas,
        'total_cursos': total_cursos,
        'total_classes': total_classes,
        'total_diretores': total_diretores,
        'total_pedagogicos': total_pedagogicos,
        'total_administrativos': total_administrativos,
        'dashboard_items': [
            {"id": "Escolas", "label": "Escolas", "total": total_escolas, "color": "success", "icon": "bi bi-building"},
            {"id": "Cursos", "label": "Cursos", "total": total_cursos, "color": "primary", "icon": "bi bi-book"},
            {"id": "Classes", "label": "Classes", "total": total_classes, "color": "danger", "icon": "bi bi-easel"},
            {"id": "Diretores", "label": "Diretores", "total": total_diretores, "color": "warning", "icon": "bi bi-person"},
            {"id": "Pedagogicos", "label": "Subdir. Pedagógicos", "total": total_pedagogicos, "color": "dark", "icon": "bi bi-person-badge"},
            {"id": "Administrativos", "label": "Subdir. Administrativos", "total": total_administrativos, "color": "secondary", "icon": "bi bi-briefcase"},
        ]
    }

    return render(request, "apps/home/home_page.html", dados)

