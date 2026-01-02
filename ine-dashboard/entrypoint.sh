#!/usr/bin/env bash
set -e

echo "Directorio actual: $(pwd)"
echo "Contenido de /app: $(ls /app)"
echo "PYTHONPATH: $PYTHONPATH"

export PORT=${APP_PORT:-8000}

echo "Ejecutando la app con: $@"
exec "$@"