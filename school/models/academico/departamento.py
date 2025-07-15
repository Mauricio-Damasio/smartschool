from django.db import models
from .base import Base
from .curso import Curso

class Departamento(Base):
  
  nome = models.CharField(max_length=50, null=True)
  curso = models.ForeignKey(Curso, on_delete=models.CASCADE, null=True)
  
  class Meta:
    
    db_table = 'Departamento'
    
  def __str__(self):
    
      return self.nome