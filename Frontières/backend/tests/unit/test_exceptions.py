"""
Tests unitaires pour les exceptions personnalisées - Millésime Sans Frontières
"""

import pytest
from fastapi import HTTPException

from app.core.exceptions import (
    BaseAppException,
    NotFoundException,
    ValidationException,
    BusinessLogicException,
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    RateLimitException,
    DatabaseException,
    ExternalServiceException,
    handle_app_exception
)


class TestBaseAppException:
    """Tests pour BaseAppException"""

    def test_base_exception_creation(self):
        """Test de création d'exception de base"""
        # Arrange
        message = "Erreur de base"
        status_code = 500
        
        # Act
        exception = BaseAppException(message, status_code)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == status_code
        assert str(exception) == message

    def test_base_exception_default_status_code(self):
        """Test de création d'exception avec code de statut par défaut"""
        # Arrange
        message = "Erreur de base"
        
        # Act
        exception = BaseAppException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 500

    def test_base_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Arrange
        message = "Erreur de base"
        
        # Act
        exception = BaseAppException(message)
        
        # Assert
        assert isinstance(exception, Exception)
        assert isinstance(exception, BaseAppException)


class TestNotFoundException:
    """Tests pour NotFoundException"""

    def test_not_found_exception_creation(self):
        """Test de création d'exception de ressource non trouvée"""
        # Arrange
        message = "Utilisateur non trouvé"
        
        # Act
        exception = NotFoundException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 404

    def test_not_found_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = NotFoundException()
        
        # Assert
        assert exception.message == "Ressource non trouvée"
        assert exception.status_code == 404

    def test_not_found_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = NotFoundException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, NotFoundException)


class TestValidationException:
    """Tests pour ValidationException"""

    def test_validation_exception_creation(self):
        """Test de création d'exception de validation"""
        # Arrange
        message = "Données invalides"
        
        # Act
        exception = ValidationException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 400

    def test_validation_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = ValidationException()
        
        # Assert
        assert exception.message == "Données invalides"
        assert exception.status_code == 400

    def test_validation_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = ValidationException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, ValidationException)


class TestBusinessLogicException:
    """Tests pour BusinessLogicException"""

    def test_business_logic_exception_creation(self):
        """Test de création d'exception de logique métier"""
        # Arrange
        message = "Opération non autorisée"
        
        # Act
        exception = BusinessLogicException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 422

    def test_business_logic_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = BusinessLogicException()
        
        # Assert
        assert exception.message == "Erreur de logique métier"
        assert exception.status_code == 422

    def test_business_logic_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = BusinessLogicException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, BusinessLogicException)


class TestAuthenticationException:
    """Tests pour AuthenticationException"""

    def test_authentication_exception_creation(self):
        """Test de création d'exception d'authentification"""
        # Arrange
        message = "Token invalide"
        
        # Act
        exception = AuthenticationException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 401

    def test_authentication_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = AuthenticationException()
        
        # Assert
        assert exception.message == "Authentification requise"
        assert exception.status_code == 401

    def test_authentication_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = AuthenticationException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, AuthenticationException)


class TestAuthorizationException:
    """Tests pour AuthorizationException"""

    def test_authorization_exception_creation(self):
        """Test de création d'exception d'autorisation"""
        # Arrange
        message = "Accès refusé"
        
        # Act
        exception = AuthorizationException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 403

    def test_authorization_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = AuthorizationException()
        
        # Assert
        assert exception.message == "Accès non autorisé"
        assert exception.status_code == 403

    def test_authorization_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = AuthorizationException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, AuthorizationException)


class TestConflictException:
    """Tests pour ConflictException"""

    def test_conflict_exception_creation(self):
        """Test de création d'exception de conflit"""
        # Arrange
        message = "Ressource déjà existante"
        
        # Act
        exception = ConflictException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 409

    def test_conflict_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = ConflictException()
        
        # Assert
        assert exception.message == "Conflit de données"
        assert exception.status_code == 409

    def test_conflict_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = ConflictException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, ConflictException)


class TestRateLimitException:
    """Tests pour RateLimitException"""

    def test_rate_limit_exception_creation(self):
        """Test de création d'exception de limite de taux"""
        # Arrange
        message = "Trop de requêtes"
        
        # Act
        exception = RateLimitException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 429

    def test_rate_limit_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = RateLimitException()
        
        # Assert
        assert exception.message == "Limite de taux dépassée"
        assert exception.status_code == 429

    def test_rate_limit_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = RateLimitException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, RateLimitException)


class TestDatabaseException:
    """Tests pour DatabaseException"""

    def test_database_exception_creation(self):
        """Test de création d'exception de base de données"""
        # Arrange
        message = "Erreur de connexion"
        
        # Act
        exception = DatabaseException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 500

    def test_database_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = DatabaseException()
        
        # Assert
        assert exception.message == "Erreur de base de données"
        assert exception.status_code == 500

    def test_database_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = DatabaseException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, DatabaseException)


class TestExternalServiceException:
    """Tests pour ExternalServiceException"""

    def test_external_service_exception_creation(self):
        """Test de création d'exception de service externe"""
        # Arrange
        message = "Service de paiement indisponible"
        
        # Act
        exception = ExternalServiceException(message)
        
        # Assert
        assert exception.message == message
        assert exception.status_code == 502

    def test_external_service_exception_default_message(self):
        """Test de création d'exception avec message par défaut"""
        # Act
        exception = ExternalServiceException()
        
        # Assert
        assert exception.message == "Erreur de service externe"
        assert exception.status_code == 502

    def test_external_service_exception_inheritance(self):
        """Test de l'héritage d'exception"""
        # Act
        exception = ExternalServiceException()
        
        # Assert
        assert isinstance(exception, BaseAppException)
        assert isinstance(exception, ExternalServiceException)


class TestHandleAppException:
    """Tests pour la fonction handle_app_exception"""

    def test_handle_not_found_exception(self):
        """Test de gestion d'exception NotFoundException"""
        # Arrange
        exception = NotFoundException("Utilisateur non trouvé")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 404
        assert "detail" in http_exception.detail
        detail = http_exception.detail
        assert detail["error"] == "NotFoundException"
        assert detail["message"] == "Utilisateur non trouvé"
        assert detail["status_code"] == 404

    def test_handle_validation_exception(self):
        """Test de gestion d'exception ValidationException"""
        # Arrange
        exception = ValidationException("Email invalide")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 400
        detail = http_exception.detail
        assert detail["error"] == "ValidationException"
        assert detail["message"] == "Email invalide"
        assert detail["status_code"] == 400

    def test_handle_business_logic_exception(self):
        """Test de gestion d'exception BusinessLogicException"""
        # Arrange
        exception = BusinessLogicException("Opération non autorisée")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 422
        detail = http_exception.detail
        assert detail["error"] == "BusinessLogicException"
        assert detail["message"] == "Opération non autorisée"
        assert detail["status_code"] == 422

    def test_handle_authentication_exception(self):
        """Test de gestion d'exception AuthenticationException"""
        # Arrange
        exception = AuthenticationException("Token expiré")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 401
        detail = http_exception.detail
        assert detail["error"] == "AuthenticationException"
        assert detail["message"] == "Token expiré"
        assert detail["status_code"] == 401

    def test_handle_authorization_exception(self):
        """Test de gestion d'exception AuthorizationException"""
        # Arrange
        exception = AuthorizationException("Permissions insuffisantes")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 403
        detail = http_exception.detail
        assert detail["error"] == "AuthorizationException"
        assert detail["message"] == "Permissions insuffisantes"
        assert detail["status_code"] == 403

    def test_handle_conflict_exception(self):
        """Test de gestion d'exception ConflictException"""
        # Arrange
        exception = ConflictException("Email déjà utilisé")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 409
        detail = http_exception.detail
        assert detail["error"] == "ConflictException"
        assert detail["message"] == "Email déjà utilisé"
        assert detail["status_code"] == 409

    def test_handle_rate_limit_exception(self):
        """Test de gestion d'exception RateLimitException"""
        # Arrange
        exception = RateLimitException("Limite dépassée")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 429
        detail = http_exception.detail
        assert detail["error"] == "RateLimitException"
        assert detail["message"] == "Limite dépassée"
        assert detail["status_code"] == 429

    def test_handle_database_exception(self):
        """Test de gestion d'exception DatabaseException"""
        # Arrange
        exception = DatabaseException("Connexion perdue")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 500
        detail = http_exception.detail
        assert detail["error"] == "DatabaseException"
        assert detail["message"] == "Connexion perdue"
        assert detail["status_code"] == 500

    def test_handle_external_service_exception(self):
        """Test de gestion d'exception ExternalServiceException"""
        # Arrange
        exception = ExternalServiceException("Service indisponible")
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 502
        detail = http_exception.detail
        assert detail["error"] == "ExternalServiceException"
        assert detail["message"] == "Service indisponible"
        assert detail["status_code"] == 502

    def test_handle_base_app_exception(self):
        """Test de gestion d'exception BaseAppException avec code personnalisé"""
        # Arrange
        exception = BaseAppException("Erreur personnalisée", 418)
        
        # Act
        http_exception = handle_app_exception(exception)
        
        # Assert
        assert isinstance(http_exception, HTTPException)
        assert http_exception.status_code == 418
        detail = http_exception.detail
        assert detail["error"] == "BaseAppException"
        assert detail["message"] == "Erreur personnalisée"
        assert detail["status_code"] == 418


class TestExceptionHierarchy:
    """Tests de la hiérarchie des exceptions"""

    def test_exception_hierarchy(self):
        """Test de la hiérarchie complète des exceptions"""
        # Arrange
        exceptions = [
            NotFoundException("Test"),
            ValidationException("Test"),
            BusinessLogicException("Test"),
            AuthenticationException("Test"),
            AuthorizationException("Test"),
            ConflictException("Test"),
            RateLimitException("Test"),
            DatabaseException("Test"),
            ExternalServiceException("Test")
        ]
        
        # Act & Assert
        for exception in exceptions:
            # Toutes doivent hériter de BaseAppException
            assert isinstance(exception, BaseAppException)
            # Toutes doivent avoir un message et un status_code
            assert hasattr(exception, 'message')
            assert hasattr(exception, 'status_code')
            # Le message doit être une chaîne
            assert isinstance(exception.message, str)
            # Le status_code doit être un entier
            assert isinstance(exception.status_code, int)

    def test_exception_status_codes(self):
        """Test des codes de statut HTTP des exceptions"""
        # Arrange
        expected_status_codes = {
            NotFoundException: 404,
            ValidationException: 400,
            BusinessLogicException: 422,
            AuthenticationException: 401,
            AuthorizationException: 403,
            ConflictException: 409,
            RateLimitException: 429,
            DatabaseException: 500,
            ExternalServiceException: 502
        }
        
        # Act & Assert
        for exception_class, expected_status_code in expected_status_codes.items():
            exception = exception_class("Test")
            assert exception.status_code == expected_status_code

    def test_exception_messages(self):
        """Test des messages par défaut des exceptions"""
        # Arrange
        expected_messages = {
            NotFoundException: "Ressource non trouvée",
            ValidationException: "Données invalides",
            BusinessLogicException: "Erreur de logique métier",
            AuthenticationException: "Authentification requise",
            AuthorizationException: "Accès non autorisé",
            ConflictException: "Conflit de données",
            RateLimitException: "Limite de taux dépassée",
            DatabaseException: "Erreur de base de données",
            ExternalServiceException: "Erreur de service externe"
        }
        
        # Act & Assert
        for exception_class, expected_message in expected_messages.items():
            exception = exception_class()
            assert exception.message == expected_message
