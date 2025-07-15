from django.db import models
from .base import Base
from .escola import Escola


class Curso(Base):
  
  MODALIDADE_CHOICES =(
    ('P', 'Presencial'),
    ('O','Online'),
    ('S','Semi-presencial')
  )
  
  NIVEL_CHOICES = (
    ('T','Técnico'),
    ('G','Graduação'),
    ('P','Pós-graduação')
  )

  
  nome = models.CharField(max_length=50)
  descricao = models.TextField()
  modalidade = models.CharField(max_length=1, choices=MODALIDADE_CHOICES)
  nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES)
  ativo = models.BooleanField(default=True)
  escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
  
  class Meta:
    
    db_table = 'Curso'
    
  def __str__(self):
      return f'{self.nome}'
  