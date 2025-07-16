from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ....models.academico.aluno import Aluno
from ....models.academico.professor import Professor
from ....models.relatorio.minipauta import MiniPauta
from ....models.academico.curso import Curso
from ....models.academico.disciplina import Disciplina
from ....models.academico.escola import Escola
from ....models.academico.diretor_geral import Diretor
from ....models.academico.classe import Classe
from django.db.models import Count, Q
from collections import Counter
from school.models.academico.disciplinaLecionada import DisciplinaLecionada


#


@login_required
def relatorio_estatisticas_gerais(request):
    diretor = Diretor.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor=diretor).first()
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

    trimestres = dict(MiniPauta.TRIMESTRES)

    curso_id = request.GET.get('curso')
    classe_id = request.GET.get('classe')
    trimestre_id = request.GET.get('trimestre')

    alunos = Aluno.objects.select_related('turma__curso', 'turma__classe')

    if curso_id:
        alunos = alunos.filter(turma__curso_id=curso_id)
    if classe_id:
        alunos = alunos.filter(turma__classe_id=classe_id)

    total_por_curso = alunos.values('turma__curso__nome').annotate(total=Count('id'))
    genero_count = Counter(aluno.genero for aluno in alunos)

    total_professores = Professor.objects.count()

    # CORRIGIDO: buscar todas as disciplinas da escola
    disciplinas = Disciplina.objects.filter(curso__escola=escola)

    # Buscar professores por disciplina
    disciplinas_lecionadas = DisciplinaLecionada.objects.filter(
        disciplina__in=disciplinas
    ).select_related('disciplina', 'professor')

    # Agrupar por disciplina
    profs_disc = disciplinas_lecionadas.values('disciplina__nome').annotate(total=Count('professor'))

    # Calcular taxa de aprovação por trimestre
    aprovacao = []
    for trimestre_key, trimestre_valor in trimestres.items():
        pautas = MiniPauta.objects.filter(trimestre=trimestre_key)

        if curso_id:
            pautas = pautas.filter(turma__curso_id=curso_id)
        if classe_id:
            pautas = pautas.filter(turma__classe_id=classe_id)

        total_pautas = pautas.count()
        aprovados = pautas.filter(mf__gte=10).count()  # Ajuste se o campo de média final for diferente

        percentual = round((aprovados / total_pautas) * 100, 2) if total_pautas > 0 else 0

        aprovacao.append({
            'trimestre': trimestre_valor,
            'percentual': percentual,
        })

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
