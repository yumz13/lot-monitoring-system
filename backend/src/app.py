from flask import Flask
from src.config import Config
from src.models import init_models
from src.routes import register_blueprints

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    init_models(app)
    
    # Register blueprints
    register_blueprints(app)
    
    @app.route('/')
    def index():
        return "Production Traveler Slip System API"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)