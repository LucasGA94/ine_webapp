from flask import Blueprint, render_template
from .services import get_ipc_data

# Definición del Blueprint
# El url_prefix='/ipc' ya está definido en app/__init__.py
ipc_bp = Blueprint('ipc', __name__, template_folder='../../templates')

@ipc_bp.route('/')
def index():
    """
    Ruta principal del módulo IPC.
    Renderiza la tabla con los datos de inflación.
    """
    data = get_ipc_data()
    error = None
    
    if not data:
        error = "No se pudieron obtener los datos del INE. Inténtelo más tarde."

    return render_template('ipc/ipc.html', data=data, error=error)