from django.urls import path
from  ....views.ui.professor.professor import index,visualizar,cadastrar,atualizar,eliminar,dashboard_professor,perfil
urlpatterns = [
    path('dashboard_professor/', dashboard_professor, name="dashboard_professor"),
    path('listar/', index, name="listar_professores"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_professor"),
    path('perfil/<int:id>/', perfil, name="perfil_professor"),
    path('cadastrar/', cadastrar, name="cadastrar_professor"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_professor"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_professor"),
]

