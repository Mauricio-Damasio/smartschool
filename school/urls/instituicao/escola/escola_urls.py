from django.urls import path
from  ....views.instituicao.escola.escola import index, visualizar,cadastrar,atualizar,eliminar,dashboard_admin,diretor_detalhe,pedagogico_detalhe, listar_cursos,administrativo_detalhe
from ....views.instituicao.escola.estatistica import  relatorio_estatisticas_gerais
from ....views.instituicao.escola.documentos import  gerar_certificado,filtrar_aluno

urlpatterns = [
    path('', index, name="listar_escolas"),
    path('dashboard_admin/', dashboard_admin, name="dashboard_admin"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_escola"),
    path('cadastrar/', cadastrar, name="cadastrar_escola"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_escola"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_escola"),
    
    #detalhes
    path('diretor_detalhe/', diretor_detalhe, name="diretor_detalhe"),
    path('pedagogico_detalhe/', pedagogico_detalhe, name="pedagogico_detalhe"),
    path('administrativo_detalhe/', administrativo_detalhe, name="administrativo_detalhe"),
    path('listar_cursos/',  listar_cursos, name="listar_cursos_escola"),
    
    
    #Estatisticas gerais
    path('relatorio/estatisticas/gerais/',  relatorio_estatisticas_gerais, name="relatorio_estatisticas_gerais"),
    
    
    #Certificados
    path('aluno/filtrado/',  filtrar_aluno, name="filtrar_aluno"),
    path('documentos/certificados/<int:aluno_id>',  gerar_certificado, name="gerar_certificados"),
    
    
    
]

