import os

class Config:
    # Configuración base común
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'default-unsafe-key-change-it')
    
    # Configuración de Base de Datos
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'ine_cache')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    # INE API
    # URL base para el servicio JSON (DATOS_TABLA, etc.)
    INE_BASE_URL = "https://servicios.ine.es/wstempus/js/es/"
    
    # Caché: 24 horas (86400 segundos) por defecto para la mayoría de datos del INE
    CACHE_EXPIRATION_SECONDS = 86400

class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True
    # En Docker Compose, 'db' es el hostname del servicio de PostgreSQL
    DB_HOST = os.getenv('DB_HOST', 'db') 

class ProductionConfig(Config):
    # Desactiva debug y testing en producción
    DEBUG = False
    TESTING = False
    
class TestingConfig(Config):
    TESTING = True
    # Podría usar una DB in-memory o una DB de pruebas dedicada
    DB_NAME = 'ine_test'

config_dict = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}