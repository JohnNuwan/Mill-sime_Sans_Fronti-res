"""
Schémas Barrel - Millésime Sans Frontières
Validation des données des fûts
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from uuid import UUID

from app.schemas.base import BaseSchema, BaseResponse


class BarrelBase(BaseSchema):
    """Schéma de base pour les fûts"""
    
    name: str = Field(..., max_length=255, description="Nom du fût")
    origin_country: str = Field(..., max_length=100, description="Pays d'origine")
    previous_content: str = Field(..., max_length=100, description="Contenu précédent")
    volume_liters: Decimal = Field(..., gt=0, description="Volume en litres")
    wood_type: str = Field(..., max_length=100, description="Type de bois")
    condition: str = Field(..., max_length=50, description="État du fût")
    price: Decimal = Field(..., gt=0, description="Prix en euros")
    stock_quantity: int = Field(..., ge=0, description="Quantité en stock")
    description: Optional[str] = Field(None, description="Description détaillée")
    dimensions: Optional[str] = Field(None, max_length=255, description="Dimensions")
    weight_kg: Optional[Decimal] = Field(None, gt=0, description="Poids en kg")
    
    @validator('volume_liters', 'price', 'weight_kg')
    def validate_decimal(cls, v):
        """Valide que les valeurs décimales sont positives"""
        if v is not None and v <= 0:
            raise ValueError('La valeur doit être positive')
        return v
    
    @validator('stock_quantity')
    def validate_stock(cls, v):
        """Valide que le stock est positif"""
        if v < 0:
            raise ValueError('Le stock ne peut pas être négatif')
        return v


class BarrelCreate(BarrelBase):
    """Schéma pour la création d'un fût"""
    
    image_urls: Optional[List[str]] = Field(None, description="URLs des images")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Fût de Château Margaux 2015",
                "origin_country": "France",
                "previous_content": "Bordeaux Rouge",
                "volume_liters": "225.00",
                "wood_type": "Chêne français",
                "condition": "Excellent",
                "price": "1500.00",
                "stock_quantity": 5,
                "description": "Fût de chêne français de première qualité, utilisé pour le vieillissement du Château Margaux 2015",
                "dimensions": "H: 95cm, D: 70cm",
                "weight_kg": "45.50",
                "image_urls": ["https://example.com/barrel1.jpg", "https://example.com/barrel1_detail.jpg"]
            }
        }


class BarrelUpdate(BaseSchema):
    """Schéma pour la mise à jour d'un fût"""
    
    name: Optional[str] = Field(None, max_length=255)
    origin_country: Optional[str] = Field(None, max_length=100)
    previous_content: Optional[str] = Field(None, max_length=100)
    volume_liters: Optional[Decimal] = Field(None, gt=0)
    wood_type: Optional[str] = Field(None, max_length=100)
    condition: Optional[str] = Field(None, max_length=50)
    price: Optional[Decimal] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    dimensions: Optional[str] = Field(None, max_length=255)
    weight_kg: Optional[Decimal] = Field(None, gt=0)
    image_urls: Optional[List[str]] = None


class BarrelResponse(BaseResponse):
    """Schéma de réponse pour un fût"""
    
    name: str
    origin_country: str
    previous_content: str
    volume_liters: Decimal
    wood_type: str
    condition: str
    price: Decimal
    stock_quantity: int
    description: Optional[str]
    dimensions: Optional[str]
    weight_kg: Optional[Decimal]
    image_urls: Optional[List[str]]
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Fût de Château Margaux 2015",
                "origin_country": "France",
                "previous_content": "Bordeaux Rouge",
                "volume_liters": "225.00",
                "wood_type": "Chêne français",
                "condition": "Excellent",
                "price": "1500.00",
                "stock_quantity": 5,
                "description": "Fût de chêne français de première qualité",
                "dimensions": "H: 95cm, D: 70cm",
                "weight_kg": "45.50",
                "image_urls": ["https://example.com/barrel1.jpg"],
                "created_at": "2025-08-27T20:00:00Z",
                "updated_at": "2025-08-27T20:00:00Z"
            }
        }


class BarrelListResponse(BaseSchema):
    """Schéma de réponse pour la liste des fûts"""
    
    id: UUID
    name: str
    origin_country: str
    previous_content: str
    volume_liters: Decimal
    wood_type: str
    condition: str
    price: Decimal
    stock_quantity: int
    main_image: Optional[str] = None
    
    @property
    def is_available(self) -> bool:
        """Vérifie si le fût est disponible"""
        return self.stock_quantity > 0
    
    @property
    def stock_status(self) -> str:
        """Retourne le statut du stock"""
        if self.stock_quantity == 0:
            return "épuisé"
        elif self.stock_quantity <= 2:
            return "stock limité"
        else:
            return "disponible"


class BarrelFilter(BaseSchema):
    """Filtres pour la recherche de fûts"""
    
    origin_country: Optional[str] = Field(None, description="Pays d'origine")
    previous_content: Optional[str] = Field(None, description="Contenu précédent")
    wood_type: Optional[str] = Field(None, description="Type de bois")
    condition: Optional[str] = Field(None, description="État du fût")
    min_price: Optional[Decimal] = Field(None, ge=0, description="Prix minimum")
    max_price: Optional[Decimal] = Field(None, ge=0, description="Prix maximum")
    min_volume: Optional[Decimal] = Field(None, gt=0, description="Volume minimum")
    max_volume: Optional[Decimal] = Field(None, gt=0, description="Volume maximum")
    in_stock: Optional[bool] = Field(None, description="En stock uniquement")
    search: Optional[str] = Field(None, description="Recherche textuelle")
    
    @validator('max_price')
    def validate_max_price(cls, v, values):
        """Valide que le prix maximum est supérieur au prix minimum"""
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v <= values['min_price']:
                raise ValueError('Le prix maximum doit être supérieur au prix minimum')
        return v
    
    @validator('max_volume')
    def validate_max_volume(cls, v, values):
        """Valide que le volume maximum est supérieur au volume minimum"""
        if v is not None and 'min_volume' in values and values['min_volume'] is not None:
            if v <= values['min_volume']:
                raise ValueError('Le volume maximum doit être supérieur au volume minimum')
        return v
