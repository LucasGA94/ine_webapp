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

# =========================================================
# 1. COPIA DEL CÓDIGO FUENTE
# El 'context: ..' en el docker-compose.yml asegura que se copie la raíz del proyecto.
# Esto incluye la carpeta 'app/', 'run.py', y la carpeta 'ine-dashboard/' completa.
COPY . /app/ 
# =========================================================

# Copia los archivos de dependencias e instálalos
# CORRECCIÓN: Buscamos requirements.txt dentro de la carpeta ine-dashboard/
COPY ine-dashboard/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================================================
# 2. CONFIGURACIÓN DEL ENTRYPOINT (RUTAS CORREGIDAS)
# Debemos especificar el subdirectorio 'ine-dashboard/' para encontrar estos scripts.
# =========================================================

# Buscamos wait-for-it.sh
COPY ine-dashboard/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Buscamos entrypoint.sh
COPY ine-dashboard/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# =========================================================
# 3. CORRECCIÓN DE PYTHON
# Añade el directorio /app al PYTHONPATH para que Python pueda encontrar el paquete 'app'.
ENV PYTHONPATH=/app:$PYTHONPATH 
# =========================================================

# Define el entrypoint para ejecutar tareas de pre-inicio
ENTRYPOINT ["entrypoint.sh"]

# Comando por defecto con --chdir para cambiar al subdirectorio antes de cargar la app
CMD ["gunicorn", "--chdir", "/app/ine-dashboard", "run:app", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]