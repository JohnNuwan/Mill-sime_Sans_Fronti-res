"""
CORS - Millésime Sans Frontières
Gestion des en-têtes CORS pour l'API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List


def setup_cors(app: FastAPI, 
               origins: List[str] = None,
               allow_credentials: bool = True,
               allow_methods: List[str] = None,
               allow_headers: List[str] = None) -> None:
    """Configure le middleware CORS"""
    
    if origins is None:
        origins = [
            "http://localhost:3000",
            "http://localhost:8000",
            "https://millesime-sans-frontieres.com"
        ]
    
    if allow_methods is None:
        allow_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    
    if allow_headers is None:
        allow_headers = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=allow_credentials,
        allow_methods=allow_methods,
        allow_headers=allow_headers,
    )


def get_cors_headers() -> dict:
    """Récupère les en-têtes CORS par défaut"""
    return {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
        "Access-Control-Allow-Headers": "*",
        "Access-Control-Allow-Credentials": "true"
    }


def validate_origin(origin: str, allowed_origins: List[str]) -> bool:
    """Valide si une origine est autorisée"""
    return origin in allowed_origins
