from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Cria os grupos Escolar, Aluno, Professor, Direitor, Pedagogico, Administrativo, Coordenador'

    def handle(self, *args, **kwargs):
        grupos = ['Escola','Aluno', 'Professor', 'Direitor', 'Pedagogico', 'Administrativo', 'Coordenador']
        for nome in grupos:
            grupo, criado = Group.objects.get_or_create(name=nome)
            if criado:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nome}" criado com sucesso.'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{nome}" já existe.'))



#python manage.py criar_grupos
