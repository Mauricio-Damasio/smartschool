from django.contrib import admin






from .models.academico.curso import Curso
from .models.academico.departamento import Departamento
from .models.academico.aluno import Aluno
from .models.academico.classe import Classe
from .models.academico.professor import Professor
from .models.academico.turma import Turma
from .models.academico.disciplina import Disciplina
from .models.academico.diretor_geral import Diretor
from .models.academico.diretor_pedagogico import Pedagogico
from .models.academico.diretor_administrativo import DiretorAdministrativo
from .models.academico.escola import Escola
from .models.academico.disciplinaLecionada import DisciplinaLecionada

from .models.localizacao.provincia import Provincia
from .models.localizacao.municipio import Municipio
from .models.localizacao.bairro import Bairro
from .models.relatorio.minipauta import MiniPauta
from .models.academico.ano_lectivo import AnoLetivo





admin.site.register(Aluno)
admin.site.register(Professor)
admin.site.register(Turma)
admin.site.register(Curso)
admin.site.register(Classe)
admin.site.register(Disciplina)
admin.site.register(Diretor)
admin.site.register(Pedagogico)
admin.site.register(DiretorAdministrativo)
admin.site.register(Provincia)
admin.site.register(Municipio)
admin.site.register(Bairro)
admin.site.register(Escola)
admin.site.register(Departamento)
admin.site.register(MiniPauta)
admin.site.register(AnoLetivo)
admin.site.register(DisciplinaLecionada)