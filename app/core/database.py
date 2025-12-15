import psycopg2
import os

# Usamos una variable global simple para almacenar la conexión (suficiente para esta arquitectura)
_db_connection = None

def get_db_connection(app):
    """Obtiene una conexión persistente, inicializándola si es necesario."""
    global _db_connection
    if _db_connection is None:
        try:
            _db_connection = psycopg2.connect(
                host=app.config['DB_HOST'],
                database=app.config['DB_NAME'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                port=app.config['DB_PORT']
            )
            # Asegurar que las transacciones se manejen
            _db_connection.autocommit = False
            
        except psycopg2.Error as e:
            print(f"ERROR: No se pudo conectar a la base de datos: {e}")
            if not app.config['TESTING'] and not app.config['DEBUG']:
                # En producción, si la DB falla, la app debe fallar
                raise ConnectionError(f"Fallo crítico al conectar a PostgreSQL: {e}")
            
            # En desarrollo, permitimos que siga (pero sin caché)
            _db_connection = False 
    
    # Retorna None si la conexión falló previamente
    if _db_connection is False:
        return None
        
    return _db_connection

def close_db_connection(exception=None):
    """Cierra la conexión global de la base de datos (usado en teardown)."""
    global _db_connection
    if _db_connection and _db_connection is not False:
        _db_connection.close()
        _db_connection = None

def init_db(app):
    """Inicializa la estructura de la base de datos (crea la tabla de caché)."""
    conn = get_db_connection(app)
    if not conn: 
        app.logger.warning("No se pudo inicializar la DB. La caché no funcionará.")
        return
        
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    cache_key VARCHAR(255) PRIMARY KEY,
                    data JSONB NOT NULL,
                    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
            conn.commit()
        app.logger.info("Tabla 'cache' verificada/creada.")
    except Exception as e:
        app.logger.error(f"ERROR al inicializar la base de datos: {e}")
        conn.rollback()