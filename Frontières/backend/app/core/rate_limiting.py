"""
Rate Limiting - Millésime Sans Frontières
Gestion de la limitation de débit des requêtes
"""

from typing import Dict, Optional
import time
from collections import defaultdict


class RateLimiter:
    """Limiteur de débit simple en mémoire"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, client_id: str, endpoint: str = "default") -> bool:
        """Vérifie si une requête est autorisée"""
        now = time.time()
        key = f"{client_id}:{endpoint}"
        
        # Nettoyer les anciennes requêtes
        self.requests[key] = [req_time for req_time in self.requests[key] 
                             if now - req_time < self.window_seconds]
        
        # Vérifier la limite
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        # Ajouter la nouvelle requête
        self.requests[key].append(now)
        return True
    
    def get_remaining_requests(self, client_id: str, endpoint: str = "default") -> int:
        """Récupère le nombre de requêtes restantes"""
        now = time.time()
        key = f"{client_id}:{endpoint}"
        
        # Nettoyer les anciennes requêtes
        self.requests[key] = [req_time for req_time in self.requests[key] 
                             if now - req_time < self.window_seconds]
        
        return max(0, self.max_requests - len(self.requests[key]))


# Instance globale du rate limiter
rate_limiter = RateLimiter()


def rate_limit_middleware(client_id: str, endpoint: str = "default") -> bool:
    """Middleware de limitation de débit"""
    return rate_limiter.is_allowed(client_id, endpoint)


def get_rate_limit_info(client_id: str, endpoint: str = "default") -> Dict[str, any]:
    """Récupère les informations de limitation de débit"""
    remaining = rate_limiter.get_remaining_requests(client_id, endpoint)
    return {
        "client_id": client_id,
        "endpoint": endpoint,
        "remaining_requests": remaining,
        "max_requests": rate_limiter.max_requests,
        "window_seconds": rate_limiter.window_seconds
    }


def reset_rate_limit(client_id: str, endpoint: str = "default") -> None:
    """Réinitialise la limitation de débit pour un client"""
    key = f"{client_id}:{endpoint}"
    rate_limiter.requests[key] = []
