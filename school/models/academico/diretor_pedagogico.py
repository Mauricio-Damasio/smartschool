from django.db import models
from .pessoa import Pessoa
from django.contrib.auth.models import User

class Pedagogico(Pessoa):

  
  numAgente = models.CharField(max_length=25, unique=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  
  class  Meta:
    
    db_table = 'Pedagogico'
    
  def __str__(self):
    
      return self.nome