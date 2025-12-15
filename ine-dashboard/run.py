import os
import sys
# Necesario para que Python encuentre los módulos dentro de la carpeta 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

# La función create_app() se define en app/__init__.py
from app import create_app

# Determina el modo de configuración (development, production)
config_mode = os.getenv('FLASK_CONFIG', 'development') 

# Crea la instancia de la aplicación Flask
app = create_app(config_mode)

if __name__ == "__main__":
    # Bloque de ejecución para desarrollo local directo (python run.py)
    # En Docker Compose, este comando será sobrescrito en modo prod.
    port = int(os.getenv("APP_PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get('DEBUG', True))