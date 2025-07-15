from django.db import models

class Base(models.Model):
  
   
  criado = models.DateTimeField(auto_now_add=True )
  modificado = models.DateTimeField(auto_now=True)
  
  class Meta:
    
    abstract = True