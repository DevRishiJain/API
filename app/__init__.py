from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

from .config import Config
from .models import db
from .routes.auth import auth_bp
from .routes.tasks import tasks_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)
    Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    
    @app.route('/')
    def index():
        return {
            'message': 'Welcome to the Task Management API',
            'version': '1.0.0'
        }
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
