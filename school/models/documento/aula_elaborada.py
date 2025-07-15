from django.db import models
from ..academico.professor import Professor
from ..academico.disciplina import Disciplina
from ..academico.turma import Turma
from ..academico.base import Base

#
class AulaElaborada(Base):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    tema = models.CharField(max_length=255)
    subtema = models.CharField(max_length=255, null=True)
    objetivos = models.TextField()
    conteudo = models.TextField()
    metodologia = models.TextField()
    recursos = models.TextField()
    avaliacao = models.TextField()

    def __str__(self):
        return f"Aula de {self.disciplina} - {self.turma} ({self.data})"
