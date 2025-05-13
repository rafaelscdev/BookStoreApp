from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import os
import git
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def update(request):
    logger.info(f"Webhook recebido: {request.method}")
    if request.method == "POST":
        try:
            repo_path = os.environ.get('REPO_PATH', '/home/rafaelscorreadev/BookStoreApp')
            logger.info(f"Usando repositório em: {repo_path}")
            
            repo = git.Repo(repo_path)
            origin = repo.remotes.origin
            
            logger.info("Fazendo pull das alterações...")
            origin.pull()
            
            logger.info("Pull realizado com sucesso")
            return HttpResponse("Updated code on PythonAnywhere")
        except Exception as e:
            logger.error(f"Erro ao atualizar código: {str(e)}")
            return HttpResponse(f"Error updating code: {str(e)}", status=500)
    else:
        logger.warning(f"Método não permitido: {request.method}")
        return HttpResponse("Couldn't update the code on PythonAnywhere")


def hello_world(request):
    template = loader.get_template('hello_world.html')
    return HttpResponse(template.render()) 