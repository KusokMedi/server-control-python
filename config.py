import secrets
from datetime import timedelta

class Config:
    SECRET_KEY = secrets.token_hex(32)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///webcontrol.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(seconds=3600)
    
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
    
    CACHE_TYPE = 'simple'
    
    RATELIMIT_STORAGE_URL = 'memory://'
    RATELIMIT_ENABLED = True
    
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = False
