"""
Schémas User - Millésime Sans Frontières
Validation des données utilisateur
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.schemas.base import BaseSchema, BaseResponse


class UserBase(BaseSchema):
    """Schéma de base pour les utilisateurs"""
    
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    first_name: Optional[str] = Field(None, max_length=100, description="Prénom")
    last_name: Optional[str] = Field(None, max_length=100, description="Nom de famille")
    company_name: Optional[str] = Field(None, max_length=255, description="Nom de l'entreprise (B2B)")
    phone_number: Optional[str] = Field(None, max_length=50, description="Numéro de téléphone")
    role: str = Field(default="b2c", description="Rôle de l'utilisateur")


class UserCreate(UserBase):
    """Schéma pour la création d'un utilisateur"""
    
    password: str = Field(..., min_length=8, description="Mot de passe (min 8 caractères)")
    password_confirm: str = Field(..., description="Confirmation du mot de passe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "client@example.com",
                "first_name": "Jean",
                "last_name": "Dupont",
                "company_name": "Cave à Vins SARL",
                "phone_number": "+33 1 23 45 67 89",
                "role": "b2b",
                "password": "motdepasse123",
                "password_confirm": "motdepasse123"
            }
        }


class UserUpdate(BaseSchema):
    """Schéma pour la mise à jour d'un utilisateur"""
    
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company_name: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None


class UserLogin(BaseSchema):
    """Schéma pour la connexion utilisateur"""
    
    email: EmailStr = Field(..., description="Email de l'utilisateur")
    password: str = Field(..., description="Mot de passe")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "client@example.com",
                "password": "motdepasse123"
            }
        }


class UserResponse(BaseResponse):
    """Schéma de réponse pour un utilisateur"""
    
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    company_name: Optional[str]
    phone_number: Optional[str]
    role: str
    is_active: bool
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "email": "client@example.com",
                "first_name": "Jean",
                "last_name": "Dupont",
                "company_name": "Cave à Vins SARL",
                "phone_number": "+33 1 23 45 67 89",
                "role": "b2b",
                "is_active": True,
                "created_at": "2025-08-27T20:00:00Z",
                "updated_at": "2025-08-27T20:00:00Z"
            }
        }


class UserWithToken(UserResponse):
    """Schéma utilisateur avec token JWT"""
    
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfile(BaseSchema):
    """Profil utilisateur complet avec adresses"""
    
    user: UserResponse
    addresses: List["AddressResponse"] = []


class PasswordChange(BaseSchema):
    """Schéma pour le changement de mot de passe"""
    
    current_password: str = Field(..., description="Mot de passe actuel")
    new_password: str = Field(..., min_length=8, description="Nouveau mot de passe")
    new_password_confirm: str = Field(..., description="Confirmation du nouveau mot de passe")


class PasswordReset(BaseSchema):
    """Schéma pour la réinitialisation de mot de passe"""
    
    email: EmailStr = Field(..., description="Email de l'utilisateur")


class PasswordResetConfirm(BaseSchema):
    """Schéma pour confirmer la réinitialisation de mot de passe"""
    
    token: str = Field(..., description="Token de réinitialisation")
    new_password: str = Field(..., min_length=8, description="Nouveau mot de passe")
    new_password_confirm: str = Field(..., description="Confirmation du nouveau mot de passe")
