from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.escola import Escola
from ....models.academico.classe import Classe
from ....models.academico.curso import Curso
from school.models.academico.diretor_geral import Diretor
from school.models.academico.diretor_pedagogico import Pedagogico
from school.models.academico.diretor_administrativo import DiretorAdministrativo
from school.models.localizacao.provincia import Provincia
from school.models.localizacao.municipio import Municipio
from school.models.localizacao.bairro import Bairro
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User, Group
    
from school.models.academico.turma import Turma      
from school.models.academico.aluno import Aluno      
from school.models.academico.professor import Professor      
from school.models.academico.coordenador import Coordenador      
from school.models.academico.disciplina import Disciplina      
from school.models.academico.departamento import Departamento      
from school.models.academico.diretor_geral import Diretor      
from datetime import datetime
from ....utils.utils_email import enviar_dados_acesso_escola


##Perfil de da escola admin


@login_required
def dashboard_admin(request:HttpRequest):
    
    #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
   

    cursos = Curso.objects.filter(escola=escola)
    turmas = Turma.objects.filter(curso__escola=escola)
    alunos = Aluno.objects.filter(turma__curso__escola=escola)
    professores = Professor.objects.filter(departamento__curso__escola=escola)
    coordenadores = Coordenador.objects.filter(curso__escola=escola)
    disciplinas = Disciplina.objects.filter(curso__escola=escola)
    departamentos = Departamento.objects.filter(curso__escola=escola)

    alunos_por_turma = [
        {"turma": turma.nome, "total": alunos.filter(turma=turma).count()}
        for turma in turmas
    ]

    dados = {
        "total_professores": professores.count(),
        "total_alunos": alunos.count(),
        "total_coordenadores": coordenadores.count(),
        "total_disciplinas": disciplinas.count(),
        "total_turmas": turmas.count(),
        "total_departamentos": departamentos.count(),
        "total_cursos": cursos.count(),
        "alunos_por_turma": alunos_por_turma,
    }

    return render(request, 'apps/instituicao/escola/perfil/home.html', dados)




# Listar 
@login_required
def index(request: HttpRequest):
  
  # Carregar todos os dados para os selects
  escolas = Escola.objects.prefetch_related('classes').all()
  direitores = Diretor.objects.all()
  pedagogicos = Pedagogico.objects.all()
  administrativos = DiretorAdministrativo.objects.all()
  provincias = Provincia.objects.all()
  municipios = Municipio.objects.all()
  bairros = Bairro.objects.all()
  
  
  dados = {
    
        'escolas':escolas,
        'direitores':direitores,
        'pedagogicos':pedagogicos,      
        'administrativos':administrativos,      
        'provincias':provincias,      
        'municipios':municipios,      
        ' bairros': bairros,      
            
  }
  
  return render(request , 'apps/instituicao/escola/index.html',dados)
  

  
# Visualizar escola 
@login_required
def visualizar(request:HttpRequest,id:int):
    
    #
    escola  = get_object_or_404(Escola, id=id)

    dados = {
        'escola': escola,
    
    }
    return render(request, 'apps/instituicao/escola/visualizar.html', dados)
  



def atualizar_classes_por_tipo(escola):
    tipo = escola.tipo_escola
    escola.classes.clear()  # Limpa todas as classes associadas antes de atualizar

    if tipo == 'EP':  # Ensino Primário
        classes_primario = Classe.objects.filter(ensino_primario__in=[str(i) for i in range(0, 7)])
        escola.classes.add(*classes_primario)

    elif tipo == 'PC':  # Primeiro e Segundo Ciclo
        classes_pc = Classe.objects.filter(primeiro_ciclo__in=[str(i) for i in range(7, 10)])
        escola.classes.add(*classes_pc)

    elif tipo == 'SC':  # Segundo Ciclo
        classes_sc = Classe.objects.filter(segundo_ciclo__in=[str(i) for i in range(10, 14)])
        escola.classes.add(*classes_sc)




# Cadastrar
def cadastrar(request:HttpRequest):
   
    
  # Carregar todos os dados para os selects
  
   direitores = Diretor.objects.all()
   pedagogicos = Pedagogico.objects.all()
   administrativos = DiretorAdministrativo.objects.all()
   provincias = Provincia.objects.all()
   municipios = Municipio.objects.all()
   bairros = Bairro.objects.all()
    
   if request.method == 'POST':
   
        nome = request.POST.get('nome')
        nif = request.POST.get('nif')
        provincia_id = request.POST.get('provincia')
        municipio_id = request.POST.get('municipio')
        bairro_id = request.POST.get('bairro')
        direitor_id = request.POST.get('direitor')
        direitor_pedagogico_id = request.POST.get('direitor_pedagogico')
        direitor_administrativo_id = request.POST.get('direitor_administrativo')
        logo = request.FILES.get('logo')
        alvara = request.FILES.get('alvara')
        ano_fundacao_raw = request.POST.get("ano_fundacao", "").strip()
        tipo_escola = request.POST.get('tipo_escola')
       
       
       #
            
        print(f"[DEBUG] Tipo de escola selecionada: {tipo_escola}")

   
        
        dados = {
          
          'direitores':direitores,
          'pedagogicos':pedagogicos,
          'administrativos':administrativos,
          'provincias':provincias,
          'municipios':municipios,
          'bairros':bairros,
        }
        
        
        
          # Validações
        if not all([nome, nif, provincia_id, municipio_id, bairro_id, direitor_id, direitor_pedagogico_id,       direitor_administrativo_id, tipo_escola, ano_fundacao_raw]):
            messages.error(request, "Todos os campos obrigatórios devem ser preenchidos.")
            return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
          
    
        print(f"[DEBUG] Valor recebido para ano_fundacao: '{ano_fundacao_raw}'")


        # Validar ano de fundação
        try:
            # Convertendo para data e pegando apenas o ano
            data_fundacao = datetime.strptime(ano_fundacao_raw, "%Y-%m-%d")
            ano_fundacao_int = data_fundacao.year

            ano_atual = datetime.now().year
            if ano_fundacao_int < 1900 or ano_fundacao_int > ano_atual:
                messages.error(request, f"O ano de fundação deve estar entre 1900 e {ano_atual}.")
                return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
        except (ValueError, TypeError):
            messages.error(request, "Ano de fundação inválido. Insira uma data válida.")
            return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
                
          
        if Escola.objects.filter(direitor=direitor_id):
            messages.error(request, "O direitor já existe.")
            return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
       
        if Escola.objects.filter(direitor_pedagogico=direitor_pedagogico_id):
            messages.error(request, "O direitor pedagógico já existe.")
            return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
       
        if Escola.objects.filter(direitor_administrativo=direitor_administrativo_id):
            messages.error(request, "O direitor administrativo já existe.")
            return render(request, 'apps/instituicao/escola/cadastrar.html', dados)
          
      
       
        direitor = get_object_or_404(Diretor, pk=direitor_id)
        pedagogico = get_object_or_404(Pedagogico, pk=direitor_pedagogico_id)
        administrativo = get_object_or_404(DiretorAdministrativo, pk=direitor_administrativo_id)
        provincia = get_object_or_404(Provincia, pk=provincia_id)
        municipio = get_object_or_404(Municipio, pk=municipio_id)
        bairro = get_object_or_404(Bairro, pk=bairro_id)
      
    
      
        
      
        ###################################################################################
        #                                    CADASTRAR
        ###################################################################################
        # Criar a escola sem as classes
        escola = Escola(
            nome=nome,
            nif=nif,
            direitor=direitor,
            direitor_pedagogico=pedagogico,
            direitor_administrativo=administrativo,
            provincia=provincia,
            municipio=municipio,
            bairro=bairro,
            logo=logo,
            alvara=alvara,
            ano_fundacao=ano_fundacao_raw,
            tipo_escola=tipo_escola,
       
        )
        
        
        #
        escola.save()
        
  
        escola.refresh_from_db()
        print(f"[DEBUG] Classes associadas: {[c.nome for c in escola.classes.all()]}")



        # Definir e associar as classes conforme o tipo da escola
        #
        atualizar_classes_por_tipo(escola)



         ####
      

        messages.success(request, f'Escola {nome} cadastrada com sucesso!')
        return redirect('school:listar_escolas')
      
      
   dados = {
          
          'direitores':direitores,
          'pedagogicos':pedagogicos,
          'administrativos':administrativos,
          'provincias':provincias,
          'municipios':municipios,
          'bairros':bairros,
        }

   return render(request, 'apps/instituicao/escola/cadastrar.html', dados)







# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    
    #
    escola = get_object_or_404(Escola, pk=id)
    
    # Carregar todos os dados para os selects
    direitores = Diretor.objects.all()
    pedagogicos = Pedagogico.objects.all()
    administrativos = DiretorAdministrativo.objects.all()
    provincias = Provincia.objects.all()
    municipios = Municipio.objects.all()
    bairros = Bairro.objects.all()
   

    if request.method == 'POST':
      
        nome = request.POST.get('nome')
        nif = request.POST.get('nif')
        email = request.POST.get('email')
        provincia_id = request.POST.get('provincia')
        municipio_id = request.POST.get('municipio')
        bairro_id = request.POST.get('bairro')
        direitor_id = request.POST.get('direitor')
        direitor_pedagogico_id = request.POST.get('direitor_pedagogico')
        direitor_administrativo_id = request.POST.get('direitor_administrativo')
        logo = request.FILES.get('logo') or escola.logo
        alvara = request.FILES.get('alvara')
        ano_fundacao = request.POST.get('ano_fundacao')
        tipo_escola = request.POST.get('tipo_escola')
        
       


        dados = {
          
          'direitores':direitores,
          'escola':escola,
          'pedagogicos':pedagogicos,
          'administrativos':administrativos,
          'provincias':provincias,
          'municipios':municipios,
          'bairros':bairros,
        }

     
        
          
        direitor = get_object_or_404(Diretor, pk=direitor_id)
        pedagogico = get_object_or_404(Pedagogico, pk=direitor_pedagogico_id)
        administrativo = get_object_or_404(DiretorAdministrativo, pk=direitor_administrativo_id)
        provincia = get_object_or_404(Provincia, pk=provincia_id)
        municipio = get_object_or_404(Municipio, pk=municipio_id)
        bairro = get_object_or_404(Bairro, pk=bairro_id)
        
        
        
        # Validações
            
        # O direitor geral, pedagógico e administrativo dem pertencer em apenas uma única escola
        if direitor:
            ja_existe = Escola.objects.filter(direitor=direitor).exclude(pk=escola.pk).exists()
            if ja_existe:
                messages.error(request, f'{direitor} já é direitor geral de uma outra escola.')
                return render(request, 'apps/instituicao/escola/atualizar.html', dados)
            
        if pedagogico:
            ja_existe = Escola.objects.filter(direitor_pedagogico=pedagogico).exclude(pk=escola.pk).exists()
            if ja_existe:
                messages.error(request, f'{pedagogico} já é direitor pedagógico de uma outra escola.')
                return render(request, 'apps/instituicao/escola/atualizar.html', dados)
            
        if administrativo:
            ja_existe = Escola.objects.filter(direitor_administrativo=administrativo).exclude(pk=escola.pk).exists()
            if ja_existe:
                messages.error(request, f'{administrativo} já é direitor administrativo de uma outra escola.')
                return render(request, 'apps/instituicao/escola/atualizar.html', dados)
    
      
       
        escola.nome=nome
        escola.nif= nif
        escola.email= email
        escola.direitor=direitor
        escola.direitor_pedagogico=pedagogico
        escola.direitor_administrativo=administrativo
        escola.provincia=provincia
        escola.municipio=municipio
        escola.bairro=bairro
        
        escola.alvara=alvara
        escola.ano_fundacao=ano_fundacao
        escola.tipo_escola=tipo_escola
        
        if logo:
          escola.logo=logo
          
          
        
      
        
        escola.save(force_update=True)
  
        #
        atualizar_classes_por_tipo(escola)

        messages.success(request, f'Escola {nome} atualizada com sucesso!')
        return redirect('school:listar_escolas')

    # Requisição GET
    dados = {
          
          'direitores':direitores,
          'escola':escola,
          'pedagogicos':pedagogicos,
          'administrativos':administrativos,
          'provincias':provincias,
          'municipios':municipios,
          'bairros':bairros,
        }

    return render(request, 'apps/instituicao/escola/atualizar.html', dados)
 

 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    escola = get_object_or_404(Escola, id=id)
    direitor = escola.direitor
   
    
    if request.method == 'POST':
      
        escola.delete()
        return redirect('school:listar_escolas')  
    
    dados ={
        'escola': escola, 
        'direitor': direitor, 
      
        }
      
    return render(request, 'apps/instituicao/escola/eliminar.html', dados )
   
   
   
   
   
   
   
   
   
#Visualizar diretores

def diretor_detalhe(request:HttpRequest):
    
     #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    
    direitor = escola.direitor #direitor da escola logada
    
    return render(request, 'apps/instituicao/escola/perfil/diretor_detalhe.html', {'direitor': direitor})
   
   
   
#Visualizar pedagógicos
def pedagogico_detalhe(request:HttpRequest):
    
     #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    pedagogico = escola.direitor_pedagogico #pedagogico da escola logada
    
    return render(request, 'apps/instituicao/escola/perfil/pedagogico_detalhe.html', {'pedagogico': pedagogico})
   
#Visualizar administrativo
def administrativo_detalhe(request:HttpRequest):
    
     #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    administrativo = escola.direitor_administrativo #Administrativo da escola logada
    
    return render(request, 'apps/instituicao/administrativo/layout/perfil.html', {'administrativo': administrativo})
   
   
   
   #Cursos
   
   
   
   
def listar_cursos(request:HttpRequest):
    
     
     #Admin logado
    diretor = Diretor.objects.get(user=request.user)

    escola = Escola.objects.filter(direitor=diretor).first()
    
           # Carregar apenas os cursos da escola logada
    cursos = Curso.objects.filter(escola=escola)
       
    return render(request, 'apps/instituicao/escola/perfil/cursos_listar.html', {'cursos': cursos})
      
      
      