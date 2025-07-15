from django.shortcuts import render
from django.http import HttpRequest
from school.models.academico.escola import Escola

def web_page(request:HttpRequest):
    
   escolas = Escola.objects.all()
   
   return render(request, "apps/web/webpage.html", {'escolas':escolas})

