"""
Routes Quotes - Millésime Sans Frontières
Gestion des devis pour les clients B2B
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from uuid import UUID

from app.core.database import get_db
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse
from app.schemas.base import PaginatedResponse, PaginationParams
from app.services.quote_service import QuoteService

# Création du routeur
quotes_router = APIRouter()


@quotes_router.get("/", response_model=PaginatedResponse[QuoteResponse])
async def get_quotes(
    pagination: PaginationParams = Depends(),
    user_id: UUID = None,
    status: str = None,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération de la liste des devis
    """
    try:
        quote_service = QuoteService(db)
        quotes, total = quote_service.get_quotes_with_filters(
            skip=pagination.offset,
            limit=pagination.size,
            user_id=user_id,
            status=status
        )
        
        pages = (total + pagination.size - 1) // pagination.size
        
        return PaginatedResponse(
            items=quotes,
            total=total,
            page=pagination.page,
            size=pagination.size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des devis: {str(e)}"
        )


@quotes_router.get("/{quote_id}", response_model=QuoteResponse)
async def get_quote(
    quote_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération d'un devis par son ID
    """
    try:
        quote_service = QuoteService(db)
        quote = quote_service.get_quote_by_id(quote_id)
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Devis non trouvé"
            )
        
        return quote
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération du devis: {str(e)}"
        )


@quotes_router.post("/", response_model=QuoteResponse, status_code=status.HTTP_201_CREATED)
async def create_quote(
    quote_data: QuoteCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Création d'un nouveau devis
    """
    try:
        quote_service = QuoteService(db)
        quote = quote_service.create_quote(quote_data)
        return quote
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création du devis: {str(e)}"
        )


@quotes_router.put("/{quote_id}", response_model=QuoteResponse)
async def update_quote(
    quote_id: UUID,
    quote_data: QuoteUpdate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Mise à jour d'un devis
    """
    try:
        quote_service = QuoteService(db)
        quote = quote_service.update_quote(quote_id, quote_data)
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Devis non trouvé"
            )
        
        return quote
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la mise à jour du devis: {str(e)}"
        )


@quotes_router.post("/{quote_id}/send", response_model=QuoteResponse)
async def send_quote(
    quote_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Envoi d'un devis au client
    """
    try:
        quote_service = QuoteService(db)
        quote = quote_service.send_quote(quote_id)
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Devis non trouvé"
            )
        
        return quote
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de l'envoi du devis: {str(e)}"
        )


@quotes_router.post("/{quote_id}/convert", response_model=QuoteResponse)
async def convert_quote_to_order(
    quote_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Conversion d'un devis en commande
    """
    try:
        quote_service = QuoteService(db)
        quote = quote_service.convert_to_order(quote_id)
        
        if not quote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Devis non trouvé"
            )
        
        return quote
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la conversion du devis: {str(e)}"
        )


@quotes_router.get("/user/{user_id}", response_model=List[QuoteResponse])
async def get_user_quotes(
    user_id: UUID,
    db: Session = Depends(get_db)
) -> Any:
    """
    Récupération des devis d'un utilisateur
    """
    try:
        quote_service = QuoteService(db)
        quotes = quote_service.get_quotes_by_user(user_id)
        return quotes
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la récupération des devis: {str(e)}"
        )
