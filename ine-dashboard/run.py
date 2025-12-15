import os
# No es necesario importar sys ni manipular el path si el WORKDIR es /app
# import sys 

# La función create_app() se define en app/__init__.py
# Esta importación asume que 'app' está en el PYTHONPATH, 
# lo cual Docker garantiza con WORKDIR /app.
from app import create_app

# Determina el modo de configuración (development, production)
config_mode = os.getenv('FLASK_CONFIG', 'development') 

# Crea la instancia de la aplicación Flask
app = create_app(config_mode)

if __name__ == "__main__":
    # Bloque de ejecución para desarrollo local directo (python run.py)
    port = int(os.getenv("APP_PORT", 8000))
    # app.config.get('DEBUG', True) debería estar en app/__init__.py
    app.run(host="0.0.0.0", port=port, debug=app.config.get('DEBUG', True))