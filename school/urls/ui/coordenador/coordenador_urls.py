from django.urls import path
from  ....views.ui.coordenador.coordenador import index,visualizar,cadastrar,atualizar, eliminar,dashboard_coordenador
from ....views.ui.coordenador.funcoes import alunos_do_curso_coordenado,gerar_pdf_alunos_filtrados, gerar_pdf_professores,professores_do_curso_coordenado

from ....views.ui.coordenador.relatorio import rendimento_professores,gerar_pdf_rendimento_professores
from ....views.ui.coordenador.horario import gerenciar_horarios, gerar_pdf_horario_turma

urlpatterns = [
    
    #
    path('dashboard_coordenador/', dashboard_coordenador, name="dashboard_coordenador"),
    path('listar/coordenadores/', index, name="listar_coordenadores"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_coordenador"),
    path('cadastrar/', cadastrar, name="cadastrar_coordenador"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_coordenador"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_coordenador"),
    
    
    #
    #
    ##FUNCOES
    
    #Professores
    
    path('coordenador/professores/', professores_do_curso_coordenado, name='professores_do_curso'),
    path('coordenador/professores/pdf/', gerar_pdf_professores, name='gerar_pdf_professores'),
        
    
    
    #Alunos
    path('alunos/curso/coordenado/',alunos_do_curso_coordenado, name="alunos_do_curso_coordenador"),
    path('alunos/gerar_pdf_alunos_filtrados/',gerar_pdf_alunos_filtrados, name="gerar_pdf_alunos_filtrados"),
    
    
    #
    #Relatório
    #
    path('alunos/rendimento_professores/',rendimento_professores, name="rendimento_professores"),
    path('alunos/gerar_pdf_rendimento_professores/',gerar_pdf_rendimento_professores, name="gerar_pdf_rendimento_professores"),
    
    
    path('coordenador/horarios/', gerenciar_horarios, name='gerenciar_horarios'),
    path('coordenador/horarios/pdf/', gerar_pdf_horario_turma, name='gerar_pdf_horario_turma'),


]

