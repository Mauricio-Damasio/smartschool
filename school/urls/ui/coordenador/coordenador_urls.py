from django.urls import path
from  ....views.ui.coordenador.coordenador import index,visualizar,cadastrar,atualizar, eliminar



urlpatterns = [
    path('', index, name="listar_coordenadores"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_coordenador"),
    path('cadastrar/', cadastrar, name="cadastrar_coordenador"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_coordenador"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_coordenador"),
  
]

