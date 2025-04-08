import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # Determine if we're running on Render (production) or locally (development)
    if os.environ.get('RENDER') or os.environ.get('DATABASE_URL', '').startswith('postgres'):
        # Production environment (Render with PostgreSQL)
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
        # Handle potential 'postgres://' to 'postgresql://' conversion
        if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
            SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
    else:
        # Development environment (local SQLite)
        SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'  # Using a relative path that works in any environment
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
