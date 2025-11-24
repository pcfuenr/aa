FROM python:3.12-slim

WORKDIR /workouts_udec_backend 

# Instalar dependencias
COPY requirements.txt . 
RUN pip install -r requirements.txt

COPY . .

# Se expone puerto
EXPOSE 4173

# Instalar curl (para healthcheck)
RUN apt-get update && apt-get install -y curl postgresql-client && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root , da permisos y cambia a el
RUN useradd -m MiPanita \
    && chown -R MiPanita:MiPanita /workouts_udec_backend
USER MiPanita

CMD ["sh", "./cmd_script.sh"]
