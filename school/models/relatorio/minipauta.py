from django.db import models
from ..academico.aluno import Aluno
from ..academico.professor import Professor
from ..academico.disciplina import Disciplina
from ..academico.turma import Turma
from django.core.validators import MinValueValidator, MaxValueValidator





class MiniPauta(models.Model):
    
    TRIMESTRES = (
    ('1', '1º Trimestre'),
    ('2', '2º Trimestre'),
    ('3', '3º Trimestre'),
)

  
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=1, choices=TRIMESTRES)




    av1 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    av2 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    av3 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])
    av4 = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(20)])

    mac = models.FloatField(null=True, blank=True)
    npp = models.FloatField(null=True, blank=True)
    npt = models.FloatField(null=True, blank=True)
    mt = models.FloatField(null=True, blank=True) 
    
    exame = models.FloatField(default=0) 
    mf = models.FloatField(default=0) 
    
 
    
    class Meta:
        unique_together = ('aluno', 'disciplina', 'trimestre')
  


    
    def __str__(self):
     return f"{self.aluno.nome} - {self.disciplina.nome} - {self.get_trimestre_display()}º Tri"



'''      
    @property
    def media_mac(self):
        avs = [self.av1, self.av2, self.av3, self.av4]
        notas = [n for n in avs if n is not None]
        return round(sum(notas)/len(notas), 1) if notas else None'''