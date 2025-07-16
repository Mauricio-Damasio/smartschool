from django.urls import path
from  ....views.instituicao.pedagogico.pedagogico import index, visualizar,cadastrar,atualizar,eliminar, dashboard_pedagogico,perfil
from ....views.instituicao.pedagogico.trimestre_liberado import trimestres_liberar
from school.views.instituicao.pedagogico.desempenho import desempenho, desempenho_pdf
from school.views.instituicao.pedagogico.aprovar_pedidos import aprovar_pedidos
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
]

