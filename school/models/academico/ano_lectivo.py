from django.db import models

class AnoLetivo(models.Model):
    nome = models.CharField(max_length=20, unique=True)  
    data_inicio = models.DateField()
    data_fim = models.DateField()
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['-data_inicio']
