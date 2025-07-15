from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from school.models.academico.professor import Professor
from school.models.academico.disciplina import Disciplina
from school.models.academico.turma import Turma
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .....models.academico.disciplinaLecionada import DisciplinaLecionada
from .....models.academico.diretor_pedagogico import Pedagogico
from .....models.academico.escola import Escola


from collections import defaultdict


@login_required
def listar_atribuicao(request: HttpRequest):
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    # Filtra as atribuições da escola do pedagógico logado
    atribuicoes = DisciplinaLecionada.objects.filter(
        turma__curso__escola=escola
    ).select_related('professor', 'disciplina', 'turma', 'turma__classe', 'turma__curso')

    # Agrupa por professor
    agrupado = defaultdict(list)
    for item in atribuicoes:
        agrupado[item.professor].append(item)

    dados = {
        'professores_atribuicoes': agrupado.items()
    }

    return render(request, 'apps/instituicao/pedagogico/disciplina_turma/listar_atribuicao.html', dados)



@login_required
def visualizar_professor(request: HttpRequest, id: int):
    professor = get_object_or_404(Professor, pk=id)

    # Verifica se o professor pertence à escola do pedagógico logado
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    if not professor.departamento.curso.escola == escola:
        messages.error(request, "Você não tem permissão para visualizar este professor.")
        return redirect('school:listar_atribuicao')

    atribuicoes = DisciplinaLecionada.objects.filter(
        professor=professor,
        turma__curso__escola=escola
    ).select_related('disciplina', 'turma', 'turma__classe', 'turma__curso')

    return render(request, 'apps/instituicao/pedagogico/disciplina_turma/visualizar.html', {
        'professor': professor,
        'atribuicoes': atribuicoes
    })



#
@login_required
def atribuir_turma_disciplina(request: HttpRequest):

    #Pedagogico logado
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    professores = Professor.objects.filter(departamento__curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)
    turmas = Turma.objects.filter(curso__escola=escola)

    dados = {
        'professores': professores,
        'disciplinas': disciplinas,
        'turmas': turmas,
    }

    if request.method == 'POST':
        professor_id = request.POST.get('professor')
        disciplina_id = request.POST.get('disciplina')
        turma_id = request.POST.get('turma')

        if not all([professor_id, disciplina_id, turma_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/pedagogico/disciplina_turma/disciplina_lecionada.html', dados)

        professor = Professor.objects.get(pk=professor_id)
        disciplina = Disciplina.objects.get(pk=disciplina_id)
        turma = Turma.objects.get(pk=turma_id)

        classe = turma.classe
        curso = turma.curso

        # Verifica se a disciplina já foi atribuída para essa turma, classe e curso
        existe = DisciplinaLecionada.objects.filter(
            turma__classe=classe,
            turma__curso=curso,
            disciplina=disciplina
        ).exists()

        if existe:
            messages.error(request, f"A disciplina '{disciplina.nome}' já foi atribuída a outro professor para esta turma-classe-curso.")
            return render(request, 'apps/instituicao/pedagogico/disciplina_turma/disciplina_lecionada.html', dados)

        # Se passou pela validação, criar a atribuição
        DisciplinaLecionada.objects.create(
            professor=professor,
            disciplina=disciplina,
            turma=turma,
        )

        messages.success(request, "Atribuição feita com sucesso!")
        return redirect('school:listar_atribuicao')

    return render(request, 'apps/instituicao/pedagogico/disciplina_turma/disciplina_lecionada.html', dados)



@login_required
def atualizar_atribuicao(request: HttpRequest, id: int):
    disciplinaLecionada = get_object_or_404(DisciplinaLecionada, pk=id)

    # Pedagógico logado
    pedagogico = Pedagogico.objects.get(user=request.user)
    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()

    professores = Professor.objects.filter(departamento__curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)
    turmas = Turma.objects.filter(curso__escola=escola)

    dados = {
        'professores': professores,
        'disciplinas': disciplinas,
        'turmas': turmas,
        'disciplinaLecionada': disciplinaLecionada,
    }

    if request.method == 'POST':
        professor_id = request.POST.get('professor')
        disciplina_id = request.POST.get('disciplina')
        turma_id = request.POST.get('turma')

        if not all([professor_id, disciplina_id, turma_id]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/pedagogico/disciplina_turma/atualizar.html', dados)

        professor = Professor.objects.get(pk=professor_id)
        disciplina = Disciplina.objects.get(pk=disciplina_id)
        turma = Turma.objects.get(pk=turma_id)

        classe = turma.classe
        curso = turma.curso

        # Verifica se essa disciplina já está atribuída na mesma turma, classe e curso por OUTRO professor
        existe = DisciplinaLecionada.objects.filter(
            turma__classe=classe,
            turma__curso=curso,
            turma=turma,
            disciplina=disciplina
        ).exclude(id=disciplinaLecionada.id).exists()

        if existe:
            messages.error(request, f"A disciplina '{disciplina.nome}' já foi atribuída a outro professor para esta turma-classe-curso.")
            return render(request, 'apps/instituicao/pedagogico/disciplina_turma/atualizar.html', dados)

        # Atualizar os dados
        disciplinaLecionada.professor = professor
        disciplinaLecionada.disciplina = disciplina
        disciplinaLecionada.turma = turma

        disciplinaLecionada.save(force_update=True)

        messages.success(request, "Atualização feita com sucesso!")
        return redirect('school:visualizar_professor_atribuicao', id=professor.id)

    return render(request, 'apps/instituicao/pedagogico/disciplina_turma/atualizar.html', dados)





#
 
 
#Eliminar
@login_required
def eliminar_atribuicao(request:HttpRequest, id:int):

 
    disciplinaLecionada = get_object_or_404(DisciplinaLecionada, id=id)
    departamento = disciplinaLecionada.professor.departamento
    
    if request.method == 'POST':
      
        disciplinaLecionada.delete()
        return redirect('school:listar_atribuicao')  
      
    return render(request, 'apps/instituicao/pedagogico/disciplina_turma/eliminar.html', {'disciplinaLecionada':disciplinaLecionada, 'departamento':departamento})