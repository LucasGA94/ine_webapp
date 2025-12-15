#!/usr/bin/env bash
set -e

# --- TAREAS DE PRE-INICIO (Ej. esperar a la DB) ---

# Si estuviera instalado un cliente de PostgreSQL (ej. 'apt-get install postgresql-client'):
echo "Esperando a PostgreSQL..."
/usr/local/bin/wait-for-it.sh db:5432 -t 30 -- echo "PostgreSQL está listo."

# Por ahora, simplemente exportamos el puerto para cualquier posible uso
export PORT=${APP_PORT:-8000}

# Ejecuta el comando principal definido en el Dockerfile (CMD) o en docker-compose
echo "Ejecutando el comando de inicio: $@"
exec "$@"