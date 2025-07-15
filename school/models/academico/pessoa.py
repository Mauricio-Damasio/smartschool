from django.db import models
from .base import Base

class Pessoa(Base):
  
   GENERO = [
    
    ('M','Masculino'),
    ('F','Femenino'),
  ]
   
   nome = models.CharField(max_length=100)
   genero = models.CharField(max_length=1, choices=GENERO)
   image = models.ImageField(upload_to='imagem', blank=True, null=True)
   
   
   class Meta:
     
     abstract = True
   