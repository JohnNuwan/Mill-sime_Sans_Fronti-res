"""
Routes d'authentification - Millésime Sans Frontières
Gestion de l'inscription, connexion et tokens JWT
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Any

from app.core.database import get_db
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, UserWithToken
from app.schemas.base import SuccessResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService

# Création du routeur
auth_router = APIRouter()

# Schéma OAuth2 pour la connexion
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")


@auth_router.post("/register", response_model=UserWithToken, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Inscription d'un nouvel utilisateur
    """
    try:
        # Validation des mots de passe
        if user_data.password != user_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Les mots de passe ne correspondent pas"
            )
        
        # Vérification si l'email existe déjà
        user_service = UserService(db)
        if user_service.get_user_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )
        
        # Création de l'utilisateur
        auth_service = AuthService(db)
        user = auth_service.create_user(user_data)
        
        # Génération du token JWT
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id)}
        )
        
        return UserWithToken(
            **user.__dict__,
            access_token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'inscription: {str(e)}"
        )


@auth_router.post("/login", response_model=UserWithToken)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Connexion utilisateur
    """
    try:
        auth_service = AuthService(db)
        user = auth_service.authenticate_user(form_data.username, form_data.password)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compte utilisateur désactivé"
            )
        
        # Génération du token JWT
        access_token = auth_service.create_access_token(
            data={"sub": str(user.id)}
        )
        
        return UserWithToken(
            **user.__dict__,
            access_token=access_token,
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la connexion: {str(e)}"
        )


@auth_router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération des informations de l'utilisateur connecté
    """
    try:
        auth_service = AuthService(db)
        current_user = await auth_service.get_current_user(token, db)
        return current_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des informations: {str(e)}"
        )
