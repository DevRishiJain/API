import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Determine if we're running on Render (production) or locally (development)
    if os.environ.get('RENDER') or os.environ.get('IS_PRODUCTION'):
        # Production environment (Render with PostgreSQL)
        database_url = os.environ.get('DATABASE_URL')
        # Handle potential 'postgres://' to 'postgresql://' conversion for SQLAlchemy 1.4+
        if database_url and database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Development environment (local SQLite)
        # Use a relative path for SQLite that works in any environment
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
