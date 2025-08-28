"""
Tests d'intégration pour l'API d'authentification - Millésime Sans Frontières
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import timedelta

from app.main import app
from app.core.database import get_db
from app.models.user import User
from app.services.auth_service import AuthService


class TestAuthAPI:
    """Tests d'intégration pour l'API d'authentification"""

    def test_register_user_success(self, client: TestClient, db_session: Session):
        """Test d'inscription d'utilisateur réussie"""
        # Arrange
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
            "first_name": "Nouveau",
            "last_name": "Utilisateur",
            "company_name": "Nouvelle Entreprise",
            "phone_number": "+33123456789",
            "role": "customer"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["company_name"] == user_data["company_name"]
        assert data["phone_number"] == user_data["phone_number"]
        assert data["role"] == user_data["role"]
        assert "id" in data
        assert "password" not in data  # Le mot de passe ne doit pas être retourné

    def test_register_user_duplicate_email(self, client: TestClient, db_session: Session, test_user: User):
        """Test d'inscription avec email en double"""
        # Arrange
        user_data = {
            "email": test_user.email,  # Email déjà existant
            "password": "newpassword123",
            "first_name": "Nouveau",
            "last_name": "Utilisateur",
            "company_name": "Nouvelle Entreprise",
            "phone_number": "+33123456789",
            "role": "customer"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "email" in data["detail"].lower() or "existe" in data["detail"].lower()

    def test_register_user_invalid_data(self, client: TestClient, db_session: Session):
        """Test d'inscription avec données invalides"""
        # Arrange
        user_data = {
            "email": "invalid-email",  # Email invalide
            "password": "123",  # Mot de passe trop court
            "first_name": "",  # Prénom vide
            "last_name": "Utilisateur"
        }
        
        # Act
        response = client.post("/api/v1/auth/register", json=user_data)
        
        # Assert
        assert response.status_code == 422  # Validation error
        data = response.json()
        assert "detail" in data

    def test_login_success(self, client: TestClient, db_session: Session, test_user: User):
        """Test de connexion réussie"""
        # Arrange
        login_data = {
            "username": test_user.email,
            "password": "testpassword123"  # Mot de passe du test_user
        }
        
        # Act
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"
        assert "user" in data
        assert data["user"]["email"] == test_user.email

    def test_login_invalid_credentials(self, client: TestClient, db_session: Session):
        """Test de connexion avec identifiants invalides"""
        # Arrange
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "detail" in data

    def test_login_inactive_user(self, client: TestClient, db_session: Session, test_user: User):
        """Test de connexion d'utilisateur inactif"""
        # Arrange
        test_user.is_active = False
        db_session.commit()
        
        login_data = {
            "username": test_user.email,
            "password": "testpassword123"
        }
        
        # Act
        response = client.post("/api/v1/auth/login", data=login_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "error" in data or "detail" in data

    def test_get_current_user_info_authenticated(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de récupération des informations de l'utilisateur connecté"""
        # Act
        response = client.get("/api/v1/auth/me", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["first_name"] == test_user.first_name
        assert data["last_name"] == test_user.last_name
        assert data["company_name"] == test_user.company_name
        assert data["phone_number"] == test_user.phone_number
        assert data["role"] == test_user.role

    def test_get_current_user_info_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de récupération des informations sans authentification"""
        # Act
        response = client.get("/api/v1/auth/me")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_get_current_user_info_invalid_token(self, client: TestClient, db_session: Session):
        """Test de récupération des informations avec token invalide"""
        # Arrange
        invalid_headers = {"Authorization": "Bearer invalid-token"}
        
        # Act
        response = client.get("/api/v1/auth/me", headers=invalid_headers)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_change_password_success(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de changement de mot de passe réussi"""
        # Arrange
        password_data = {
            "current_password": "testpassword123",
            "new_password": "newpassword456"
        }
        
        # Act
        response = client.post("/api/v1/auth/change-password", json=password_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Vérifier que le nouveau mot de passe fonctionne
        login_data = {
            "username": test_user.email,
            "password": "newpassword456"
        }
        login_response = client.post("/api/v1/auth/login", data=login_data)
        assert login_response.status_code == 200

    def test_change_password_wrong_current_password(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de changement de mot de passe avec mot de passe actuel incorrect"""
        # Arrange
        password_data = {
            "current_password": "wrongpassword",
            "new_password": "newpassword456"
        }
        
        # Act
        response = client.post("/api/v1/auth/change-password", json=password_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data

    def test_change_password_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de changement de mot de passe sans authentification"""
        # Arrange
        password_data = {
            "current_password": "oldpassword",
            "new_password": "newpassword456"
        }
        
        # Act
        response = client.post("/api/v1/auth/change-password", json=password_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_forgot_password_success(self, client: TestClient, db_session: Session, test_user: User):
        """Test de demande de réinitialisation de mot de passe réussie"""
        # Arrange
        forgot_data = {
            "email": test_user.email
        }
        
        # Act
        response = client.post("/api/v1/auth/forgot-password", json=forgot_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_forgot_password_nonexistent_email(self, client: TestClient, db_session: Session):
        """Test de demande de réinitialisation avec email inexistant"""
        # Arrange
        forgot_data = {
            "email": "nonexistent@example.com"
        }
        
        # Act
        response = client.post("/api/v1/auth/forgot-password", json=forgot_data)
        
        # Assert
        # Pour des raisons de sécurité, on retourne toujours un succès
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_reset_password_success(self, client: TestClient, db_session: Session, test_user: User):
        """Test de réinitialisation de mot de passe réussie"""
        # Arrange
        # Générer un token de réinitialisation
        reset_token = AuthService.create_access_token(
            data={"sub": str(test_user.id), "type": "password_reset"},
            expires_delta=timedelta(hours=1)
        )
        
        reset_data = {
            "token": reset_token,
            "new_password": "resetpassword123"
        }
        
        # Act
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        
        # Vérifier que le nouveau mot de passe fonctionne
        login_data = {
            "username": test_user.email,
            "password": "resetpassword123"
        }
        login_response = client.post("/api/v1/auth/login", data=login_data)
        assert login_response.status_code == 200

    def test_reset_password_invalid_token(self, client: TestClient, db_session: Session):
        """Test de réinitialisation avec token invalide"""
        # Arrange
        reset_data = {
            "token": "invalid-token",
            "new_password": "resetpassword123"
        }
        
        # Act
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data

    def test_reset_password_expired_token(self, client: TestClient, db_session: Session, test_user: User):
        """Test de réinitialisation avec token expiré"""
        # Arrange
        # Générer un token expiré
        expired_token = AuthService.create_access_token(
            data={"sub": str(test_user.id), "type": "password_reset"},
            expires_delta=timedelta(seconds=-1)
        )
        
        reset_data = {
            "token": expired_token,
            "new_password": "resetpassword123"
        }
        
        # Act
        response = client.post("/api/v1/auth/reset-password", json=reset_data)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "error" in data or "detail" in data

    def test_token_refresh_success(self, client: TestClient, db_session: Session, test_user: User):
        """Test de rafraîchissement de token réussi"""
        # Arrange
        # Créer un token d'accès
        access_token = AuthService.create_access_token(data={"sub": str(test_user.id)})
        
        refresh_data = {
            "access_token": access_token
        }
        
        # Act
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert data["token_type"] == "bearer"

    def test_token_refresh_invalid_token(self, client: TestClient, db_session: Session):
        """Test de rafraîchissement avec token invalide"""
        # Arrange
        refresh_data = {
            "access_token": "invalid-token"
        }
        
        # Act
        response = client.post("/api/v1/auth/refresh", json=refresh_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_logout_success(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de déconnexion réussie"""
        # Act
        response = client.post("/api/v1/auth/logout", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_logout_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de déconnexion sans authentification"""
        # Act
        response = client.post("/api/v1/auth/logout")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data
