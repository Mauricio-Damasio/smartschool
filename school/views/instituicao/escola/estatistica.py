from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ....models.academico.aluno import Aluno
from ....models.academico.professor import Professor
from ....models.relatorio.minipauta import MiniPauta
from ....models.academico.curso import Curso
from ....models.academico.classe import Classe
from collections import Counter
from django.db.models import Count

@login_required
def relatorio_estatisticas_gerais(request):
    
    escola = request.user.escola
    
    cursos = Curso.objects.filter(escola=escola)
   
    
    # Filtrar classes conforme o tipo da escola
    if escola.tipo_escola == 'EP':
            classes = Classe.objects.filter(ensino_primario__isnull=False) 
    elif escola.tipo_escola == 'PC':
            classes = Classe.objects.filter(primeiro_ciclo__isnull=False)
    elif escola.tipo_escola == 'SC':
            classes = Classe.objects.filter(segundo_ciclo__isnull=False)
    else:
            classes = Classe.objects.none()

    # Choices do campo trimestre 
    trimestres = dict(MiniPauta.TRIMESTRES)

    curso_id = request.GET.get('curso')
    classe_id = request.GET.get('classe')
    trimestre_id = request.GET.get('trimestre')

    alunos = Aluno.objects.select_related('turma__curso', 'turma__classe')

    # Filtros com base na relação com turma
    if curso_id:
        alunos = alunos.filter(turma__curso_id=curso_id)
    if classe_id:
        alunos = alunos.filter(turma__classe_id=classe_id)

    # Total por curso
    total_por_curso = alunos.values('turma__curso__nome').annotate(total=Count('id'))

    # Distribuição por gênero
    genero_count = Counter(aluno.genero for aluno in alunos)



    # Total de professores
    total_professores = Professor.objects.count()

    # Professores por disciplina
    profs_disc = Professor.objects.values('disciplina__nome').annotate(total=Count('id'))

    # Aprovação geral por trimestre
    aprovacao = []
    for trimestre_key, trimestre_valor in trimestres.items():
        pautas = MiniPauta.objects.filter(trimestre=trimestre_key)

        # Filtro por curso e classe
        if curso_id:
            pautas = pautas.filter(turma__curso_id=curso_id)
        if classe_id:
            pautas = pautas.filter(turma__classe_id=classe_id)

     
       

    return render(request, 'apps/instituicao/escola/estatisticas/estatisticas_gerais.html', {
        'cursos': cursos,
        'classes': classes,
        'trimestres': trimestres,
        'total_curso_labels': [item['turma__curso__nome'] for item in total_por_curso],
        'total_curso_data': [item['total'] for item in total_por_curso],
        'genero_labels': list(genero_count.keys()),
        'genero_data': list(genero_count.values()),
      
        'total_professores': total_professores,
        'profs_disc_labels': [item['disciplina__nome'] for item in profs_disc],
        'profs_disc_data': [item['total'] for item in profs_disc],
        'aprovacao_labels': [item['trimestre'] for item in aprovacao],
        'aprovacao_data': [item['percentual'] for item in aprovacao],
    })