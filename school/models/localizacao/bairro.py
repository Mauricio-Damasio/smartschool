from django.db import models
from ..academico.base import Base

class Bairro(Base):
  
  nome = models.CharField(max_length=50)

  
  
  class Meta:
    
    db_table = "Bairro"
    
  def __str__(self):
      return self.nome
  