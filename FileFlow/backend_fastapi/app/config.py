import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings using pydantic-settings"""
    
    # App info
    app_name: str = "FileFlow API"
    app_version: str = "2.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./fileflow.db"
    
    # JWT settings
    secret_key: str = os.urandom(32).hex()
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # File upload settings
    upload_folder: str = "user_files"
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    allowed_extensions: list[str] = [
        "txt", "pdf", "png", "jpg", "jpeg", "gif", 
        "zip", "tar", "7z", "mp4", "mov", "mp3", "wav"
    ]
    
    # CORS settings
    cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
