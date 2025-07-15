from django.urls import path
from  school.views.instituicao.departamento.departamento import index, visualizar ,cadastrar,atualizar,eliminar

urlpatterns = [
    path('', index, name="listar_departamentos"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_departamento"),
    path('cadastrar/', cadastrar, name="cadastrar_departamento"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_departamento"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_departamento"),
]

