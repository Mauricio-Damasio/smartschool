from django.db import models
from ..academico.base import Base

class Municipio(Base):
  
  nome = models.CharField(max_length=50)
  cidade = models.CharField(max_length=50)

  
  
  class Meta:
    
    db_table = "Municipio"
    
  def __str__(self):
      return self.nome
  