from django.core.mail import EmailMessage
from django.conf import settings
import logging

logger = logging.getLogger(__name__) 


#Escola
def enviar_dados_acesso_escola(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o escola recém-cadastrado.
    """
    try:
        mensagem = f"""
        Bem-vindo! {nome},<br><br>
        A sua escola foi cadastrada com sucesso na nossa plataforma smartschool!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False

#Diretor
def enviar_dados_acesso_diretor(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o diretor recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como diretor(a) foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False


#Pedagógico
def enviar_dados_acesso_pedagogico(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o pedagógico recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como diretor(a) pedagógico foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False
    
#Administrativo
def enviar_dados_acesso_administrativo(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o administrativo recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como diretor(a) administrativo foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False
#Coordenador
def enviar_dados_acesso_coordenador(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o coordenador recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como diretor(a) coordenador foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False
    
#Professor
def enviar_dados_acesso_professor(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o professor recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como professor(a) foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False
    
    
    
#Aluno
def enviar_dados_acesso_aluno(nome, username, senha, email_destino):
    """
    Envia e-mail com os dados de acesso ao sistema para o aluno recém-cadastrado.
    """
    try:
        mensagem = f"""
        Olá {nome},<br><br>
        Seu cadastro como aluno(a) foi realizado com sucesso!<br><br>
        <strong>Usuário:</strong> {username}<br>
        <strong>Senha:</strong> {senha}<br><br>
        Acesse o sistema usando suas credenciais.<br><br>
        Atenciosamente,<br>
        Equipe SmartSchool.
        """

        email_msg = EmailMessage(
            'Dados de Acesso ao Sistema SmartSchool',
            mensagem,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino],
        )
        email_msg.content_subtype = 'html'
        email_msg.send(fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar e-mail para {email_destino}: {e}")
        return False
