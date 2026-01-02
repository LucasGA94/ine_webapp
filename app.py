import os
import requests
import logging
from flask import Flask, render_template, jsonify

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'cambia-esta-clave-insegura')
    DB_HOST = os.getenv('DB_HOST', 'db')
    DB_NAME = os.getenv('DB_NAME', 'ine_cache')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_PORT = os.getenv('DB_PORT', '5432')
    INE_BASE_URL = "https://servicios.ine.es/wstempus/js/es/"

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(config_dict.get(config_name, DevelopmentConfig))

    logging.basicConfig(level=logging.INFO if app.debug else logging.WARNING)

    def fetch_ine_data(id_type, id_value, params=None):
        url = f"{app.config['INE_BASE_URL']}{id_type}/{id_value}"
        params = params or {}
        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            app.logger.error(f"Error fetching INE: {e}")
            return None

    @app.route('/')
    def index():
        return """
        <h1>¡INE Dashboard funcionando! 🚀</h1>
        <ul>
            <li><a href="/ipc">IPC</a></li>
            <li><a href="/poblacion">Población</a></li>
            <li><a href="/infra/health">Health check</a></li>
        </ul>
        """

    @app.route('/ipc')
    def ipc():
        data = fetch_ine_data('DATOS_TABLA', '50902', {'nlast': 12})
        if data is None:
            return "Error cargando datos del INE", 500
        return render_template('ipc/ipc.html', data=data)

    @app.route('/poblacion')
    def poblacion():
        # ID válido para población residente total España (serie anual)
        data = fetch_ine_data('DATOS_TABLA', '56934', {'nlast': 20})
        if data is None:
            return "Error cargando datos del INE", 500
        return render_template('poblacion/poblacion.html', data=data)

    @app.route('/infra/health')
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.route('/infra/ready')
    def ready():
        return jsonify({"status": "ready"}), 200

    return app

app = create_app(os.getenv('FLASK_CONFIG', 'development'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)