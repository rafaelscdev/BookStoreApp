# Usa uma imagem base enxuta do Python
FROM python:3.12-slim

# Variáveis de ambiente para Python, pip e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Adiciona o Poetry ao PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instala dependências do sistema
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
        libpq-dev \
        gcc \
        pkg-config \
        default-libmysqlclient-dev \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Instala o psycopg2 (caso use Postgres)
RUN apt-get update \
    && apt-get install libpq-dev gcc \
    && pip install psycopg2

# Define o diretório de trabalho
WORKDIR /usr/src/app

# Copia os arquivos de dependências do projeto
COPY poetry.lock pyproject.toml ./

# Instala as dependências do projeto
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o restante do código do projeto
COPY . .

# Expõe a porta padrão do Django/Heroku
ENV PORT=8000
EXPOSE $PORT

# Coleta os arquivos estáticos
RUN poetry run python manage.py collectstatic --noinput

# Comando para rodar a aplicação
CMD poetry run gunicorn bookstoreapp.wsgi:application --bind 0.0.0.0:$PORT