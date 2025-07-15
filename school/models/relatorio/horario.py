from django.db import models
from ..academico.base import Base
from ..academico.disciplina import Disciplina
from ..academico.turma import Turma
from ..academico.professor import Professor

class Horario(Base):
    TIPO_CHOICES = [
        ('aula', 'Aula'),
        ('prova', 'Prova'),
    ]

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    dia_semana = models.CharField(max_length=10, choices=[
        ('segunda', 'Segunda-feira'),
        ('terca', 'Terça-feira'),
        ('quarta', 'Quarta-feira'),
        ('quinta', 'Quinta-feira'),
        ('sexta', 'Sexta-feira'),
        ('sabado', 'Sábado'),
    ])
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()

    class Meta:
        ordering = ['dia_semana', 'hora_inicio']
        unique_together = ('turma', 'disciplina', 'dia_semana', 'hora_inicio', 'tipo')

    def __str__(self):
        return f"{self.turma.nome} - {self.disciplina.nome} ({self.get_tipo_display()})"
