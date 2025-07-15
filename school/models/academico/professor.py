from django.db import models
from .pessoa import Pessoa
from .departamento import Departamento
from django.contrib.auth.models import User

class Professor(Pessoa):
  
   
   numAgente = models.CharField(max_length=25, unique=True)
   departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
   user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
   
   
   class Meta:
      db_table = 'Professor'
      
   def __str__(self):
     
    return f'{self.nome}'