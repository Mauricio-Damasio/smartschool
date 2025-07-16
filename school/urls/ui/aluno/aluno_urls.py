from django.urls import path
from  ....views.ui.aluno.aluno import index, visualizar,cadastrar,atualizar,eliminar,dashboard_aluno,perfil
from ....views.ui.aluno.relatorio import relatorio_alunos_por_ano, relatorio_alunos_pdf

urlpatterns = [
    
    
    path('dashboard_aluno/', dashboard_aluno, name="dashboard_aluno"),
    path('listar/', index, name="listar_alunos"),
    path('perfil/<int:id>/',  perfil, name="perfil_aluno"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_aluno"),
    path('cadastrar/', cadastrar, name="cadastrar_alunos"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_aluno"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_aluno"),
    
    
    # Relatórios
    path('relatorio/alunos/ano', relatorio_alunos_por_ano, name="relatorio_alunos_por_ano"),
    path('relatorio/alunos/pdf/<int:ano_id>/', relatorio_alunos_pdf, name="relatorio_alunos_pdf"),
]



