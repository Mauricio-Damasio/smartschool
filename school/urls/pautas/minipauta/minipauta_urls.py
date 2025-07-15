from django.urls import path
from ....views.instituicao.pautas.pauta import salvar_mini_pauta,mini_pauta_pdf, mini_pauta_preencher


urlpatterns = [
    path('preencher/', mini_pauta_preencher, name='mini_pauta_preencher'),
    path('mini_pauta_salvar/', salvar_mini_pauta, name='mini_pauta_salvar'),
    
     path('mini_pauta/pdf/', mini_pauta_pdf, name='gerar_mini_pauta_pdf'),

]
