# Usa una imagen base de Python estable
FROM python:3.11-slim

# Configuraciones de entorno (evita que Python almacene bytes compilados, desactiva el buffering)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de dependencias e instálalos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script de inicio y lo hace ejecutable
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copia el código fuente de la aplicación (incluyendo app/ y run.py)
COPY app/ app/
COPY run.py .

# Define el entrypoint para ejecutar tareas de pre-inicio
ENTRYPOINT ["entrypoint.sh"]

# Comando por defecto (Usado en producción o si no se sobrescribe)
# Arranca Gunicorn con 4 workers, enlazado al puerto 8000
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]