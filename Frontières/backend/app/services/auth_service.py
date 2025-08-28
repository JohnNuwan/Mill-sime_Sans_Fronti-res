"""
Auth Service - Millésime Sans Frontières
Gestion de l'authentification et des utilisateurs
"""

from typing import Optional, Union, Dict, Any
from datetime import timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.auth import verify_password as auth_verify_password, create_access_token as auth_create_access_token
from app.core.security import validate_password_strength
from app.core.exceptions import ValidationException, AuthenticationException

# Configuration du contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def hash_password(self, password: str) -> str:
        """Hache un mot de passe"""
        return pwd_context.hash(password)

    def get_password_hash(self, password: str) -> str:
        """Alias pour hash_password pour la compatibilité"""
        return self.hash_password(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Vérifie un mot de passe"""
        return auth_verify_password(plain_password, hashed_password)

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            return None
        
        if not user.is_active:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crée un token d'accès JWT"""
        return auth_create_access_token(data, expires_delta)

    def verify_token(self, token: str) -> dict:
        """Vérifie un token JWT"""
        from app.core.auth import verify_token as auth_verify_token
        return auth_verify_token(token)

    def is_token_expired(self, token: str) -> bool:
        """Vérifie si un token est expiré"""
        from app.core.auth import is_token_expired as auth_is_token_expired
        return auth_is_token_expired(token)

    def create_user(self, user_data: Union[UserCreate, Dict]) -> User:
        """Crée un nouvel utilisateur"""
        if isinstance(user_data, dict):
            email = user_data.get("email")
            password = user_data.get("password")
            first_name = user_data.get("first_name", "")
            last_name = user_data.get("last_name", "")
            role = user_data.get("role", "user")
        else:
            email = user_data.email
            password = user_data.password
            first_name = user_data.first_name
            last_name = user_data.last_name
            role = user_data.role

        # Vérifier que l'email n'est pas déjà utilisé
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            raise ValidationException("Cet email est déjà utilisé")

        # Valider la force du mot de passe
        password_validation = validate_password_strength(password)
        if not password_validation["is_valid"]:
            raise ValidationException(f"Mot de passe trop faible: {', '.join(password_validation['errors'])}")

        # Créer l'utilisateur
        hashed_password = self.hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            role=role,
            is_active=True
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def validate_password_strength(self, password: str) -> bool:
        """Valide la force d'un mot de passe"""
        validation = validate_password_strength(password)
        return validation["is_valid"]
