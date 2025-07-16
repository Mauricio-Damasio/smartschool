from django.urls import path
from  ....views.instituicao.administrativo.administrativo import index, visualizar,cadastrar,atualizar,eliminar

urlpatterns = [
    path('', index, name="listar_administrativos"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_administrativo"),
    path('cadastrar/', cadastrar, name="cadastrar_administrativo"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_administrativo"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_administrativo"),
]

