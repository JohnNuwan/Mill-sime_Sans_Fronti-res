"""
Rate Limiting - Millésime Sans Frontières
Gestion de la limitation de débit des requêtes
"""

import time
from typing import Dict, Any
from datetime import datetime, timedelta

# Stockage en mémoire des limites (dans un vrai projet, utiliser Redis)
_rate_limit_store: Dict[str, Dict[str, Any]] = {}

def rate_limit_middleware(client_id: str, endpoint: str = "default") -> bool:
    """
    Middleware de limitation de débit
    
    Args:
        client_id: Identifiant du client
        endpoint: Point de terminaison de l'API
        
    Returns:
        bool: True si la requête est autorisée, False sinon
    """
    key = f"{client_id}:{endpoint}"
    current_time = time.time()
    
    # Configuration des limites par endpoint
    limits = {
        "default": {"requests": 100, "window": 3600},  # 100 req/h
        "/api/v1/orders": {"requests": 50, "window": 3600},  # 50 req/h
        "/api/v1/quotes": {"requests": 30, "window": 3600},  # 30 req/h
        "/api/v1/auth": {"requests": 10, "window": 3600},  # 10 req/h
    }
    
    limit_config = limits.get(endpoint, limits["default"])
    max_requests = limit_config["requests"]
    window = limit_config["window"]
    
    # Nettoyer les anciennes entrées
    if key in _rate_limit_store:
        old_entries = []
        for timestamp in _rate_limit_store[key]["timestamps"]:
            if current_time - timestamp > window:
                old_entries.append(timestamp)
        
        for old_timestamp in old_entries:
            _rate_limit_store[key]["timestamps"].remove(old_timestamp)
    
    # Initialiser si nécessaire
    if key not in _rate_limit_store:
        _rate_limit_store[key] = {
            "timestamps": [],
            "blocked_until": 0
        }
    
    # Vérifier si le client est bloqué
    if current_time < _rate_limit_store[key]["blocked_until"]:
        return False
    
    # Ajouter la requête actuelle
    _rate_limit_store[key]["timestamps"].append(current_time)
    
    # Vérifier la limite
    if len(_rate_limit_store[key]["timestamps"]) > max_requests:
        # Bloquer le client pendant 1 heure
        _rate_limit_store[key]["blocked_until"] = current_time + 3600
        return False
    
    return True

def get_rate_limit_info(client_id: str, endpoint: str = "default") -> Dict[str, Any]:
    """
    Récupère les informations de limitation de débit pour un client
    
    Args:
        client_id: Identifiant du client
        endpoint: Point de terminaison de l'API
        
    Returns:
        Dict: Informations sur la limitation de débit
    """
    key = f"{client_id}:{endpoint}"
    
    if key not in _rate_limit_store:
        return {
            "client_id": client_id,
            "endpoint": endpoint,
            "current_requests": 0,
            "limit": 100,
            "remaining": 100,
            "reset_time": None,
            "is_blocked": False
        }
    
    current_time = time.time()
    timestamps = _rate_limit_store[key]["timestamps"]
    blocked_until = _rate_limit_store[key]["blocked_until"]
    
    # Nettoyer les anciennes entrées
    old_entries = []
    for timestamp in timestamps:
        if current_time - timestamp > 3600:  # 1 heure
            old_entries.append(timestamp)
    
    for old_timestamp in old_entries:
        timestamps.remove(old_timestamp)
    
    current_requests = len(timestamps)
    limit = 100  # Limite par défaut
    
    # Ajuster la limite selon l'endpoint
    if endpoint == "/api/v1/orders":
        limit = 50
    elif endpoint == "/api/v1/quotes":
        limit = 30
    elif endpoint == "/api/v1/auth":
        limit = 10
    
    remaining = max(0, limit - current_requests)
    is_blocked = current_time < blocked_until
    
    return {
        "client_id": client_id,
        "endpoint": endpoint,
        "current_requests": current_requests,
        "limit": limit,
        "remaining": remaining,
        "reset_time": current_time + 3600 if current_requests > 0 else None,
        "is_blocked": is_blocked,
        "blocked_until": blocked_until if is_blocked else None
    }

def reset_rate_limit(client_id: str, endpoint: str = "default") -> bool:
    """
    Réinitialise la limitation de débit pour un client
    
    Args:
        client_id: Identifiant du client
        endpoint: Point de terminaison de l'API
        
    Returns:
        bool: True si réinitialisé avec succès
    """
    key = f"{client_id}:{endpoint}"
    
    if key in _rate_limit_store:
        _rate_limit_store[key] = {
            "timestamps": [],
            "blocked_until": 0
        }
        return True
    
    return False

def get_all_rate_limits() -> Dict[str, Dict[str, Any]]:
    """
    Récupère toutes les limitations de débit actives
    
    Returns:
        Dict: Toutes les limitations de débit
    """
    current_time = time.time()
    active_limits = {}
    
    for key, data in _rate_limit_store.items():
        # Nettoyer les anciennes entrées
        old_entries = []
        for timestamp in data["timestamps"]:
            if current_time - timestamp > 3600:
                old_entries.append(timestamp)
        
        for old_timestamp in old_entries:
            data["timestamps"].remove(old_timestamp)
        
        # Ne garder que les limites actives
        if data["timestamps"] or current_time < data["blocked_until"]:
            active_limits[key] = data
    
    return active_limits
