from django.urls import path
from  ....views.ui.aluno.aluno import index, visualizar,cadastrar,atualizar,eliminar,dashboard_aluno,perfil
from ....views.ui.aluno.relatorio import relatorio_alunos_por_ano, relatorio_alunos_pdf
from ....views.ui.aluno.notas import minhas_notas,gerar_pdf_notas_aluno
from ....views.ui.aluno.visualizar_horario import horario_turma_aluno,horario_pdf_aluno
from ....views.ui.aluno.frequencia import frequencia_pdf_aluno,frequencia_aluno

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
    
    
    #Notas
    path('aluno/minhas-notas/', minhas_notas, name='minhas_notas'),
    path('aluno/minhas-notas/pdf/', gerar_pdf_notas_aluno, name='gerar_pdf_notas_aluno'),
    
    
    #Horário
    path('aluno/horario/', horario_turma_aluno, name='horario_turma_aluno'),
    path('aluno/horario/pdf/', horario_pdf_aluno, name='horario_pdf_aluno'),
    
    #Frequencia
    path('aluno/frequencia/', frequencia_aluno, name='frequencia_aluno'),
    path('aluno/frequencia/pdf/', frequencia_pdf_aluno, name='frequencia_pdf_aluno'),

]



