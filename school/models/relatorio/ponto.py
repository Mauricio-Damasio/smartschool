from django.db import models
from django.utils import timezone
from ..academico.base import Base


class Ponto(Base):
    TIPO_USUARIO = (
        ('P', 'Professor'),
        ('C', 'Coordenador'),
    )
    tipo = models.CharField(max_length=1, choices=TIPO_USUARIO)
    usuario_id = models.PositiveIntegerField(default=0)
    data = models.DateField(default=timezone.now)
    hora_entrada = models.TimeField()
    hora_saida = models.TimeField(blank=True, null=True)
    observacao = models.TextField(blank=True)

    def __str__(self):
        nome = f'Usuário {self.usuario_id}'
        if self.tipo == 'P':
            from ..academico.professor import Professor
            prof = Professor.objects.filter(id=self.usuario_id).first()
            nome = prof.nome if prof else nome
        elif self.tipo == 'C':
            from ..academico.coordenador import Coordenador
            coord = Coordenador.objects.filter(id=self.usuario_id).first()
            nome = coord.nome if coord else nome
        return f"{self.get_tipo_display()} {nome} - {self.data}"


