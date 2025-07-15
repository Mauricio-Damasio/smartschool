from django.urls import path
from  ....views.instituicao.curso.curso import index, visualizar,cadastrar,atualizar,eliminar

urlpatterns = [
    path('', index, name="listar_cursos"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_curso"),
    path('cadastrar/', cadastrar, name="cadastrar_curso"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_curso"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_curso"),
]

