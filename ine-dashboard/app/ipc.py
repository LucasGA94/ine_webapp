from flask import Blueprint, render_template
import requests

ipc = Blueprint('ipc', __name__, url_prefix='/ipc')


@ipc.route('/')
def index():
    """
    Muestra el Índice de Precios de Consumo (IPC) General.
    Obtiene datos de la API del INE.
    """
    data = []
    error = None
    
    try:
        # API del INE para IPC General (Base 2021)
        # IPC General Nacional - Código de operación: 50904
        url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/50904"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        json_data = response.json()
        
        # Extraer los últimos 12 registros
        if json_data and len(json_data) > 0:
            serie = json_data[0].get('Data', [])
            data = serie[-12:] if len(serie) > 12 else serie
            
    except requests.exceptions.RequestException as e:
        error = f"Error al obtener datos del INE: {str(e)}"
    except (KeyError, IndexError) as e:
        error = f"Error al procesar los datos: {str(e)}"
    
    return render_template('ipc/ipc.html', data=data, error=error)
