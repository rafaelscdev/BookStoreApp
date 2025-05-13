# Bookstoreapp

Bookstore APP from Backend Python course from EBAC

## Tecnologias Utilizadas

- Python 3.12+
- Django
- Poetry (Gerenciador de dependências)
- Docker & Docker Compose
- PostgreSQL
- Make (opcional, mas recomendado)

## Pré-requisitos

```
Python 3.12+
Poetry
Docker && docker-compose
Make (opcional, mas recomendado)
```

## Ambiente de Desenvolvimento

O projeto pode ser executado de duas maneiras:

1. **Localmente com Poetry**: Ideal para desenvolvimento rápido e testes
2. **Com Docker**: Recomendado para garantir consistência entre ambientes

## Quickstart

1. Clone this project

   ```shell
   git clone https://github.com/rafaelscdev/BookStoreApp.git 
   ```

2. Install dependencies:

   ```shell
   cd bookstoreapp
   make install  # ou poetry install
   ```

3. Run local dev server:

   ```shell
   make run  # ou poetry run python manage.py runserver
   make local-migrate  # ou poetry run python manage.py migrate
   ```
   
4. Run docker dev server environment:

   ```shell
   make build  # ou docker-compose build
   make up     # ou docker-compose up -d
   make migrate  # ou docker-compose exec web python manage.py migrate
   ```

5. Run tests:

   ```shell
   # Com Docker:
   make test  # ou docker-compose exec web python manage.py test
   
   # Local com Poetry:
   make local-test  # ou poetry run python manage.py test
   ```

## Comandos Make Disponíveis

### Desenvolvimento com Docker

- `make build` - Constrói os containers Docker
- `make up` - Inicia os containers Docker em background
- `make down` - Para e remove os containers Docker
- `make restart` - Reinicia os containers Docker
- `make logs` - Mostra os logs dos containers
- `make migrate` - Executa as migrações do Django
- `make migrations` - Cria novas migrações
- `make shell` - Abre o shell do Django
- `make test` - Executa os testes

### Desenvolvimento Local com Poetry

- `make install` - Instala as dependências do projeto
- `make run` - Executa o servidor de desenvolvimento local
- `make local-migrate` - Executa as migrações localmente
- `make local-test` - Executa os testes localmente

### Limpeza e Manutenção

- `make clean` - Remove arquivos temporários e caches
- `make reset-db` - Remove e recria o volume do banco de dados

Para ver todos os comandos disponíveis, execute:

```shell
make help
```

## Estrutura do Projeto

```
bookstoreapp/
├── bookstore/          # Configurações principais do Django
├── books/             # Aplicação principal
├── tests/             # Testes automatizados
├── docker/            # Configurações Docker
└── manage.py          # Script de gerenciamento Django
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.