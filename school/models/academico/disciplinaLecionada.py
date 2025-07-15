
from django.db import models
from .professor import Professor
from .disciplina import Disciplina

from .turma import Turma
from .base import Base

class DisciplinaLecionada(Base):
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE,null=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('turma', 'disciplina')  # Em uma turma, uma disciplina só pode ser lecionada por um professor
        db_table = 'DisciplinaLecionada'

    def __str__(self):
        return f"{self.professor.nome} - {self.disciplina.nome} - {self.turma.nome}"




    