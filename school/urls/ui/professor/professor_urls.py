from django.urls import path
from  ....views.ui.professor.professor import index,visualizar,cadastrar,atualizar,eliminar,dashboard_professor,perfil
from  ....views.ui.professor.aulas import  aulas_do_professor,elaborar_aula,exportar_aula_pdf,visualizar_alunos_professor,exportar_alunos_pdf
from ....views.ui.professor.frequencia import registrar_frequencia,relatorio_frequencia


#
urlpatterns = [
    path('dashboard_professor/', dashboard_professor, name="dashboard_professor"),
    path('listar/', index, name="listar_professores"),
    path('visualizar/<int:id>/', visualizar, name="visualizar_professor"),
    path('perfil/<int:id>/', perfil, name="perfil_professor"),
    path('cadastrar/', cadastrar, name="cadastrar_professor"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_professor"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_professor"),
    
    
    
    
    #Aulas
    
    path('aulas/', aulas_do_professor, name='aulas_do_professor'),
    path('aula/elaborar/<int:disciplina_id>/<int:turma_id>/', elaborar_aula, name='elaborar_aula'),
    path('aula/pdf/<int:aula_id>/', exportar_aula_pdf, name='exportar_aula_pdf'),
    
    #Alunos visualizar
     path('professor/alunos/exportar-pdf/<int:turma_id>/', exportar_alunos_pdf, name='exportar_alunos_pdf'),
     path('professor/alunos/visualizar_alunos_professor/', visualizar_alunos_professor, name='visualizar_alunos_professor'),
     
     
     #Frequência
     path('professor/registrar/frequencia/', registrar_frequencia, name='registrar_frequencia'),
     path('professor/relatorio/frequencia/', relatorio_frequencia, name='relatorio_frequencia'),

]

