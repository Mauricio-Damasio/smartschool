from django.urls import path
from ...views.webpage.webpage import web_page





urlpatterns = [
    
    path('', web_page, name="web_page"),


   
]

