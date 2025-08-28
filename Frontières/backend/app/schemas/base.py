"""
Schémas de base - Millésime Sans Frontières
Classes communes pour tous les schémas
"""

from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar, List
from datetime import datetime
from uuid import UUID

# Type générique pour les items
T = TypeVar('T')

class BaseSchema(BaseModel):
    """Schéma de base avec configuration commune"""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }


class BaseResponse(BaseSchema):
    """Schéma de réponse de base"""
    
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None


class PaginationParams(BaseSchema):
    """Paramètres de pagination"""
    
    page: int = Field(default=1, ge=1, description="Numéro de page")
    size: int = Field(default=20, ge=1, le=100, description="Taille de la page")
    
    @property
    def offset(self) -> int:
        """Calcule l'offset pour la requête SQL"""
        return (self.page - 1) * self.size


class PaginatedResponse(BaseSchema, Generic[T]):
    """Réponse paginée"""
    
    items: List[T]
    total: int
    page: int
    size: int
    pages: int
    
    @property
    def has_next(self) -> bool:
        """Vérifie s'il y a une page suivante"""
        return self.page < self.pages
    
    @property
    def has_previous(self) -> bool:
        """Vérifie s'il y a une page précédente"""
        return self.page > 1


class ErrorResponse(BaseSchema):
    """Schéma de réponse d'erreur"""
    
    error: str
    message: str
    details: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class SuccessResponse(BaseSchema):
    """Schéma de réponse de succès"""
    
    message: str
    data: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
