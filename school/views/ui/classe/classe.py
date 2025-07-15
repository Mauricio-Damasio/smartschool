from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpRequest
from ....models.academico.classe import Classe
from ....models.academico.escola import Escola
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Listar 
@login_required
def index(request):
    
    #
    classes_primario = Classe.objects.exclude(ensino_primario__isnull=True).exclude(ensino_primario='')
    classes_primeiro = Classe.objects.exclude(primeiro_ciclo__isnull=True).exclude(primeiro_ciclo='')
    classes_segundo = Classe.objects.exclude(segundo_ciclo__isnull=True).exclude(segundo_ciclo='')


    context = {
        'classes_primario': classes_primario,
        'classes_primeiro': classes_primeiro,
        'classes_segundo': classes_segundo,
    }
    return render(request, 'apps/ui/classe/index.html', context)
  

  
# Visualizar 
@login_required
def visualizar(request:HttpRequest,id:int):
    
    #
    classe  = get_object_or_404(Classe, id=id)
    
    return render(request, 'apps/ui/classe/visualizar.html', {'classe':classe})





#Atualizar as classes criadas na escola 
def associar_classe_a_escolas_existentes(nova_classe):
    if nova_classe.segundo_ciclo:
        escolas = Escola.objects.filter(tipo_escola='SC')
        for escola in escolas:
            escola.classes.add(nova_classe)

    elif nova_classe.primeiro_ciclo:
        escolas = Escola.objects.filter(tipo_escola='PC')
        for escola in escolas:
            escola.classes.add(nova_classe)

    elif nova_classe.ensino_primario:
        escolas = Escola.objects.filter(tipo_escola='EP')
        for escola in escolas:
            escola.classes.add(nova_classe)


# Cadastrar
@login_required
def cadastrar(request: HttpRequest):
    
    
    #
    if request.method == 'POST':
        
        
        #
        ensino_primario = request.POST.get('ensino_primario')
        primeiro_ciclo = request.POST.get('primeiro_ciclo')
        segundo_ciclo = request.POST.get('segundo_ciclo')

     
        # Verificar se já existe a classe
        if ensino_primario:
            if Classe.objects.filter(ensino_primario=ensino_primario).exists():
                messages.error(request, f"A classe {ensino_primario}ª do Ensino Primário já está cadastrada.")
                return redirect('school:listar_classes')

            nova_classe=Classe.objects.create(ensino_primario=ensino_primario)
            messages.success(request, f'Classe {ensino_primario}ª do Ensino Primário cadastrada com sucesso!')
          
            #  
            associar_classe_a_escolas_existentes(nova_classe)
        
        elif primeiro_ciclo:
            if Classe.objects.filter(primeiro_ciclo=primeiro_ciclo).exists():
                messages.error(request, f"A classe {primeiro_ciclo}ª do Primeiro Ciclo já está cadastrada.")
                return redirect('school:listar_classes')

            nova_classe=Classe.objects.create(primeiro_ciclo=primeiro_ciclo)
            messages.success(request, f'Classe {primeiro_ciclo}ª do Primeiro Ciclo cadastrada com sucesso!')
                 
            #  
            associar_classe_a_escolas_existentes(nova_classe)
        
        elif segundo_ciclo:
            if Classe.objects.filter(segundo_ciclo=segundo_ciclo).exists():
                messages.error(request, f"A classe {segundo_ciclo}ª do Segundo Ciclo já está cadastrada.")
                return redirect('school:listar_classes')

            nova_classe=Classe.objects.create(segundo_ciclo=segundo_ciclo)
            messages.success(request, f'Classe {segundo_ciclo}ª do Segundo Ciclo cadastrada com sucesso!')
            
            #  
            associar_classe_a_escolas_existentes(nova_classe)

        return redirect('school:listar_classes')

    return render(request, 'apps/ui/classe/cadastrar.html')


# Atualizar
@login_required
def atualizar(request: HttpRequest, id: int):
    classe = get_object_or_404(Classe, pk=id)

    dados = {
        'classe': classe,
        'ensino_primario': [str(i) for i in range(0, 7)],
        'primeiro_ciclo': [str(i) for i in range(7, 10)],
        'segundo_ciclo': [str(i) for i in range(10, 14)],
    }

    if request.method == 'POST':
        ensino_primario = request.POST.get('ensino_primario')
        primeiro_ciclo = request.POST.get('primeiro_ciclo')
        segundo_ciclo = request.POST.get('segundo_ciclo')

        # ENSINO PRIMÁRIO
        if ensino_primario:
            ja_existe = Classe.objects.filter(ensino_primario=ensino_primario).exclude(pk=classe.pk).exists()
            if ja_existe:
                messages.error(request, f'A classe {ensino_primario}ª já existe no Ensino Primário.')
                return render(request, 'apps/ui/classe/atualizar.html', dados)

            classe.ensino_primario = ensino_primario
            classe.primeiro_ciclo = None
            classe.segundo_ciclo = None
            classe.save(force_update=True)
            messages.success(request, 'Classe atualizada com sucesso!')
            return redirect('school:listar_classes')

        # PRIMEIRO CICLO
        elif primeiro_ciclo:
            ja_existe = Classe.objects.filter(primeiro_ciclo=primeiro_ciclo).exclude(pk=classe.pk).exists()
            if ja_existe:
                messages.error(request, f'A classe {primeiro_ciclo}ª já existe no Primeiro Ciclo.')
                return render(request, 'apps/ui/classe/atualizar.html', dados)

            classe.primeiro_ciclo = primeiro_ciclo
            classe.ensino_primario = None
            classe.segundo_ciclo = None
            classe.save(force_update=True)
            messages.success(request, 'Classe atualizada com sucesso!')
            return redirect('school:listar_classes')

        # SEGUNDO CICLO
        elif segundo_ciclo:
            ja_existe = Classe.objects.filter(segundo_ciclo=segundo_ciclo).exclude(pk=classe.pk).exists()
            if ja_existe:
                messages.error(request, f'A classe {segundo_ciclo}ª já existe no Segundo Ciclo.')
                return render(request, 'apps/ui/classe/atualizar.html', dados)

            classe.segundo_ciclo = segundo_ciclo
            classe.ensino_primario = None
            classe.primeiro_ciclo = None
            classe.save(force_update=True)
            messages.success(request, 'Classe atualizada com sucesso!')
            return redirect('school:listar_classes')

        else:
            messages.error(request, 'Você deve selecionar uma classe.')
            return render(request, 'apps/ui/classe/atualizar.html', dados)

    return render(request, 'apps/ui/classe/atualizar.html', dados)

 
 
 #Eliminar
@login_required
def eliminar(request:HttpRequest, id:int):

 
    classe = get_object_or_404(Classe, id=id)
   
    if request.method == 'POST':
      
        classe.delete()
        return redirect('school:listar_classes')  

      
    return render(request, 'apps/ui/classe/eliminar.html',{'classe': classe} )
   
   
   
 
   
   
   
   
   
   