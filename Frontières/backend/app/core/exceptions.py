"""
Exceptions personnalisées - Millésime Sans Frontières
Gestion centralisée des erreurs de l'application
"""

from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Exception de base pour l'application"""
    
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(BaseAppException):
    """Exception levée quand une ressource n'est pas trouvée"""
    
    def __init__(self, message: str = "Ressource non trouvée"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationException(BaseAppException):
    """Exception levée pour les erreurs de validation"""
    
    def __init__(self, message: str = "Données invalides"):
        super().__init__(message, status.HTTP_400_BAD_REQUEST)


class BusinessLogicException(BaseAppException):
    """Exception levée pour les erreurs de logique métier"""
    
    def __init__(self, message: str = "Erreur de logique métier"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


class AuthenticationException(BaseAppException):
    """Exception levée pour les erreurs d'authentification"""
    
    def __init__(self, message: str = "Authentification requise"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationException(BaseAppException):
    """Exception levée pour les erreurs d'autorisation"""
    
    def __init__(self, message: str = "Accès non autorisé"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class ConflictException(BaseAppException):
    """Exception levée pour les conflits de données"""
    
    def __init__(self, message: str = "Conflit de données"):
        super().__init__(message, status.HTTP_409_CONFLICT)


class RateLimitException(BaseAppException):
    """Exception levée pour les limites de taux dépassées"""
    
    def __init__(self, message: str = "Limite de taux dépassée"):
        super().__init__(message, status.HTTP_429_TOO_MANY_REQUESTS)


class DatabaseException(BaseAppException):
    """Exception levée pour les erreurs de base de données"""
    
    def __init__(self, message: str = "Erreur de base de données"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExternalServiceException(BaseAppException):
    """Exception levée pour les erreurs de services externes"""
    
    def __init__(self, message: str = "Erreur de service externe"):
        super().__init__(message, status.HTTP_502_BAD_GATEWAY)


def handle_app_exception(exc: BaseAppException) -> HTTPException:
    """Convertit une exception de l'application en HTTPException FastAPI"""
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "detail": exc.message,
            "status_code": exc.status_code
        }
    )
