from app.core.ine_client import fetch_ine_data
from app.core.cache import get_cached_data, set_cached_data

# ID de la tabla del INE: Población residente por fecha, sexo y edad
# Nota: Esta tabla es semestral/anual
POBLACION_TABLE_ID = "48268"

def get_poblacion_data():
    """
    Obtiene datos de población residente.
    Logica similar al servicio de IPC pero adaptada a la estructura de población.
    """
    cache_key = f"ine_table_{POBLACION_TABLE_ID}"
    
    # 1. Caché
    cached = get_cached_data(cache_key)
    if cached:
        return cached

    # 2. API INE (últimos 4 periodos para ver la evolución reciente)
    raw_data = fetch_ine_data("DATOS_TABLA", POBLACION_TABLE_ID, params={"nlast": 4})
    
    if not raw_data:
        return []

    # 3. Procesamiento
    # La tabla de población suele devolver muchas series (Total, Hombres, Mujeres, por edades...)
    # Vamos a filtrar para quedarnos con el "Total Nacional" y "Todas las edades" 
    # para no saturar la vista básica.
    
    filtered_series = []
    
    if isinstance(raw_data, list):
        for serie in raw_data:
            nombre = serie.get("Nombre", "")
            # Filtro básico: Queremos el Total, no desgloses muy específicos
            # Esto depende de cómo el INE nombre las series en ese momento
            if "Total" in nombre and "Todas las edades" in nombre:
                filtered_series.append({
                    "nombre": nombre,
                    "datos": serie.get("Data", [])
                })
        
        # Si el filtro es muy estricto y no saca nada, devolvemos las primeras 5 series por defecto
        if not filtered_series:
            for serie in raw_data[:5]:
                filtered_series.append({
                    "nombre": serie.get("Nombre", "Serie sin nombre"),
                    "datos": serie.get("Data", [])
                })

    # 4. Guardar en caché
    if filtered_series:
        set_cached_data(cache_key, filtered_series)
        
    return filtered_series