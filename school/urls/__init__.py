from django.urls import path, include




app_name = 'school'

urlpatterns = [
    
    #Include Webpage Urls
    path('', include('school.urls.webpage.webpage_urls')),
    
    
    
    
    #Urls de autenticação
    path('autenticacao/', include('school.urls.auth.autenticacao_urls')),
    
    
    #Home page
    path('home/', include('school.urls.home.home_urls')),
    
    
  
  
   ########################################################################
   #                             ACADÉMICO
   ########################################################################
  
    # Alunos urls
    path('aluno/', include('school.urls.ui.aluno.aluno_urls')),
    
    # Professores urls
     path('professor/', include('school.urls.ui.professor.professor_urls')),
     
    # Coordenadores urls
     path('coordenador/', include('school.urls.ui.coordenador.coordenador_urls')),
    
    # Discipplinas urls
     path('disciplina/', include('school.urls.ui.disciplina.disciplina_urls')),
     
    # Turmas urls
     path('turma/', include('school.urls.ui.turma.turma_urls')),

    # Classes urls
     path('classe/', include('school.urls.ui.classe.classe_urls')),
    
      
   ########################################################################
   #                             INSTITUIÇÃO
   ########################################################################
    
    #Cursos urls
    path('escola/', include('school.urls.instituicao.escola.escola_urls')),
    
    #Cursos urls
    path('curso/', include('school.urls.instituicao.curso.curso_urls')),
    
    
    
    #Direitor urls
    path('direitor/', include('school.urls.instituicao.direitor.direitor_urls')),
    
    #Direitor pedagogico urls
    path('pedagogico/', include('school.urls.instituicao.pedagogico.pedagogico_urls')),
    
    
    #Direitor administrativo urls
    path('administrativo/', include('school.urls.instituicao.administrativo.administrativo_urls')),
    
    
    
    #Departamento urls
    path('departamento/', include('school.urls.instituicao.departamento.departamento_urls')),
    
    
    #Pauta urls

    
    
   path('pauta/', include(('school.urls.pautas.minipauta.minipauta_urls'))),


    
    #
    path('configuracao/', include('school.urls.configuracao.configuracao')),
]
