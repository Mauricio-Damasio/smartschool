from django.urls import path
from ...views.configuracao.personalizar import personalizar





urlpatterns = [
    

    path('personalizar/', personalizar, name="personalizar"),
]
