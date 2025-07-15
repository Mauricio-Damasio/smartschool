from django.urls import path
from ...views.curso.curso import index

urlpatterns = [
    
    path('', index, name='index'),
]
