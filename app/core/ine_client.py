import requests
from flask import current_app

def fetch_ine_data(id_type, id_value, params=None):
    """
    Wrapper genérico para llamar a la API JSON del INE (wstempus).
    
    :param id_type: El tipo de llamada (ej. 'DATOS_TABLA', 'SERIES_TABLA').
    :param id_value: El ID de la tabla o serie (ej. '50902').
    :param params: Diccionario de parámetros adicionales de la URL (ej. {'nlast': 12, 'tip': 'A'}).
    :return: El JSON decodificado de la API (list/dict) o None en caso de error.
    """
    base_url = current_app.config['INE_BASE_URL']
    
    # Construir la URL completa
    # Ejemplo: https://servicios.ine.es/wstempus/js/es/DATOS_TABLA/50902
    url = f"{base_url}{id_type}/{id_value}"
    
    if params is None:
        params = {}
    
    try:
        current_app.logger.info(f"Consultando INE: {url} con {params}")
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status() # Lanza una excepción para códigos 4xx/5xx

        return response.json()

    except requests.exceptions.HTTPError as e:
        current_app.logger.error(f"Error HTTP del INE para {url}: {e.response.status_code}")
        # current_app.logger.error(f"Respuesta del INE: {e.response.text[:200]}...")
        return None
        
    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"Error de conexión al API del INE: {e}")
        return None