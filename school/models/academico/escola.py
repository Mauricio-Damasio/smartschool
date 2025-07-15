from django.db import models
from .base import Base

from .diretor_geral import Diretor
from .diretor_pedagogico import Pedagogico
from .diretor_administrativo import DiretorAdministrativo

from ..localizacao.provincia import Provincia
from ..localizacao.municipio import Municipio
from ..localizacao.bairro import Bairro

from ..academico.classe import Classe





class Escola(Base):
  
  
  TIPO_ESCOLA = [
    ('EP','Ensino Primário'),
    ('PC','Primeiro Ciclo '),
    ('SC','Segundo Ciclo'),
  ]
  
  nome = models.CharField(max_length=20)
  nif = models.CharField(max_length=15)
  provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL,null=True)
  municipio = models.ForeignKey(Municipio, on_delete=models.SET_NULL,null=True)
  bairro = models.ForeignKey(Bairro, on_delete=models.SET_NULL,null=True)
  direitor = models.ForeignKey(Diretor, on_delete=models.SET_NULL, null=True)
  direitor_pedagogico = models.ForeignKey(Pedagogico, on_delete=models.SET_NULL, null=True)
  direitor_administrativo = models.ForeignKey(DiretorAdministrativo, on_delete=models.SET_NULL, null=True)
  logo = models.ImageField(upload_to='media/logo/', blank=True, null=True)
  alvara = models.FileField(upload_to='alvara/', blank=True, null=True)
  tipo_escola = models.CharField(max_length=2, choices=TIPO_ESCOLA)
  classes = models.ManyToManyField(Classe, blank=True)
  

  

    
  class Meta:
    db_table = 'Escola'
    
  def __str__(self):
   return f'{self.nome}-{self.direitor.nome}'
  
  
  
  
  
  
  
  
  '''
    def get_professores(self):
        return Professor.objects.filter(departamento__curso__escola=self)

    def get_alunos(self):
        return Aluno.objects.filter(turma__curso__escola=self)

    def get_disciplinas(self):
        return Disciplina.objects.filter(curso__escola=self)'''