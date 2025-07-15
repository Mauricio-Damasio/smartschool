from django.urls import path
from  ....views.ui.classe.classe import index,visualizar,cadastrar,atualizar,eliminar



urlpatterns = [
    path('', index, name="listar_classes"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_classe"),
    path('cadastrar/', cadastrar, name="cadastrar_classe"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_classe"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_classe"),
  
]

