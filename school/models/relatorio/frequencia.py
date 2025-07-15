from django.db import models
from ..academico.professor import Professor
from ..academico.aluno import Aluno
from ..academico.turma import Turma
from ..academico.base import Base


class Frequencia(Base):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    data = models.DateField()
    presente = models.BooleanField()
    
    