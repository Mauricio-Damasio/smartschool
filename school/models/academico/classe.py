from django.db import models
from .base import Base



class Classe(Base):
  
  PRIMARIA_CHOICES = (
      
      ('0','0ª'),
      ('1','1ª'),
      ('2','2ª'),
      ('3','3ª'),
      ('4','4ª'),
      ('5','5ª'),
      ('6','6ª'),
      
  )
  PRIMEIRO_CICLO_CHOICES = (
      
      ('7','7ª'),
      ('8','8ª'),
      ('9','9ª'),
    
      
  )
  SEGUNDO_CICLO_CHOICES = (
      
      ('10','10ª'),
      ('11','11ª'),
      ('12','12ª'),
      ('13','13ª'),
      
  )
  
  ensino_primario = models.CharField(max_length=1, choices=PRIMARIA_CHOICES, null=True, blank=True)
  primeiro_ciclo = models.CharField(max_length=1, choices=PRIMEIRO_CICLO_CHOICES, null=True, blank=True)
  segundo_ciclo = models.CharField(max_length=2, choices=SEGUNDO_CICLO_CHOICES, null=True, blank=True)

    
  class Meta:
    db_table = 'Classe'
    
  def __str__(self):
    if self.ensino_primario:
        return f"{self.get_ensino_primario_display()}"
    elif self.primeiro_ciclo:
        return f"{self.get_primeiro_ciclo_display()}"
    elif self.segundo_ciclo:
        return f"{self.get_segundo_ciclo_display()}"
    return "Classe não definida"

    
  
  
