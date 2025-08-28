from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from .base import BaseSchema
from .user import UserResponse
from .barrel import BarrelResponse


class OrderItemBase(BaseSchema):
    """Schéma de base pour les éléments de commande"""
    quantity: int = Field(..., gt=0, description="Quantité commandée")
    unit_price: Decimal = Field(..., ge=0, description="Prix unitaire")


class OrderItemCreate(OrderItemBase):
    """Schéma pour créer un élément de commande"""
    barrel_id: str = Field(..., description="ID du tonneau")


class OrderItemUpdate(BaseSchema):
    """Schéma pour mettre à jour un élément de commande"""
    quantity: Optional[int] = Field(None, gt=0, description="Quantité commandée")
    unit_price: Optional[Decimal] = Field(None, ge=0, description="Prix unitaire")


class OrderItemResponse(OrderItemBase):
    """Schéma de réponse pour un élément de commande"""
    id: str
    order_id: str
    barrel_id: str
    barrel: BarrelResponse
    created_at: datetime

    class Config:
        from_attributes = True


class OrderBase(BaseSchema):
    """Schéma de base pour les commandes"""
    shipping_address_id: str = Field(..., description="ID de l'adresse de livraison")
    billing_address_id: str = Field(..., description="ID de l'adresse de facturation")
    notes: Optional[str] = Field(None, max_length=1000, description="Notes de commande")
    shipping_method: Optional[str] = Field(None, max_length=100, description="Méthode de livraison")
    payment_method: Optional[str] = Field(None, max_length=100, description="Méthode de paiement")


class OrderCreate(OrderBase):
    """Schéma pour créer une commande"""
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Éléments de la commande")
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('La commande doit contenir au moins un élément')
        return v


class OrderUpdate(BaseSchema):
    """Schéma pour mettre à jour une commande"""
    notes: Optional[str] = Field(None, max_length=1000, description="Notes de commande")
    shipping_method: Optional[str] = Field(None, max_length=100, description="Méthode de livraison")
    payment_method: Optional[str] = Field(None, max_length=100, description="Méthode de paiement")


class OrderStatusUpdate(BaseSchema):
    """Schéma pour mettre à jour le statut d'une commande"""
    status: str = Field(..., description="Nouveau statut de la commande")
    notes: Optional[str] = Field(None, max_length=1000, description="Notes sur le changement de statut")


class OrderResponse(OrderBase):
    """Schéma de réponse pour une commande"""
    id: str
    user_id: str
    user: UserResponse
    order_number: str
    status: str
    payment_status: str
    subtotal: Decimal
    total_amount: Decimal
    shipping_cost: Optional[Decimal]
    tax_amount: Optional[Decimal]
    discount_amount: Optional[Decimal]
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OrderListResponse(BaseSchema):
    """Schéma de réponse pour la liste des commandes"""
    id: str
    order_number: str
    status: str
    payment_status: str
    total_amount: Decimal
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True


class OrderFilter(BaseSchema):
    """Schéma de filtrage pour les commandes"""
    status: Optional[str] = Field(None, description="Filtrer par statut")
    payment_status: Optional[str] = Field(None, description="Filtrer par statut de paiement")
    user_id: Optional[str] = Field(None, description="Filtrer par utilisateur")
    date_from: Optional[datetime] = Field(None, description="Date de début pour le filtrage")
    date_to: Optional[datetime] = Field(None, description="Date de fin pour le filtrage")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Montant minimum")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Montant maximum")
    search: Optional[str] = Field(None, max_length=100, description="Recherche dans le numéro de commande")


class OrderSummary(BaseSchema):
    """Schéma de résumé pour les statistiques de commandes"""
    total_orders: int
    total_revenue: Decimal
    average_order_value: Decimal
    orders_by_status: dict
    orders_by_month: dict
