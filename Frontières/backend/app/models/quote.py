"""
Modèle Quote - Millésime Sans Frontières
Gestion des devis
"""

from sqlalchemy import Column, String, Numeric, DateTime, Text, Enum, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from decimal import Decimal

from app.core.database import Base
from app.core.constants import QuoteStatus


class Quote(Base):
    """Modèle devis"""
    
    __tablename__ = "quotes"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Numéro de devis unique
    quote_number = Column(String(50), nullable=False, unique=True, index=True)
    
    # Clé étrangère vers l'utilisateur
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Statut du devis
    status = Column(Enum(QuoteStatus), nullable=False, default=QuoteStatus.DRAFT)
    
    # Informations de livraison
    shipping_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    billing_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    
    # Calculs financiers
    subtotal = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    tax_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    shipping_cost = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    discount_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    total_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    
    # Informations de validité
    valid_until = Column(DateTime(timezone=True), nullable=False)
    is_expired = Column(String(1), nullable=False, default="N")  # Y/N pour SQLite
    
    # Remises et taxes
    discount_percentage = Column(Numeric(5, 2), nullable=False, default=Decimal('0.00'))
    tax_percentage = Column(Numeric(5, 2), nullable=False, default=Decimal('20.00'))
    
    # Informations de livraison
    shipping_method = Column(String(100), nullable=True)
    estimated_delivery_days = Column(Integer, nullable=True)
    
    # Notes et commentaires
    customer_notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    accepted_at = Column(DateTime(timezone=True), nullable=True)
    expired_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    user = relationship("User", back_populates="quotes")
    items = relationship("QuoteItem", back_populates="quote", cascade="all, delete-orphan")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    
    def __repr__(self):
        return f"<Quote(id={self.id}, quote_number='{self.quote_number}', status='{self.status.value}', total={self.total_amount}€)>"
    
    @property
    def item_count(self) -> int:
        """Retourne le nombre d'articles dans le devis"""
        return sum(item.quantity for item in self.items)
    
    @property
    def is_expired_quote(self) -> bool:
        """Vérifie si le devis est expiré"""
        from datetime import datetime
        return datetime.now() > self.valid_until
    
    @property
    def is_convertible_to_order(self) -> bool:
        """Vérifie si le devis peut être converti en commande"""
        return self.status == QuoteStatus.ACCEPTED and not self.is_expired_quote
    
    @property
    def is_editable(self) -> bool:
        """Vérifie si le devis peut être modifié"""
        return self.status == QuoteStatus.DRAFT
    
    def calculate_totals(self) -> None:
        """Calcule tous les montants du devis"""
        self.subtotal = sum(item.total_price for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
    
    def can_update_status(self, new_status: QuoteStatus) -> bool:
        """Vérifie si le changement de statut est autorisé"""
        valid_transitions = {
            QuoteStatus.DRAFT: [QuoteStatus.SENT, QuoteStatus.CANCELLED],
            QuoteStatus.SENT: [QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.EXPIRED],
            QuoteStatus.ACCEPTED: [QuoteStatus.CONVERTED, QuoteStatus.EXPIRED],
            QuoteStatus.REJECTED: [],
            QuoteStatus.EXPIRED: [],
            QuoteStatus.CONVERTED: [],
            QuoteStatus.CANCELLED: []
        }
        return new_status in valid_transitions.get(self.status, [])
    
    def check_expiry(self) -> bool:
        """Vérifie et met à jour l'expiration du devis"""
        if self.is_expired_quote and self.status not in [QuoteStatus.EXPIRED, QuoteStatus.CONVERTED]:
            self.status = QuoteStatus.EXPIRED
            self.is_expired = "Y"
            self.expired_at = func.now()
            return True
        return False
