"""
Configuration de l'application - Millésime Sans Frontières
Gestion des variables d'environnement et paramètres
"""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Informations de base
    APP_NAME: str = "Millésime Sans Frontières API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Base de données
    DATABASE_URL: str = "postgresql://millesime_user:millesime_password@localhost:5432/millesime_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Sécurité
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080"
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Email (optionnel pour le développement)
    SMTP_HOST: str = ""
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instance globale des paramètres
settings = Settings()


# Fonction pour obtenir les paramètres de base de données
def get_database_url() -> str:
    """Retourne l'URL de la base de données"""
    if os.getenv("DATABASE_URL"):
        return os.getenv("DATABASE_URL")
    return settings.DATABASE_URL


# Fonction pour obtenir les paramètres Redis
def get_redis_url() -> str:
    """Retourne l'URL Redis"""
    if os.getenv("REDIS_URL"):
        return os.getenv("REDIS_URL")
    return settings.REDIS_URL
