import os
from flask import Flask
from dotenv import load_dotenv 

# Cargar .env si estamos en desarrollo
if os.environ.get('FLASK_CONFIG', 'development') == 'development':
    load_dotenv()

# Importar componentes de la aplicación
from .config import config_dict
from .core.database import init_db, close_db_connection 

def create_app(config_name='development'):
    """
    Función Factory de la Aplicación.
    Crea la instancia de Flask y configura todos los módulos y extensiones.
    """
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # 1. Inicializar Core (DB, Caché)
    # Inicializa la DB (crea la tabla caché). Debe estar dentro del contexto de la app.
    with app.app_context():
        init_db(app) 
        
    # Registrar un handler para cerrar la conexión al terminar la petición/app
    app.teardown_appcontext(close_db_connection)

    # 2. Registrar Blueprints (Módulos de Negocio)
    from .modules.ipc.routes import ipc_bp
    from .modules.poblacion.routes import poblacion_bp
    
    # El blueprint de IPC tendrá la ruta raíz /ipc
    app.register_blueprint(ipc_bp, url_prefix='/ipc')
    # El blueprint de Población tendrá la ruta raíz /poblacion
    app.register_blueprint(poblacion_bp, url_prefix='/poblacion')

    # 3. Registrar Módulos de Infraestructura (Monitoring, Health Check)
    from .core.monitoring import monitoring_bp
    app.register_blueprint(monitoring_bp, url_prefix='/infra')

    return app