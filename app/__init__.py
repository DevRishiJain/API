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
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(tasks_bp, url_prefix='/api/tasks')
    
    @app.route('/')
    def index():
        return {
            'message': 'Welcome to the Task Management API',
            'version': '1.0.0',
            'database': app.config['SQLALCHEMY_DATABASE_URI'].split('://')[-1].split('@')[0].split('/')[0]
        }
    
    # Create database tables - only in development mode
    # In production, migrations should be used instead of direct db.create_all()
    with app.app_context():
        import os
        if not os.environ.get('RENDER') and not app.config['SQLALCHEMY_DATABASE_URI'].startswith('postgresql'):
            # Create data directory if it doesn't exist (for SQLite)
            if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
                db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
                import os
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            db.create_all()
    
    return app
