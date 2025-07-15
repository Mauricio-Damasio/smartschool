from django.db import models
from ..academico.disciplina import Disciplina
from ..academico.turma import Turma






TRIMESTRE_CHOICES = (
    (1, "1º Trimestre"),
    (2, "2º Trimestre"),
    (3, "3º Trimestre"),
)

class TrimestreLiberado(models.Model):
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    trimestre = models.IntegerField(choices=TRIMESTRE_CHOICES)
    liberado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('turma', 'disciplina', 'trimestre')

    def __str__(self):
     return f"{self.turma} | {self.disciplina} | {self.get_trimestre_display()} | {'Liberado' if self.liberado else 'Bloqueado'}"
