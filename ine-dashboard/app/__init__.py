import os
from flask import Flask, jsonify, Blueprint
from dotenv import load_dotenv 

if os.environ.get('FLASK_CONFIG', 'development') == 'development':
    load_dotenv()

from .config import config_dict
from .core.database import init_db, close_db_connection 

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    with app.app_context():
        init_db(app) 
        
    app.teardown_appcontext(close_db_connection)

    from .modules.ipc.routes import ipc_bp
    from .modules.poblacion.routes import poblacion_bp
    
    app.register_blueprint(ipc_bp, url_prefix='/ipc')
    app.register_blueprint(poblacion_bp, url_prefix='/poblacion')

    # Blueprint de monitorización básico
    monitoring_bp = Blueprint('monitoring', __name__)

    @monitoring_bp.route('/health')
    def health():
        return jsonify({"status": "healthy", "app": "ine-dashboard"}), 200

    @monitoring_bp.route('/ready')
    def ready():
        return jsonify({"status": "ready"}), 200

    app.register_blueprint(monitoring_bp, url_prefix='/infra')

    # Ruta raíz para probar que la app responde
    @app.route('/')
    def index():
        return """
        <h1>¡INE Dashboard funcionando! 🚀</h1>
        <p>Endpoints disponibles:</p>
        <ul>
            <li><a href="/ipc">/ipc</a></li>
            <li><a href="/poblacion">/poblacion</a></li>
            <li><a href="/infra/health">/infra/health</a></li>
            <li><a href="/infra/ready">/infra/ready</a></li>
        </ul>
        <p>Si ves esto, ¡todo está correcto!</p>
        """

    return app