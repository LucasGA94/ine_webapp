from app.core.ine_client import fetch_ine_data
from app.core.cache import get_cached_data, set_cached_data

# ID de la tabla del INE para el IPC General (Base 2021)
IPC_TABLE_ID = "50902"

def get_ipc_data():
    """
    Obtiene los datos del IPC.
    1. Intenta leer de la caché (base de datos).
    2. Si falla, llama a la API del INE.
    3. Guarda en caché y devuelve los datos procesados.
    """
    cache_key = f"ine_table_{IPC_TABLE_ID}"
    
    # 1. Intentar obtener de caché
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    # 2. Si no hay caché, pedir al INE (últimos 12 periodos)
    # nlast=12 trae el último año
    raw_data = fetch_ine_data("DATOS_TABLA", IPC_TABLE_ID, params={"nlast": 12})
    
    if not raw_data:
        return []

    # 3. Procesamiento de datos
    # El INE devuelve una lista de series. Buscamos la serie "General".
    # Si la petición es genérica, suele devolver varias. Filtramos o cogemos la primera.
    processed_data = []
    
    # Buscamos la serie que contiene los datos (usualmente 'Data' dentro del objeto)
    # Simplificación: Tomamos la primera serie disponible que tenga datos
    if isinstance(raw_data, list) and len(raw_data) > 0:
        # Extraemos la lista de valores temporales ('Data') de la primera serie
        series_data = raw_data[0].get("Data", [])
        
        # Opcional: Formatear fechas o valores aquí si fuera necesario
        processed_data = series_data

    # 4. Guardar en caché el resultado PROCESADO (o el crudo, según preferencia)
    # Aquí guardamos lo procesado para ahorrar CPU en lecturas futuras
    if processed_data:
        set_cached_data(cache_key, processed_data)
        
    return processed_data