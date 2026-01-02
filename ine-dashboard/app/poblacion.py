from flask import Blueprint, render_template
import requests

poblacion = Blueprint('poblacion', __name__, url_prefix='/poblacion')


@poblacion.route('/')
def index():
    """
    Muestra datos de población residente en España.
    Obtiene datos de la API del INE.
    """
    series = []
    error = None
    
    try:
        # API del INE para Población residente en España
        # Población residente - Código: 31304
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/31304"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        json_data = response.json()
        
        # Extraer datos
        if json_data and len(json_data) > 0:
            series = json_data[0].get('Data', [])
            
    except requests.exceptions.RequestException as e:
        error = f"Error al obtener datos del INE: {str(e)}"
    except (KeyError, IndexError) as e:
        error = f"Error al procesar los datos: {str(e)}"
    
    return render_template('poblacion/población.html', series=series, error=error)
