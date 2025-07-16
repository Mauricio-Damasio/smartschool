from django.urls import path
from  ....views.instituicao.direitor.direitor import index, visualizar,cadastrar,atualizar,eliminar

urlpatterns = [
    path('', index, name="listar_direitores"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_direitor"),
    path('cadastrar/', cadastrar, name="cadastrar_direitor"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_direitor"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_direitor"),
]

