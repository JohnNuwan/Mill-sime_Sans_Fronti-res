"""
Routes Barrels - Millésime Sans Frontières
Gestion du catalogue des fûts
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Any, List, Optional
from uuid import UUID

from app.core.database import get_db
from app.schemas.barrel import (
    BarrelCreate, 
    BarrelUpdate, 
    BarrelResponse, 
    BarrelListResponse,
    BarrelFilter
)
from app.schemas.base import PaginatedResponse, PaginationParams
from app.services.barrel_service import BarrelService

# Création du routeur
barrels_router = APIRouter()


@barrels_router.get("/", response_model=PaginatedResponse[BarrelListResponse])
async def get_barrels(
    pagination: PaginationParams = Depends(),
    filters: BarrelFilter = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération de la liste des fûts avec pagination et filtres
    """
    try:
        barrel_service = BarrelService(db)
        barrels, total = barrel_service.get_barrels_with_filters(
            skip=pagination.offset,
            limit=pagination.size,
            filters=filters
        )
        
        # Calcul du nombre de pages
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResponse(
            items=barrels,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des fûts: {str(e)}"
        )


@barrels_router.get("/{barrel_id}", response_model=BarrelResponse)
async def get_barrel(
    barrel_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération d'un fût par son ID
    """
    try:
        barrel_service = BarrelService(db)
        barrel = barrel_service.get_barrel_by_id(barrel_id)
        
        if not barrel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fût non trouvé"
            )
        
        return barrel
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du fût: {str(e)}"
        )


@barrels_router.post("/", response_model=BarrelResponse, status_code=status.HTTP_201_CREATED)
async def create_barrel(
    barrel_data: BarrelCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Création d'un nouveau fût (Admin uniquement)
    """
    try:
        barrel_service = BarrelService(db)
        barrel = barrel_service.create_barrel(barrel_data)
        return barrel
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du fût: {str(e)}"
        )


@barrels_router.put("/{barrel_id}", response_model=BarrelResponse)
async def update_barrel(
    barrel_id: UUID,
    barrel_data: BarrelUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Mise à jour d'un fût (Admin uniquement)
    """
    try:
        barrel_service = BarrelService(db)
        barrel = barrel_service.update_barrel(barrel_id, barrel_data)
        
        if not barrel:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fût non trouvé"
            )
        
        return barrel
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du fût: {str(e)}"
        )


@barrels_router.delete("/{barrel_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_barrel(
    barrel_id: UUID,
    db: Session = Depends(get_db)
) -> None:
    """
    Suppression d'un fût (Admin uniquement)
    """
    try:
        barrel_service = BarrelService(db)
        success = barrel_service.delete_barrel(barrel_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fût non trouvé"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la suppression du fût: {str(e)}"
        )


@barrels_router.get("/search/", response_model=List[BarrelListResponse])
async def search_barrels(
    q: str = Query(..., min_length=2, description="Terme de recherche"),
    limit: int = Query(20, ge=1, le=100, description="Nombre maximum de résultats"),
    db: Session = Depends(get_db)
) -> Any:
    """
    Recherche de fûts par terme textuel
    """
    try:
        barrel_service = BarrelService(db)
        barrels = barrel_service.search_barrels(q, limit=limit)
        return barrels
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la recherche: {str(e)}"
        )


@barrels_router.get("/categories/origins", response_model=List[str])
async def get_origin_countries(db: Session = Depends(get_db)) -> Any:
    """
    Récupération de la liste des pays d'origine
    """
    try:
        barrel_service = BarrelService(db)
        countries = barrel_service.get_origin_countries()
        return countries
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des pays: {str(e)}"
        )


@barrels_router.get("/categories/wood-types", response_model=List[str])
async def get_wood_types(db: Session = Depends(get_db)) -> Any:
    """
    Récupération de la liste des types de bois
    """
    try:
        barrel_service = BarrelService(db)
        wood_types = barrel_service.get_wood_types()
        return wood_types
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des types de bois: {str(e)}"
        )
