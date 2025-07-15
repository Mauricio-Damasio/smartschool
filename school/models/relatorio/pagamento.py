from django.db import models
from ..academico.aluno import Aluno
from ..academico.base import Base

# Pagamento
class Pagamento(Base):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_pagamento = models.DateField(null=True, blank=True)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    mes_referente = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=[('Pago', 'Pago'), ('Pendente', 'Pendente')])
