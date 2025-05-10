# Variáveis do projeto
PYTHON_VERSION ?= 3.12
PROJECT_NAME = bookstoreapp

# Opções do Poetry
POETRY ?= poetry
RUN_POETRY = $(POETRY) run

# Opções do pytest
PYTEST_OPTIONS ?= --verbosity=2 --showlocals --cov=.

# Cores para output
COLOR_RESET = \033[0m
COLOR_INFO = \033[36m
COLOR_SUCCESS = \033[32m
COLOR_WARNING = \033[33m

##@ Desenvolvimento com Docker

.PHONY: build
build: ## Constrói os containers Docker
	docker-compose build

.PHONY: up
up: ## Inicia os containers Docker em background
	docker-compose up -d

.PHONY: down
down: ## Para e remove os containers Docker
	docker-compose down

.PHONY: restart
restart: down up ## Reinicia os containers Docker

.PHONY: logs
logs: ## Mostra os logs dos containers
	docker-compose logs -f

.PHONY: migrate
migrate: ## Executa as migrações do Django
	docker-compose exec web python manage.py migrate

.PHONY: migrations
migrations: ## Cria novas migrações baseadas nas mudanças dos models
	docker-compose exec web python manage.py makemigrations

.PHONY: shell
shell: ## Abre o shell do Django
	docker-compose exec web python manage.py shell

.PHONY: test
test: ## Executa os testes
	docker-compose exec web python manage.py test

##@ Desenvolvimento Local com Poetry

.PHONY: install
install: ## Instala as dependências do projeto usando Poetry
	$(POETRY) install

.PHONY: run
run: ## Executa o servidor de desenvolvimento local
	$(RUN_POETRY) python manage.py runserver

.PHONY: local-migrate
local-migrate: ## Executa as migrações localmente
	$(RUN_POETRY) python manage.py migrate

.PHONY: local-test
local-test: ## Executa os testes localmente
	$(RUN_POETRY) python manage.py test

##@ Limpeza e Manutenção

.PHONY: clean
clean: ## Remove arquivos temporários e caches
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

.PHONY: reset-db
reset-db: ## Remove e recria o volume do banco de dados
	docker-compose down -v
	docker-compose up -d
	make migrate

##@ Utilidades

.PHONY: help
help: ## Mostra esta mensagem de ajuda
	@awk 'BEGIN {FS = ":.*##"; printf "\nUso:\n  make \033[36m<target>\033[0m\n"} \
		/^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } \
		/^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) }' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help 