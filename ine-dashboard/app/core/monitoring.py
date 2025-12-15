# app/core/monitoring.py
from flask import Blueprint, current_app, jsonify
import requests

# Creamos el Blueprint
monitoring_bp = Blueprint('monitoring', __name__)

@monitoring_bp.route('/health')
def health():
    """Endpoint simple para comprobar que la app está viva"""
    return jsonify({"status": "healthy", "app": "ine-dashboard"}), 200

@monitoring_bp.route('/api-status')
def api_status():
    """Comprueba si la API del INE responde"""
    base_url = current_app.config.get('INE_BASE_URL')
    if not base_url:
        return jsonify({"error": "INE_BASE_URL no configurado"}), 500
    
    try:
        test_url = f"{base_url}DATOS_TABLA/50902"  # Tabla de ejemplo conocida
        response = requests.get(test_url, timeout=10)
        ine_ok = response.status_code == 200
    except Exception:
        ine_ok = False
    
    return jsonify({
        "status": "ok" if ine_ok else "error",
        "ine_api_reachable": ine_ok
    }), 200 if ine_ok else 503

def fetch_ine_data(id_type, id_value, params=None):
    """
    Wrapper genérico para llamar a la API JSON del INE (wstempus).
    
    :param id_type: El tipo de llamada (ej. 'DATOS_TABLA', 'SERIES_TABLA').
    :param id_value: El ID de la tabla o serie (ej. '50902').
    :param params: Diccionario de parámetros adicionales.
    :return: El JSON decodificado o None en caso de error.
    """
    base_url = current_app.config['INE_BASE_URL']
    url = f"{base_url}{id_type}/{id_value}"
    
    if params is None:
        params = {}
    
    try:
        current_app.logger.info(f"Consultando INE: {url} con params={params}")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        current_app.logger.error(f"Error HTTP del INE ({url}): {e.response.status_code}")
        return None
    
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error de conexión al API del INE: {e}")
        return None