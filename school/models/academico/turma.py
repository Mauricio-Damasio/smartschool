from django.db import models
from .base import Base
from .classe import Classe
from .curso import Curso
from .ano_lectivo import AnoLetivo


class Turma(Base):
  

    
  TURNO_CHOICES = (
   
    ('M','Manhâ'),
    ('T','Tarde' ),
    ('N','Noite'),
  )
  

  nome = models.CharField(max_length=10, null=True)
  turno = models.CharField(max_length=1, choices=TURNO_CHOICES, null=True)
  classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
  curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
  ano_lectivo = models.ForeignKey(AnoLetivo, on_delete=models.CASCADE)
  
  class Meta:
    
    db_table: 'Turma'
    unique_together = ('nome', 'curso', 'classe')  # Garante que "Turma A" possa existir em vários cursos/classes
    
    
  def __str__(self):
     return self.nome 