from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from .base import BaseSchema
from .user import UserResponse
from .barrel import BarrelResponse


class QuoteItemBase(BaseSchema):
    """Schéma de base pour les éléments de devis"""
    barrel_id: str = Field(..., description="ID du tonneau")
    quantity: int = Field(..., gt=0, description="Quantité demandée")
    unit_price: Decimal = Field(..., ge=0, description="Prix unitaire proposé")
    description: Optional[str] = Field(None, max_length=500, description="Description de l'élément")


class QuoteItemCreate(QuoteItemBase):
    """Schéma pour créer un élément de devis"""
    pass


class QuoteItemUpdate(BaseSchema):
    """Schéma pour mettre à jour un élément de devis"""
    barrel_id: Optional[str] = Field(None, description="ID du tonneau")
    quantity: Optional[int] = Field(None, gt=0, description="Quantité demandée")
    unit_price: Optional[Decimal] = Field(None, ge=0, description="Prix unitaire proposé")
    description: Optional[str] = Field(None, max_length=500, description="Description de l'élément")


class QuoteItemResponse(QuoteItemBase):
    """Schéma de réponse pour un élément de devis"""
    id: str
    quote_id: str
    barrel: BarrelResponse
    created_at: datetime

    class Config:
        from_attributes = True


class QuoteBase(BaseSchema):
    """Schéma de base pour les devis"""
    title: str = Field(..., max_length=200, description="Titre du devis")
    description: Optional[str] = Field(None, max_length=1000, description="Description générale du devis")
    valid_until: date = Field(..., description="Date de validité du devis")
    terms_conditions: Optional[str] = Field(None, max_length=2000, description="Conditions générales")
    notes: Optional[str] = Field(None, max_length=1000, description="Notes internes")
    shipping_cost: Optional[Decimal] = Field(None, ge=0, description="Coût de livraison")
    tax_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Taux de taxe en pourcentage")
    discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100, description="Remise en pourcentage")


class QuoteCreate(QuoteBase):
    """Schéma pour créer un devis"""
    items: List[QuoteItemCreate] = Field(..., min_items=1, description="Éléments du devis")
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Le devis doit contenir au moins un élément')
        return v
    
    @validator('valid_until')
    def validate_valid_until(cls, v):
        if v <= date.today():
            raise ValueError('La date de validité doit être dans le futur')
        return v


class QuoteUpdate(BaseSchema):
    """Schéma pour mettre à jour un devis"""
    title: Optional[str] = Field(None, max_length=200, description="Titre du devis")
    description: Optional[str] = Field(None, max_length=1000, description="Description générale du devis")
    valid_until: Optional[date] = Field(None, description="Date de validité du devis")
    terms_conditions: Optional[str] = Field(None, max_length=2000, description="Conditions générales")
    notes: Optional[str] = Field(None, max_length=1000, description="Notes internes")
    shipping_cost: Optional[Decimal] = Field(None, ge=0, description="Coût de livraison")
    tax_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="Taux de taxe en pourcentage")
    discount_percentage: Optional[Decimal] = Field(None, ge=0, le=100, description="Remise en pourcentage")


class QuoteStatusUpdate(BaseSchema):
    """Schéma pour mettre à jour le statut d'un devis"""
    status: str = Field(..., description="Nouveau statut du devis")
    notes: Optional[str] = Field(None, max_length=1000, description="Notes sur le changement de statut")


class QuoteSend(BaseSchema):
    """Schéma pour envoyer un devis"""
    email: Optional[str] = Field(None, description="Email alternatif pour l'envoi")
    message: Optional[str] = Field(None, max_length=1000, description="Message personnalisé")


class QuoteResponse(QuoteBase):
    """Schéma de réponse pour un devis"""
    id: str
    user_id: str
    user: UserResponse
    quote_number: str
    status: str
    subtotal: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    total_amount: Decimal
    items: List[QuoteItemResponse]
    converted_to_order_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class QuoteListResponse(BaseSchema):
    """Schéma de réponse pour la liste des devis"""
    id: str
    quote_number: str
    title: str
    status: str
    total_amount: Decimal
    valid_until: date
    created_at: datetime
    user: UserResponse

    class Config:
        from_attributes = True


class QuoteFilter(BaseSchema):
    """Schéma de filtrage pour les devis"""
    status: Optional[str] = Field(None, description="Filtrer par statut")
    user_id: Optional[str] = Field(None, description="Filtrer par utilisateur")
    date_from: Optional[datetime] = Field(None, description="Date de début pour le filtrage")
    date_to: Optional[datetime] = Field(None, description="Date de fin pour le filtrage")
    valid_from: Optional[date] = Field(None, description="Date de validité de début")
    valid_to: Optional[date] = Field(None, description="Date de validité de fin")
    min_amount: Optional[Decimal] = Field(None, ge=0, description="Montant minimum")
    max_amount: Optional[Decimal] = Field(None, ge=0, description="Montant maximum")
    search: Optional[str] = Field(None, max_length=100, description="Recherche dans le titre ou la description")


class QuoteSummary(BaseSchema):
    """Schéma de résumé pour les statistiques de devis"""
    total_quotes: int
    total_value: Decimal
    average_quote_value: Decimal
    quotes_by_status: dict
    quotes_by_month: dict
    conversion_rate: Decimal
