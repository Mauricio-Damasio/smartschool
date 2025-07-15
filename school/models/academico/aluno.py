from django.db import models
from .pessoa import Pessoa
from .turma import Turma
from django.contrib.auth.models import User

class Aluno(Pessoa):
  
  idade = models.IntegerField(default=0)
  telefone = models.CharField(max_length=9)
  data_nascimento = models.DateField()
  bilhete = models.CharField(max_length=20, unique=True)
  turma = models.ForeignKey(Turma, on_delete=models.SET_NULL, null=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

  
  class Meta:
    db_table = 'aluno'
    
  def __str__(self):
    return self.nome or "Sem nome"

    