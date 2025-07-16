from django.urls import path
from  ....views.instituicao.administrativo.administrativo import dashboard_administrativo, index, visualizar,cadastrar,atualizar,eliminar
from school.views.instituicao.administrativo.assiduidade import  assiduidade_relatorio,cadastrar_assiduidade
from school.views.instituicao.administrativo.recursos_humanos import avaliar_desempenho, registrar_ponto,gerar_pdf_ponto,listar_desempenhos,gerar_pdf_desempenho,eliminar_desempenho

from school.views.instituicao.administrativo.relatorios_financeiros import alunos_por_curso_pdf,pagamentos_em_atraso_pdf, pagamentos_pdf,filtro_pagamento_pdf_view, filtro_pagamento_atraso_pdf,cadastrar_pagamento




#
urlpatterns = [
    path('dashboard_administrativo/', dashboard_administrativo, name="dashboard_administrativo"),
    
    #
    path('listar/administrativos', index, name="listar_administrativos"),
    path('visualizar/<int:id>/',  visualizar, name="visualizar_administrativo"),
    path('cadastrar/', cadastrar, name="cadastrar_administrativo"),
    path('atualizar/<int:id>/', atualizar, name="atualizar_administrativo"),
    path('eliminar/<int:id>/', eliminar, name="eliminar_administrativo"),
    
  
    
    #Assiduidade    
     path('recusos/humanos/assiduidade/', assiduidade_relatorio, name="assiduidade_relatorio"),
     path('recusos/humanos/cadastrar_assiduidade/',cadastrar_assiduidade, name="cadastrar_assiduidade"),
    
    #Recursos humanos
     path('recusos/listar_desempenhos/',listar_desempenhos, name="listar_desempenhos"),
     path('recusos/avaliar_desempenho/', avaliar_desempenho, name="avaliar_desempenho"),
     path('recusos/gerar/pdf/desempenho/<int:pk>/', gerar_pdf_desempenho, name="gerar_pdf_desempenho"),
     path('recusos/registrar_ponto/',registrar_ponto, name="registrar_ponto"),
     path('recusos/gerar_pdf_ponto/<int:ponto_id>',gerar_pdf_ponto, name="gerar_pdf_ponto"),
     path('recusos/eliminar_desempenho/<int:id>',eliminar_desempenho, name="eliminar_desempenho"),
     
     
     # Relatorios
     path('financas/alunos_por_curso_pdf/', alunos_por_curso_pdf, name="alunos_por_curso_pdf"),
     
     
     #
     path('financas/cadastrar/pagamento/',cadastrar_pagamento, name="cadastrar_pagamento"),
     path('financas/pagamentos_em_atraso_pdf/',pagamentos_em_atraso_pdf, name="pagamentos_em_atraso_pdf"),
     path('financas/filtro_pagamento/', filtro_pagamento_pdf_view, name="filtro_pagamento_pdf_view"),
     path('financas/pagamentos_pdf/', pagamentos_pdf, name="pagamentos_pdf"),
     path('financas/filtro_pagamento_atraso_pdf/',  filtro_pagamento_atraso_pdf, name="filtro_pagamento_atraso_pdf"),
     
]

