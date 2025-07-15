from django.urls import path
from  ....views.ui.turma.turma import index,visualizar,cadastrar,atualizar,eliminar



urlpatterns = [
    path('', index, name="listar_turmas"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_turma"),
    path('cadastrar/', cadastrar, name="cadastrar_turma"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_turma"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_turma"),
  
]

