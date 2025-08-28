"""
Routes Orders - Millésime Sans Frontières
Gestion des commandes des clients
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID

from app.core.database import get_db
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse
from app.schemas.base import PaginatedResponse, PaginationParams
from app.services.order_service import OrderService

# Création du routeur
orders_router = APIRouter()


@orders_router.get("/", response_model=PaginatedResponse[OrderResponse])
async def get_orders(
    pagination: PaginationParams = Depends(),
    user_id: UUID = None,
    status: str = None,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération de la liste des commandes
    """
    try:
        order_service = OrderService(db)
        orders, total = order_service.get_orders_with_filters(
            skip=pagination.offset,
            limit=pagination.size,
            user_id=user_id,
            status=status
        )
        
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResponse(
            items=orders,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des commandes: {str(e)}"
        )


@orders_router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération d'une commande par son ID
    """
    try:
        order_service = OrderService(db)
        order = order_service.get_order_by_id(order_id)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée"
            )
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération de la commande: {str(e)}"
        )


@orders_router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Création d'une nouvelle commande
    """
    try:
        order_service = OrderService(db)
        order = order_service.create_order(order_data)
        return order
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de la commande: {str(e)}"
        )


@orders_router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: UUID,
    new_status: str,
    db: Session = Depends(get_db)
) -> Any:
    """
    Mise à jour du statut d'une commande
    """
    try:
        order_service = OrderService(db)
        order = order_service.update_order_status(order_id, new_status)
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Commande non trouvée"
            )
        
        return order
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du statut: {str(e)}"
        )


@orders_router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération des commandes d'un utilisateur
    """
    try:
        order_service = OrderService(db)
        orders = order_service.get_orders_by_user(user_id)
        return orders
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des commandes: {str(e)}"
        )
