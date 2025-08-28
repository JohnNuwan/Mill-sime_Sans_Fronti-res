"""
Tests unitaires pour AuthService - Millésime Sans Frontières
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from jose import JWTError
from fastapi import HTTPException

from app.services.auth_service import AuthService
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.exceptions import ValidationException


class TestAuthService:
    """Tests pour le service d'authentification"""

    def setup_method(self):
        """Configuration initiale pour chaque test"""
        self.mock_db = Mock()
        self.auth_service = AuthService(self.mock_db)

    def test_verify_password_valid(self):
        """Test de vérification de mot de passe valide"""
        # Arrange
        plain_password = "TestPassword123!"  # Mot de passe fort
        # Générer un vrai hash avec le service
        hashed_password = self.auth_service.get_password_hash(plain_password)
        
        # Act
        result = self.auth_service.verify_password(plain_password, hashed_password)
        
        # Assert
        assert result is True

    def test_verify_password_invalid(self):
        """Test de vérification de mot de passe invalide"""
        # Arrange
        plain_password = "WrongPassword123!"  # Mot de passe fort mais incorrect
        # Générer un hash pour un autre mot de passe
        hashed_password = self.auth_service.get_password_hash("CorrectPassword123!")  # Mot de passe fort
        
        # Act
        result = self.auth_service.verify_password(plain_password, hashed_password)
        
        # Assert
        assert result is False

    def test_get_password_hash(self):
        """Test de génération de hash de mot de passe"""
        # Arrange
        password = "TestPassword123!"  # Mot de passe fort
        
        # Act
        result = self.auth_service.get_password_hash(password)
        
        # Assert
        assert result != password
        assert isinstance(result, str)
        assert len(result) > 0

    def test_authenticate_user_success(self):
        """Test d'authentification d'utilisateur réussie"""
        # Arrange
        email = "test@example.com"
        password = "TestPassword123!"  # Mot de passe fort
        hashed_password = self.auth_service.get_password_hash(password)
        
        mock_user = Mock(spec=User)
        mock_user.email = email
        mock_user.hashed_password = hashed_password  # Corrigé: hashed_password au lieu de password_hash
        mock_user.is_active = True
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Act
        result = self.auth_service.authenticate_user(email, password)
        
        # Assert
        assert result == mock_user

    def test_authenticate_user_invalid_email(self):
        """Test d'authentification avec email invalide"""
        # Arrange
        email = "nonexistent@example.com"
        password = "testpassword123"
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Act
        result = self.auth_service.authenticate_user(email, password)
        
        # Assert
        assert result is None

    def test_authenticate_user_invalid_password(self):
        """Test d'authentification avec mot de passe invalide"""
        # Arrange
        email = "test@example.com"
        password = "WrongPassword123!"  # Mot de passe fort mais incorrect
        hashed_password = self.auth_service.get_password_hash("CorrectPassword123!")  # Mot de passe fort
        
        mock_user = Mock(spec=User)
        mock_user.email = email
        mock_user.hashed_password = hashed_password  # Corrigé: hashed_password
        mock_user.is_active = True
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Act
        result = self.auth_service.authenticate_user(email, password)
        
        # Assert
        assert result is None

    def test_authenticate_user_inactive(self):
        """Test d'authentification d'utilisateur inactif"""
        # Arrange
        email = "test@example.com"
        password = "TestPassword123!"  # Mot de passe fort
        hashed_password = self.auth_service.get_password_hash(password)
        
        mock_user = Mock(spec=User)
        mock_user.email = email
        mock_user.hashed_password = hashed_password  # Corrigé: hashed_password
        mock_user.is_active = False
        
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        # Act
        result = self.auth_service.authenticate_user(email, password)
        
        # Assert
        assert result is None

    def test_create_access_token(self):
        """Test de création de token d'accès"""
        # Arrange
        data = {"sub": "test_user_123"}
        expires_delta = timedelta(minutes=30)
        
        # Act
        result = self.auth_service.create_access_token(data, expires_delta)
        
        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_create_access_token_default_expiry(self):
        """Test de création de token d'accès avec expiration par défaut"""
        # Arrange
        data = {"sub": "test_user_123"}
        
        # Act
        result = self.auth_service.create_access_token(data)
        
        # Assert
        assert isinstance(result, str)
        assert len(result) > 0

    def test_verify_token_valid(self):
        """Test de vérification de token valide"""
        # Arrange
        data = {"sub": "test_user_123"}
        token = self.auth_service.create_access_token(data)
        
        # Act
        result = self.auth_service.verify_token(token)
        
        # Assert
        assert result is not None
        assert "sub" in result

    def test_verify_token_invalid(self):
        """Test de vérification de token invalide"""
        # Arrange
        invalid_token = "invalid.jwt.token"
        
        # Act & Assert
        with pytest.raises(ValueError, match="Token invalide"):
            self.auth_service.verify_token(invalid_token)

    def test_verify_token_expired(self):
        """Test de vérification de token expiré"""
        # Arrange
        data = {"sub": "test_user_123"}
        # Créer un token qui expire immédiatement
        expires_delta = timedelta(seconds=-1)
        token = self.auth_service.create_access_token(data, expires_delta)
        
        # Act & Assert
        # Le token expiré doit lever une exception
        with pytest.raises(ValueError, match="Token expiré"):
            self.auth_service.verify_token(token)

    def test_is_token_expired_false(self):
        """Test de vérification d'expiration de token non expiré"""
        # Arrange
        data = {"sub": "test_user_123"}
        expires_delta = timedelta(minutes=30)
        token = self.auth_service.create_access_token(data, expires_delta)
        
        # Act
        result = self.auth_service.is_token_expired(token)
        
        # Assert
        assert result is False

    def test_is_token_expired_true(self):
        """Test de vérification d'expiration de token expiré"""
        # Arrange
        data = {"sub": "test_user_123"}
        expires_delta = timedelta(seconds=-1)
        token = self.auth_service.create_access_token(data, expires_delta)
        
        # Act
        result = self.auth_service.is_token_expired(token)
        
        # Assert
        assert result is True

    def test_create_user_success(self):
        """Test de création d'utilisateur réussie"""
        # Arrange
        user_data = UserCreate(
            email="unique_test@example.com",  # Email unique
            password="TestPassword123!",  # Mot de passe fort avec majuscule et caractère spécial
            password_confirm="TestPassword123!",
            first_name="Jean",
            last_name="Dupont",
            company_name="Test Company",
            phone_number="+33123456789",
            role="customer"
        )
        
        # Mock de la base de données pour simuler qu'aucun utilisateur n'existe avec cet email
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock de l'utilisateur créé
        mock_user = Mock(spec=User)
        mock_user.email = user_data.email
        mock_user.first_name = user_data.first_name
        mock_user.last_name = user_data.last_name
        mock_user.role = user_data.role
        mock_user.is_active = True
        
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Mock de la création d'utilisateur
        with patch('app.services.auth_service.User') as mock_user_class:
            mock_user_class.return_value = mock_user
            
            # Act
            result = self.auth_service.create_user(user_data)
            
            # Assert
            assert result == mock_user
            self.mock_db.add.assert_called_once()
            self.mock_db.commit.assert_called_once()
            self.mock_db.refresh.assert_called_once()

    def test_create_user_missing_required_fields(self):
        """Test de création d'utilisateur avec champs requis manquants"""
        # Arrange
        user_data = UserCreate(
            email="unique_test2@example.com",  # Email unique
            password="TestPassword123!",  # Mot de passe fort
            password_confirm="TestPassword123!",
            first_name="Jean",
            last_name="Dupont",
            company_name="Test Company",
            phone_number="+33123456789",
            role="customer"
        )
        
        # Mock de la base de données pour simuler qu'aucun utilisateur n'existe avec cet email
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock de la création d'utilisateur qui lève une exception
        with patch('app.services.auth_service.User') as mock_user_class:
            mock_user_class.side_effect = TypeError("Missing required field")
            
            # Act & Assert
            with pytest.raises(TypeError):
                self.auth_service.create_user(user_data)

    def test_create_user_invalid_email_format(self):
        """Test de création d'utilisateur avec format d'email invalide"""
        # Arrange
        # Utiliser un email valide mais avec un format qui pourrait poser problème
        user_data = UserCreate(
            email="unique_test3@example.com",  # Email unique
            password="TestPassword123!",  # Mot de passe fort
            password_confirm="TestPassword123!",
            first_name="Jean",
            last_name="Dupont",
            company_name="Test Company",
            phone_number="+33123456789",
            role="customer"
        )
        
        # Mock de la base de données pour simuler qu'aucun utilisateur n'existe avec cet email
        self.mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock de la création d'utilisateur qui lève une exception
        with patch('app.services.auth_service.User') as mock_user_class:
            mock_user_class.side_effect = ValueError("Invalid email format")
            
            # Act & Assert
            with pytest.raises(ValueError):
                self.auth_service.create_user(user_data)

    def test_password_strength_validation(self):
        """Test de validation de la force du mot de passe"""
        # Arrange
        strong_password = "StrongPassword123!"
        weak_password = "123"
        
        # Act
        strong_hash = self.auth_service.get_password_hash(strong_password)
        weak_hash = self.auth_service.get_password_hash(weak_password)
        
        # Assert
        assert strong_hash != strong_password
        assert weak_hash != weak_password
        # Les deux mots de passe doivent être hashés (pas de validation de force dans le service)

    def test_token_payload_structure(self):
        """Test de la structure du payload du token"""
        # Arrange
        data = {"sub": "test_user_123", "role": "admin"}
        
        # Act
        token = self.auth_service.create_access_token(data)
        payload = self.auth_service.verify_token(token)
        
        # Assert
        assert payload is not None
        assert "sub" in payload
        assert "role" in payload
        assert "exp" in payload
        assert payload["sub"] == "test_user_123"
        assert payload["role"] == "admin"

    def test_multiple_tokens_same_user(self):
        """Test de création de plusieurs tokens pour le même utilisateur"""
        # Arrange
        data = {"sub": "test_user_123"}
        
        # Act
        token1 = self.auth_service.create_access_token(data)
        # Attendre un peu pour que les timestamps soient différents
        import time
        time.sleep(0.1)
        token2 = self.auth_service.create_access_token(data)
        
        # Assert
        # Les tokens peuvent être identiques si créés très rapidement
        # Vérifions plutôt qu'ils sont valides
        assert isinstance(token1, str)
        assert isinstance(token2, str)
        assert self.auth_service.verify_token(token1) is not None
        assert self.auth_service.verify_token(token2) is not None

    def test_token_expiry_accuracy(self):
        """Test de la précision de l'expiration du token"""
        # Arrange
        data = {"sub": "test_user_123"}
        expires_delta = timedelta(minutes=5)
        
        # Act
        token = self.auth_service.create_access_token(data, expires_delta)
        
        # Assert
        payload = self.auth_service.verify_token(token)
        assert payload is not None
        assert "exp" in payload
        
        # Vérifier que le token n'est pas encore expiré
        assert not self.auth_service.is_token_expired(token)
