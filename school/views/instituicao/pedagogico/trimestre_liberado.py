from django.shortcuts import render, redirect
from ....models.academico.turma import Turma
from ....models.academico.disciplina import Disciplina
from ....models.relatorio.trimestre_liberado import TrimestreLiberado 
from ....models.academico.escola import Escola 
from ....models.academico.diretor_pedagogico import Pedagogico
from django.contrib import messages





def trimestres_liberar(request):
    
    #
    pedagogico = Pedagogico.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor_pedagogico=pedagogico).first()
    if not escola:
        messages.error(request, "Nenhuma escola vinculada ao seu perfil pedagógico.")
        return redirect('school:dashboard_pedagogico')
    
    turmas = Turma.objects.filter(curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)

    if request.method == 'POST':
        for turma in turmas:
            disciplinas_da_turma = disciplinas.filter(curso=turma.curso)  
            for disciplina in disciplinas_da_turma:
                for trimestre in [1, 2, 3]:
                    checkbox_name = f"{turma.id}_{disciplina.id}_{trimestre}"
                    liberado = checkbox_name in request.POST

                    TrimestreLiberado.objects.update_or_create(
                        turma=turma,
                        disciplina=disciplina,
                        trimestre=trimestre,
                        defaults={'liberado': liberado}
                    )

        print(request.POST)
        
        messages.success(request, "Desbloqueios atualizados com sucesso.")
        return redirect('school:trimestres_liberar') 

    # Carrega todos os registros existentes
    desbloqueios = TrimestreLiberado.objects.all()

    # Cria o dicionário com o status atual
    status = {
        f"{d.turma_id}_{d.disciplina_id}_{d.trimestre}": d.liberado
        for d in desbloqueios
    }

    context = {
        'turmas': turmas,
        'disciplinas': disciplinas,
        'status': status
    }

    return render(request, 'apps/instituicao/pedagogico/trimestres_liberar.html', context)
