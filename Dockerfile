FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app/backend

# Dependencias primeiro para aproveitar o cache de camadas.
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia somente o backend; o .dockerignore exclui segredos locais.
COPY backend/ ./

# Arquivos estaticos para o WhiteNoise. Valores abaixo sao descartaveis
# e utilizados apenas durante a construcao, sem acessar o banco.
RUN SECRET_KEY=chave-temporaria-apenas-para-build \
    DB_NAME=build \
    DB_USER=build \
    DB_PASSWORD=build \
    python manage.py collectstatic --noinput

# Executar o servidor sem privilegios de root.
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["gunicorn", "papellog.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--access-logfile", "-"]
