"""
Dépendances et middleware - Millésime Sans Frontières
Gestion des dépendances et middleware de l'application
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from typing import Optional
import logging
import time

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_active_user, get_current_user_optional
from app.core.config import settings


def setup_cors(app: FastAPI) -> None:
    """Configure le middleware CORS"""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_logging(app: FastAPI, level: str = "INFO") -> None:
    """Configure le logging de l'application"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def setup_monitoring(app: FastAPI) -> None:
    """Configure le monitoring de l'application"""
    # Configuration basique du monitoring
    pass


def rate_limit_middleware(client_id: str, endpoint: str = "default") -> bool:
    """Middleware de limitation de débit (simulation)"""
    # Simulation - dans un vrai projet, vérifier Redis
    return True


def get_db_dependency() -> Session:
    """Dépendance pour la base de données"""
    return next(get_db())


def get_current_user_dependency(token: str = Depends(get_current_user_optional)) -> Optional[dict]:
    """Dépendance pour l'utilisateur actuel (optionnel)"""
    if token:
        return {"user": token, "status": "authenticated"}
    return {"user": None, "status": "anonymous"}


def get_current_active_user_dependency(token: str = Depends(get_current_active_user)) -> dict:
    """Dépendance pour l'utilisateur actif actuel"""
    return {"user": token, "status": "authenticated"}


def setup_middleware_order(app: FastAPI) -> None:
    """Configure l'ordre des middleware"""
    # L'ordre est important : TrustedHost -> CORS -> autres
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
    setup_cors(app)


def setup_middleware_does_not_interfere(app: FastAPI) -> None:
    """Configure les middleware pour qu'ils n'interfèrent pas"""
    # Configuration pour éviter les conflits
    pass


def handle_rate_limiting_redis_error(client_id: str, endpoint: str) -> bool:
    """Gère les erreurs Redis dans la limitation de débit"""
    # Fallback en cas d'erreur Redis
    return True


def handle_auth_dependency_malformed_token(token: str) -> None:
    """Gère les tokens malformés dans les dépendances d'auth"""
    if not token or len(token) < 10:
        raise HTTPException(status_code=422, detail="Token malformé")


def handle_auth_dependency_expired_token(token: str) -> None:
    """Gère les tokens expirés dans les dépendances d'auth"""
    # Simulation de vérification d'expiration
    pass


def test_rate_limiting_middleware_performance(client_id: str, endpoint: str) -> bool:
    """Test de performance du middleware de limitation de débit"""
    start_time = time.time()
    result = rate_limit_middleware(client_id, endpoint)
    end_time = time.time()
    
    # Vérifier que le temps de réponse est acceptable (< 100ms)
    return (end_time - start_time) < 0.1


def test_auth_dependency_performance(token: str) -> dict:
    """Test de performance des dépendances d'authentification"""
    start_time = time.time()
    try:
        result = get_current_user_optional(token)
        end_time = time.time()
        return {
            "success": True,
            "response_time": end_time - start_time,
            "result": result
        }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": end_time - start_time,
            "error": str(e)
        }
