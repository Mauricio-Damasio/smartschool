
from django.db import models
from django.utils import timezone
from ..academico.base import Base



class Desempenho(Base):
    TIPO_USUARIO = (
        ('P', 'Professor'),
        ('C', 'Coordenador'),
    )
    tipo = models.CharField(max_length=15, choices=TIPO_USUARIO)
    usuario_id = models.PositiveIntegerField()
    data_avaliacao = models.DateField(default=timezone.now)
    nota = models.DecimalField(max_digits=4, decimal_places=2)
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f"{self.tipo} {self.usuario_id} - {self.nota}"
