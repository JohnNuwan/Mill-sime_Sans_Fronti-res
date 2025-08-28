"""
Modèles de base de données - Millésime Sans Frontières
Import de tous les modèles SQLAlchemy
"""

from app.core.database import Base
from app.models.user import User
from app.models.address import Address
from app.models.barrel import Barrel
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem

# Export de tous les modèles
__all__ = [
    "Base",
    "User",
    "Address", 
    "Barrel",
    "Order",
    "OrderItem",
    "Quote",
    "QuoteItem"
]
