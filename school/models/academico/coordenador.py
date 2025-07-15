from django.db import models
from .pessoa import Pessoa
from .curso import Curso
from .departamento import Departamento
from django.contrib.auth.models import User

class Coordenador(Pessoa):
  
  numAgente = models.CharField(max_length=25, unique=True, null=True)
  departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
  curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  
  class Meta:
    
    db_table = 'Coordenador'
    
  def __str__(self):
    
      return f'{self.nome}-{self.numAgente}'
  