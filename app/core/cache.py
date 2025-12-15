from datetime import datetime, timedelta
import json
from flask import current_app
from .database import get_db_connection

def get_cached_data(cache_key):
    """
    Recupera datos de la caché si son válidos. Retorna dict/list o None.
    """
    conn = get_db_connection(current_app)
    if not conn: return None
    
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT data FROM cache WHERE cache_key = %s AND expires_at > %s",
                (cache_key, datetime.now())
            )
            result = cur.fetchone()
            if result:
                # El resultado es un JSONB, psycopg2 lo deserializa a dict/list
                return result[0] 
            return None
    except Exception as e:
        current_app.logger.error(f"Error al leer caché para {cache_key}: {e}")
        return None

def set_cached_data(cache_key, data):
    """
    Guarda datos en la caché con la fecha de expiración definida en la configuración.
    """
    conn = get_db_connection(current_app)
    if not conn: return
    
    try:
        expiry = current_app.config['CACHE_EXPIRATION_SECONDS']
        expires_at = datetime.now() + timedelta(seconds=expiry)
        
        # PostgreSQL necesita el dato como string JSON
        json_data = json.dumps(data)
        
        with conn.cursor() as cur:
            # ON CONFLICT DO UPDATE: Actualiza si ya existe la clave
            cur.execute(
                """
                INSERT INTO cache (cache_key, data, expires_at) 
                VALUES (%s, %s::jsonb, %s) 
                ON CONFLICT (cache_key) 
                DO UPDATE SET data = EXCLUDED.data, expires_at = EXCLUDED.expires_at
                """,
                (cache_key, json_data, expires_at)
            )
            conn.commit()
    except Exception as e:
        current_app.logger.error(f"Error al escribir caché para {cache_key}: {e}")
        conn.rollback()