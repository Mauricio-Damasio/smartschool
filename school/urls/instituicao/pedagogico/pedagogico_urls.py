from django.urls import path
from  ....views.instituicao.pedagogico.pedagogico import index, visualizar,cadastrar,atualizar,eliminar, dashboard_pedagogico,perfil
from ....views.instituicao.pedagogico.trimestre_liberado import trimestres_liberar
from school.views.instituicao.pedagogico.desempenho import desempenho, desempenho_pdf
from school.views.instituicao.pedagogico.aprovar_pedidos import aprovar_pedidos
from school.views.instituicao.pedagogico.disciplina_turma.disciplina_lecionada import atribuir_turma_disciplina,listar_atribuicao,atualizar_atribuicao,visualizar_professor,eliminar_atribuicao



#
urlpatterns = [
    path('dashboard_pedagogico/', dashboard_pedagogico ,name="dashboard_pedagogico"),
    path('perfil/', perfil ,name="perfil"),
    

    #
    path('listar/pedagogico/', index, name="listar_pedagogicos"),
    
    #
    path('visualizar/<int:id>/',  visualizar, name="visualizar_pedagogico"),
    path('cadastrar/', cadastrar, name="cadastrar_pedagogico"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_pedagogico"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_pedagogico"),
    
    #
    path('trimestres_liberar/', trimestres_liberar, name="trimestres_liberar"),
    path('relatorios/desempenho/', desempenho, name="desempenho"),
    path('relatorios/desempenho_pdf/', desempenho_pdf, name="desempenho_pdf"),
    path('documentos/aprovar/', aprovar_pedidos, name="aprovar_pedidos"),
    
    # Atribuir disciplina-turma
    path('eliminar_atribuicao/<int:id>/',eliminar_atribuicao, name="eliminar_atribuicao"),
    path('atualizar_atribuicao/<int:id>/', atualizar_atribuicao, name="atualizar_atribuicao"),
    path('visualizar-professor/<int:id>/', visualizar_professor, name="visualizar_professor_atribuicao"),
    path('listar/atribuicao/', listar_atribuicao, name="listar_atribuicao"),
    path('atribuir/turma_disciplina/', atribuir_turma_disciplina, name="atribuir_turma_disciplina"),
    
]

