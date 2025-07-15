from django.urls import path
from  ....views.ui.disciplina.disciplina import index,visualizar,cadastrar, atualizar, eliminar



urlpatterns = [
    path('', index, name="listar_disciplinas"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_disciplina"),
    path('cadastrar/', cadastrar, name="cadastrar_disciplina"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_disciplina"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_disciplina"),
  
]

