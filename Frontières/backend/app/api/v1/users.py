"""
Routes Users - Millésime Sans Frontières
Gestion des comptes utilisateurs
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID

from app.core.database import get_db
from app.schemas.user import UserUpdate, UserResponse
from app.schemas.base import PaginatedResponse, PaginationParams
from app.services.user_service import UserService

# Création du routeur
users_router = APIRouter()


@users_router.get("/", response_model=PaginatedResponse[UserResponse])
async def get_users(
    pagination: PaginationParams = Depends(),
    role: str = None,
    is_active: bool = None,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération de la liste des utilisateurs (Admin uniquement)
    """
    try:
        user_service = UserService(db)
        users = user_service.get_users(
            skip=pagination.offset,
            limit=pagination.size,
            role=role,
            is_active=is_active
        )
        
        total = user_service.get_user_count(role=role)
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResponse(
            items=users,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des utilisateurs: {str(e)}"
        )


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération d'un utilisateur par son ID
    """
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de l'utilisateur: {str(e)}"
        )


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Mise à jour d'un utilisateur
    """
    try:
        user_service = UserService(db)
        user = user_service.update_user(user_id, user_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour de l'utilisateur: {str(e)}"
        )


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Suppression d'un utilisateur (désactivation)
    """
    try:
        user_service = UserService(db)
        success = user_service.delete_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression de l'utilisateur: {str(e)}"
        )


@users_router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Activation d'un utilisateur
    """
    try:
        user_service = UserService(db)
        success = user_service.activate_user(user_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Utilisateur non trouvé"
            )
        
        user = user_service.get_user_by_id(user_id)
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'activation de l'utilisateur: {str(e)}"
        )
