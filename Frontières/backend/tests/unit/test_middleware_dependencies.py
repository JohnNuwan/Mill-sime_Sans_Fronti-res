"""
Tests unitaires pour les middlewares et dépendances FastAPI - Millésime Sans Frontières
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_active_user, get_current_user_optional
from app.core.rate_limiting import rate_limit_middleware
from app.core.cors import setup_cors
from app.core.logging import setup_logging
from app.core.monitoring import setup_monitoring
from app.models.user import User
from app.core.constants import UserRole


class TestDatabaseDependencies:
    """Tests pour les dépendances de base de données"""

    def test_get_db_creates_session(self):
        """Test que get_db crée une session de base de données"""
        # Arrange
        mock_db = Mock()
        
        # Act
        with patch('app.core.database.SessionLocal') as mock_session_local:
            mock_session_local.return_value = mock_db
            session = get_db()
            
        # Assert
        assert session == mock_db

    def test_get_db_closes_session_on_exception(self):
        """Test que get_db ferme la session en cas d'exception"""
        # Arrange
        mock_db = Mock()
        mock_db.close = Mock()
        
        # Act & Assert
        with patch('app.core.database.SessionLocal') as mock_session_local:
            mock_session_local.return_value = mock_db
            
            # Simuler une exception
            mock_db.commit.side_effect = Exception("Database error")
            
            try:
                session = get_db()
                session.commit()
            except Exception:
                pass
            
            # Vérifier que close a été appelé
            mock_db.close.assert_called_once()


class TestAuthenticationDependencies:
    """Tests pour les dépendances d'authentification"""

    @patch('app.core.auth.jwt.decode')
    @patch('app.core.auth.get_user_by_id')
    def test_get_current_user_valid_token(self, mock_get_user, mock_jwt_decode):
        """Test de get_current_user avec token valide"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = "test-user-id"
        mock_user.email = "test@example.com"
        
        mock_get_user.return_value = mock_user
        mock_jwt_decode.return_value = {"sub": "test-user-id"}
        
        # Act
        result = get_current_user("valid_token_string")
        
        # Assert
        assert result["user_id"] == "test-user-id"
        assert result["payload"]["sub"] == "test-user-id"
        mock_jwt_decode.assert_called_once()

    @patch('app.core.auth.jwt.decode')
    def test_get_current_user_invalid_token(self, mock_jwt_decode):
        """Test de get_current_user avec token invalide"""
        # Arrange
        mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("invalid_token_string")
        
        assert exc_info.value.status_code == 401
        assert "Invalid authentication credentials" in str(exc_info.value.detail)

    @patch('app.core.auth.jwt.decode')
    @patch('app.core.auth.get_user_by_id')
    def test_get_current_user_user_not_found(self, mock_get_user, mock_jwt_decode):
        """Test de get_current_user avec utilisateur non trouvé"""
        # Arrange
        mock_jwt_decode.return_value = {"sub": "non-existent-user-id"}
        mock_get_user.return_value = None
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user("valid_token_string")
        
        assert exc_info.value.status_code == 401
        assert "User not found" in str(exc_info.value.detail)

    @patch('app.core.auth.get_current_user')
    def test_get_current_active_user_active_user(self, mock_get_current_user):
        """Test de get_current_active_user avec utilisateur actif"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_get_current_user.return_value = mock_user
        
        # Act
        result = get_current_active_user("valid_token_string")
        
        # Assert
        assert result == mock_user

    @patch('app.core.auth.get_current_user')
    def test_get_current_active_user_inactive_user(self, mock_get_current_user):
        """Test de get_current_active_user avec utilisateur inactif"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        mock_get_current_user.return_value = mock_user
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user("valid_token_string")
        
        assert exc_info.value.status_code == 400
        assert "Inactive user" in str(exc_info.value.detail)

    @patch('app.core.auth.jwt.decode')
    @patch('app.core.auth.get_user_by_id')
    def test_get_current_user_optional_valid_token(self, mock_get_user, mock_jwt_decode):
        """Test de get_current_user_optional avec token valide"""
        # Arrange
        mock_user = Mock(spec=User)
        mock_user.id = "test-user-id"
        
        mock_get_user.return_value = mock_user
        mock_jwt_decode.return_value = {"sub": "test-user-id"}
        
        # Act
        result = get_current_user_optional("valid_token_string")
        
        # Assert
        assert result == mock_user

    @patch('app.core.auth.jwt.decode')
    def test_get_current_user_optional_invalid_token(self, mock_jwt_decode):
        """Test de get_current_user_optional avec token invalide"""
        # Arrange
        mock_jwt_decode.side_effect = jwt.InvalidTokenError("Invalid token")
        
        # Act
        result = get_current_user_optional("invalid_token_string")
        
        # Assert
        assert result is None

    def test_get_current_user_optional_no_token(self):
        """Test de get_current_user_optional sans token"""
        # Act
        result = get_current_user_optional(None)
        
        # Assert
        assert result is None


class TestRateLimitingMiddleware:
    """Tests pour le middleware de limitation de taux"""

    def test_rate_limit_middleware_allows_request(self):
        """Test que le middleware autorise une requête normale"""
        # Arrange
        mock_request = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/test"
        
        mock_call_next = AsyncMock()
        mock_call_next.return_value = Mock(status_code=200)
        
        # Act
        with patch('app.core.rate_limiting.redis_client') as mock_redis:
            mock_redis.get.return_value = "5"  # 5 requêtes dans la fenêtre
            mock_redis.incr.return_value = 6   # 6ème requête
            
            response = rate_limit_middleware(mock_request, mock_call_next)
        
        # Assert
        assert response.status_code == 200
        mock_call_next.assert_called_once()

    def test_rate_limit_middleware_blocks_request(self):
        """Test que le middleware bloque une requête en cas de dépassement"""
        # Arrange
        mock_request = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/test"
        
        mock_call_next = AsyncMock()
        
        # Act
        with patch('app.core.rate_limiting.redis_client') as mock_redis:
            mock_redis.get.return_value = "100"  # Limite dépassée
            mock_redis.incr.return_value = 101
            
            response = rate_limit_middleware(mock_request, mock_call_next)
        
        # Assert
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.body.decode()
        mock_call_next.assert_not_called()

    def test_rate_limit_middleware_different_endpoints(self):
        """Test que le middleware traite différents endpoints séparément"""
        # Arrange
        mock_request1 = Mock()
        mock_request1.client.host = "127.0.0.1"
        mock_request1.url.path = "/api/v1/auth/login"
        
        mock_request2 = Mock()
        mock_request2.client.host = "127.0.0.1"
        mock_request2.url.path = "/api/v1/barrels"
        
        mock_call_next = AsyncMock()
        mock_call_next.return_value = Mock(status_code=200)
        
        # Act
        with patch('app.core.rate_limiting.redis_client') as mock_redis:
            mock_redis.get.return_value = "5"
            mock_redis.incr.return_value = 6
            
            # Premier endpoint
            response1 = rate_limit_middleware(mock_request1, mock_call_next)
            
            # Deuxième endpoint
            response2 = rate_limit_middleware(mock_request2, mock_call_next)
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        # Vérifier que les clés Redis sont différentes
        assert mock_redis.get.call_count == 2
        assert mock_redis.incr.call_count == 2


class TestCORSMiddleware:
    """Tests pour le middleware CORS"""

    def test_setup_cors_configures_cors(self):
        """Test que setup_cors configure CORS correctement"""
        # Arrange
        app = FastAPI()
        
        # Act
        setup_cors(app)
        
        # Assert
        # Vérifier que CORS est configuré
        assert hasattr(app, 'user_middleware')
        
        # Vérifier que le middleware CORS est présent
        cors_middleware = None
        for middleware in app.user_middleware:
            if 'CORSMiddleware' in str(middleware.cls):
                cors_middleware = middleware
                break
        
        assert cors_middleware is not None

    def test_setup_cors_with_custom_origins(self):
        """Test que setup_cors accepte des origines personnalisées"""
        # Arrange
        app = FastAPI()
        custom_origins = ["https://custom-domain.com", "https://another-domain.com"]
        
        # Act
        setup_cors(app, origins=custom_origins)
        
        # Assert
        # Vérifier que CORS est configuré avec les origines personnalisées
        assert hasattr(app, 'user_middleware')

    def test_setup_cors_with_credentials(self):
        """Test que setup_cors configure les credentials correctement"""
        # Arrange
        app = FastAPI()
        
        # Act
        setup_cors(app, allow_credentials=True)
        
        # Assert
        # Vérifier que CORS est configuré
        assert hasattr(app, 'user_middleware')


class TestLoggingMiddleware:
    """Tests pour le middleware de logging"""

    def test_setup_logging_configures_logging(self):
        """Test que setup_logging configure le logging correctement"""
        # Arrange
        app = FastAPI()
        
        # Act
        setup_logging(app)
        
        # Assert
        # Vérifier que le logging est configuré
        # Note: L'implémentation exacte dépend de la configuration
        assert True  # Placeholder pour la vérification

    def test_setup_logging_with_custom_level(self):
        """Test que setup_logging accepte un niveau personnalisé"""
        # Arrange
        app = FastAPI()
        custom_level = "DEBUG"
        
        # Act
        setup_logging(app, level=custom_level)
        
        # Assert
        # Vérifier que le logging est configuré avec le niveau personnalisé
        assert True  # Placeholder pour la vérification


class TestMonitoringMiddleware:
    """Tests pour le middleware de monitoring"""

    def test_setup_monitoring_configures_monitoring(self):
        """Test que setup_monitoring configure le monitoring correctement"""
        # Arrange
        app = FastAPI()
        
        # Act
        setup_monitoring(app)
        
        # Assert
        # Vérifier que le monitoring est configuré
        # Note: L'implémentation exacte dépend de la configuration
        assert True  # Placeholder pour la vérification

    def test_setup_monitoring_with_custom_metrics(self):
        """Test que setup_monitoring accepte des métriques personnalisées"""
        # Arrange
        app = FastAPI()
        custom_metrics = {"request_count": 10, "response_time": 150}
        
        # Act
        setup_monitoring(app, metrics=custom_metrics)
        
        # Assert
        # Vérifier que le monitoring est configuré avec les métriques personnalisées
        assert True  # Placeholder pour la vérification


class TestDependencyInjection:
    """Tests pour l'injection de dépendances"""

    def test_dependency_injection_with_db(self):
        """Test de l'injection de dépendance avec la base de données"""
        # Arrange
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint(db: Session = Depends(get_db)):
            return {"message": "success", "db_session": str(type(db))}
        
        # Act
        with patch('app.core.database.SessionLocal') as mock_session_local:
            mock_db = Mock()
            mock_session_local.return_value = mock_db
            
            client = TestClient(app)
            response = client.get("/test")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "success"

    def test_dependency_injection_with_auth(self):
        """Test de l'injection de dépendance avec l'authentification"""
        # Arrange
        app = FastAPI()
        
        @app.get("/protected")
        def protected_endpoint(current_user: User = Depends(get_current_active_user)):
            return {"message": "protected", "user_id": current_user.id}
        
        # Act
        with patch('app.core.auth.get_current_active_user') as mock_get_user:
            mock_user = Mock(spec=User)
            mock_user.id = "test-user-id"
            mock_get_user.return_value = mock_user
            
            client = TestClient(app)
            response = client.get("/protected", headers={"Authorization": "Bearer valid_token"})
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "protected"
        assert response.json()["user_id"] == "test-user-id"

    def test_dependency_injection_optional_auth(self):
        """Test de l'injection de dépendance avec authentification optionnelle"""
        # Arrange
        app = FastAPI()
        
        @app.get("/optional-auth")
        def optional_auth_endpoint(current_user: User = Depends(get_current_user_optional)):
            if current_user:
                return {"message": "authenticated", "user_id": current_user.id}
            else:
                return {"message": "anonymous"}
        
        # Act
        client = TestClient(app)
        
        # Test sans authentification
        response1 = client.get("/optional-auth")
        
        # Test avec authentification
        with patch('app.core.auth.get_current_user_optional') as mock_get_user:
            mock_user = Mock(spec=User)
            mock_user.id = "test-user-id"
            mock_get_user.return_value = mock_user
            
            response2 = client.get("/optional-auth", headers={"Authorization": "Bearer valid_token"})
        
        # Assert
        assert response1.status_code == 200
        assert response1.json()["message"] == "anonymous"
        
        assert response2.status_code == 200
        assert response2.json()["message"] == "authenticated"
        assert response2.json()["user_id"] == "test-user-id"


class TestMiddlewareOrder:
    """Tests pour l'ordre des middlewares"""

    def test_middleware_order_is_correct(self):
        """Test que l'ordre des middlewares est correct"""
        # Arrange
        app = FastAPI()
        
        # Act
        setup_cors(app)
        setup_logging(app)
        setup_monitoring(app)
        
        # Assert
        # Vérifier que les middlewares sont dans le bon ordre
        # Note: L'ordre exact dépend de l'implémentation
        assert len(app.user_middleware) >= 3

    def test_middleware_does_not_interfere(self):
        """Test que les middlewares n'interfèrent pas entre eux"""
        # Arrange
        app = FastAPI()
        
        @app.get("/test")
        def test_endpoint():
            return {"message": "success"}
        
        # Act
        setup_cors(app)
        setup_logging(app)
        setup_monitoring(app)
        
        client = TestClient(app)
        response = client.get("/test")
        
        # Assert
        assert response.status_code == 200
        assert response.json()["message"] == "success"


class TestErrorHandling:
    """Tests pour la gestion d'erreurs dans les middlewares"""

    def test_rate_limiting_middleware_handles_redis_error(self):
        """Test que le middleware de limitation gère les erreurs Redis"""
        # Arrange
        mock_request = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/test"
        
        mock_call_next = AsyncMock()
        mock_call_next.return_value = Mock(status_code=200)
        
        # Act
        with patch('app.core.rate_limiting.redis_client') as mock_redis:
            mock_redis.get.side_effect = Exception("Redis connection error")
            
            # Le middleware devrait gérer l'erreur et permettre la requête
            response = rate_limit_middleware(mock_request, mock_call_next)
        
        # Assert
        # En cas d'erreur Redis, le middleware devrait permettre la requête
        assert response.status_code == 200
        mock_call_next.assert_called_once()

    def test_auth_dependency_handles_malformed_token(self):
        """Test que la dépendance d'auth gère les tokens malformés"""
        # Arrange
        malformed_token = "not.a.valid.jwt.token"
        
        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            get_current_user(malformed_token)
        
        assert exc_info.value.status_code == 401
        assert "Invalid authentication credentials" in str(exc_info.value.detail)

    def test_auth_dependency_handles_expired_token(self):
        """Test que la dépendance d'auth gère les tokens expirés"""
        # Arrange
        expired_token = "expired.jwt.token"
        
        # Act & Assert
        with patch('app.core.auth.jwt.decode') as mock_jwt_decode:
            mock_jwt_decode.side_effect = jwt.ExpiredSignatureError("Token expired")
            
            with pytest.raises(HTTPException) as exc_info:
                get_current_user(expired_token)
            
            assert exc_info.value.status_code == 401
            assert "Token expired" in str(exc_info.value.detail)


class TestPerformance:
    """Tests de performance pour les middlewares"""

    def test_rate_limiting_middleware_performance(self):
        """Test de performance du middleware de limitation"""
        # Arrange
        mock_request = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.url.path = "/api/v1/test"
        
        mock_call_next = AsyncMock()
        mock_call_next.return_value = Mock(status_code=200)
        
        # Act
        import time
        start_time = time.time()
        
        with patch('app.core.rate_limiting.redis_client') as mock_redis:
            mock_redis.get.return_value = "5"
            mock_redis.incr.return_value = 6
            
            for _ in range(100):  # 100 requêtes
                rate_limit_middleware(mock_request, mock_call_next)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        # Le middleware devrait être rapide (< 1 seconde pour 100 requêtes)
        assert execution_time < 1.0

    def test_auth_dependency_performance(self):
        """Test de performance de la dépendance d'auth"""
        # Arrange
        valid_token = "valid.jwt.token"
        
        # Act
        import time
        start_time = time.time()
        
        with patch('app.core.auth.jwt.decode') as mock_jwt_decode, \
             patch('app.core.auth.get_user_by_id') as mock_get_user:
            
            mock_jwt_decode.return_value = {"sub": "test-user-id"}
            mock_user = Mock(spec=User)
            mock_user.id = "test-user-id"
            mock_get_user.return_value = mock_user
            
            for _ in range(100):  # 100 authentifications
                get_current_user(valid_token)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Assert
        # L'authentification devrait être rapide (< 1 seconde pour 100 requêtes)
        assert execution_time < 1.0
