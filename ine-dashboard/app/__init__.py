from flask import Flask, redirect, url_for
import os


def create_app(config_mode='development'):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_mode: Configuration mode ('development', 'production', etc.)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['DEBUG'] = config_mode == 'development'
    
    # Database configuration (if needed)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Register blueprints
    from app.ipc import ipc
    from app.poblacion import poblacion
    
    app.register_blueprint(ipc)
    app.register_blueprint(poblacion)
    
    # Root route - redirect to IPC page
    @app.route('/')
    def index():
        return redirect(url_for('ipc.index'))
    
    return app
