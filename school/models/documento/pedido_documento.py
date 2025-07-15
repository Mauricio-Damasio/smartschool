from django.db import models
from ..academico.base import Base
from ..academico.aluno import Aluno
from django.contrib.auth.models import User

class PedidoDocumento(Base):
    TIPO_CHOICES = [
        ('c', 'Certificado'),
        ('d', 'Declaração'),
        ('h', 'Histórico'),
    ]

    STATUS_CHOICES = [
        ('p', 'Pendente'),
        ('a', 'Aprovado'),
        ('r', 'Rejeitado'),
    ]

    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p')
    observacao = models.TextField(blank=True, null=True)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_validacao = models.DateTimeField(blank=True, null=True)
    validado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.aluno} - {self.get_tipo_display()} ({self.get_status_display()})"
