from django.db import models
from .base import Base
from .curso import Curso
from .classe import Classe

class Disciplina(Base):
  
  nome = models.CharField(max_length=50)
  curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
  classe = models.ForeignKey(Classe, on_delete=models.SET_NULL, null=True)
  descricao = models.TextField(null=True, blank=True)
    
  class Meta:
    
    db_table = 'Disciplina'
    
  def __str__(self):
      if self.curso:
          return f"{self.nome} - {self.curso.nome}"
      return self.nome or "Disciplina sem nome"
   