#!/usr/bin/env python3
import os
import subprocess
import sys

def run_command(command):
    """Executa um comando e retorna o resultado"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao executar comando: {e.stderr}"

def deploy():
    """Executa o processo de deploy"""
    print("Iniciando deploy...")
    
    # Atualiza o código
    success, output = run_command("git pull origin main")
    if not success:
        print(f"Erro ao atualizar código: {output}")
        return False
    print("Código atualizado com sucesso")
    
    # Instala/atualiza dependências
    success, output = run_command("poetry install")
    if not success:
        print(f"Erro ao instalar dependências: {output}")
        return False
    print("Dependências instaladas com sucesso")
    
    # Executa migrações
    success, output = run_command("poetry run python manage.py migrate")
    if not success:
        print(f"Erro ao executar migrações: {output}")
        return False
    print("Migrações executadas com sucesso")
    
    # Coleta arquivos estáticos
    success, output = run_command("poetry run python manage.py collectstatic --noinput")
    if not success:
        print(f"Erro ao coletar arquivos estáticos: {output}")
        return False
    print("Arquivos estáticos coletados com sucesso")
    
    # Reinicia o servidor web
    success, output = run_command("touch /var/www/rafaelscorreadev_pythonanywhere_com_wsgi.py")
    if not success:
        print(f"Erro ao reiniciar servidor: {output}")
        return False
    print("Servidor reiniciado com sucesso")
    
    print("Deploy concluído com sucesso!")
    return True

if __name__ == "__main__":
    deploy() 