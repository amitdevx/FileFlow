import os
import warnings

class Config:
    # SECRET_KEY should be set via environment variable in production
    # A random fallback is used only for development; this will invalidate
    # sessions on every restart
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        warnings.warn(
            "SECRET_KEY not set in environment. Using random key. "
            "Sessions will be invalidated on restart. "
            "Set SECRET_KEY environment variable for production use.",
            RuntimeWarning
        )
        SECRET_KEY = os.urandom(24)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///fileflow.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'user_files'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload