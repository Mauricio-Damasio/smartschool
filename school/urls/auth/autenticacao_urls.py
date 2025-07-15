from django.urls import path
from ...views.auth.autenticacao import autenticacao,registrar,login_view,logout

urlpatterns = [
    path('', autenticacao, name='autenticacao'),
    path('cadastrar/', registrar, name='registrar'),
    path('login/', login_view, name='login_view'),
    path('logout/', logout, name='logout'),
]
