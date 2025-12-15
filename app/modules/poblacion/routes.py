from flask import Blueprint, render_template
from .services import get_poblacion_data

# El url_prefix='/poblacion' se define en el registro del app factory
poblacion_bp = Blueprint('poblacion', __name__, template_folder='../../templates')

@poblacion_bp.route('/')
def index():
    """
    Ruta principal del módulo Población.
    """
    series_data = get_poblacion_data()
    error = None
    
    if not series_data:
        error = "No hay datos de población disponibles o hubo un error de conexión."

    # Pasamos 'series' al template, ya que es una lista de objetos (Nombre, Datos)
    return render_template('poblacion/poblacion.html', series=series_data, error=error)