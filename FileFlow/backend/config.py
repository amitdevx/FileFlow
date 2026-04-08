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
    
    # Performance optimization settings
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year cache for static files
    JSON_SORT_KEYS = False  # Disable JSON key sorting for performance
    PROPAGATE_EXCEPTIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    
    # Compression settings (for nginx to use gzip)
    COMPRESSION_ENABLED = True