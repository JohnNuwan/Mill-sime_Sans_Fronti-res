"""
Routeur API principal - Millésime Sans Frontières
Inclusion de tous les sous-routeurs
"""

from fastapi import APIRouter

from app.api.v1.auth import auth_router
from app.api.v1.users import users_router
from app.api.v1.barrels import barrels_router
from app.api.v1.orders import orders_router
from app.api.v1.quotes import quotes_router

# Création du routeur principal
api_router = APIRouter()

# Inclusion des sous-routeurs
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(barrels_router, prefix="/barrels", tags=["Barrels"])
api_router.include_router(orders_router, prefix="/orders", tags=["Orders"])
api_router.include_router(quotes_router, prefix="/quotes", tags=["Quotes"])
