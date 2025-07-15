from django.urls import path
from ...views.home.home_page import dashboard_superAdmin





urlpatterns = [
    
    path('dashboard_superAdmin/', dashboard_superAdmin, name="dashboard_superAdmin"),
   
]

