"""
Modèle QuoteItem - Millésime Sans Frontières
Gestion des articles de devis
"""

from sqlalchemy import Column, String, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from decimal import Decimal

from app.core.database import Base


class QuoteItem(Base):
    """Modèle article de devis"""
    
    __tablename__ = "quote_items"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Clés étrangères
    quote_id = Column(String(36), ForeignKey("quotes.id"), nullable=False)
    barrel_id = Column(String(36), ForeignKey("barrels.id"), nullable=False)
    
    # Quantité et prix
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Remises et taxes
    discount_percentage = Column(Numeric(5, 2), nullable=False, default=Decimal('0.00'))
    tax_percentage = Column(Numeric(5, 2), nullable=False, default=Decimal('20.00'))
    
    # Notes
    notes = Column(String(500), nullable=True)
    
    # Relations
    quote = relationship("Quote", back_populates="items")
    barrel = relationship("Barrel", back_populates="quote_items")
    
    def __repr__(self):
        return f"<QuoteItem(id={self.id}, quantity={self.quantity}, unit_price={self.unit_price}€)>"
    
    def calculate_total_price(self) -> None:
        """Calcule le prix total de l'article"""
        subtotal = self.unit_price * self.quantity
        discount = subtotal * (self.discount_percentage / Decimal('100'))
        subtotal_after_discount = subtotal - discount
        tax = subtotal_after_discount * (self.tax_percentage / Decimal('100'))
        self.total_price = subtotal_after_discount + tax
    
    @property
    def formatted_unit_price(self) -> str:
        """Retourne le prix unitaire formaté"""
        return f"{self.unit_price}€"
    
    @property
    def formatted_total_price(self) -> str:
        """Retourne le prix total formaté"""
        return f"{self.total_price}€"
    
    @property
    def discount_amount(self) -> Decimal:
        """Retourne le montant de la remise"""
        return self.unit_price * self.quantity * (self.discount_percentage / Decimal('100'))
    
    @property
    def tax_amount(self) -> Decimal:
        """Retourne le montant de la taxe"""
        subtotal_after_discount = (self.unit_price * self.quantity) - self.discount_amount
        return subtotal_after_discount * (self.tax_percentage / Decimal('100'))
