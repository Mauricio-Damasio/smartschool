from django.db import models
from ..academico.base import Base
from ..academico.professor import Professor
from ..academico.coordenador import Coordenador

class Assiduidade(Base):
    data = models.DateField()
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField()
    cargo = models.CharField(max_length=50, choices=[('Professor', 'Professor'), ('Coordenador', 'Coordenador')])

    professor = models.ForeignKey(
        Professor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assiduidades'
    )
    coordenador = models.ForeignKey(
        Coordenador,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assiduidades'
    )

    observacoes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro de Assiduidade"
        verbose_name_plural = "Registros de Assiduidade"
        ordering = ['-data', 'hora_entrada']

    def __str__(self):
        nome = self.professor.nome if self.professor else self.coordenador.nome
        return f"{nome} - {self.data} ({self.cargo})"
