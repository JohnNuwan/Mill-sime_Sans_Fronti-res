"""
Modèle Order - Millésime Sans Frontières
Gestion des commandes
"""

from sqlalchemy import Column, String, Numeric, DateTime, Text, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from decimal import Decimal

from app.core.database import Base
from app.core.constants import OrderStatus, PaymentStatus


class Order(Base):
    """Modèle commande"""
    
    __tablename__ = "orders"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Numéro de commande unique
    order_number = Column(String(50), nullable=False, unique=True, index=True)
    
    # Clé étrangère vers l'utilisateur
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Statuts
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    payment_status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    
    # Informations de livraison
    shipping_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    billing_address_id = Column(String(36), ForeignKey("addresses.id"), nullable=True)
    
    # Calculs financiers
    subtotal = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    tax_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    shipping_cost = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    discount_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    total_amount = Column(Numeric(10, 2), nullable=False, default=Decimal('0.00'))
    
    # Informations de paiement
    payment_method = Column(String(100), nullable=True)
    payment_reference = Column(String(255), nullable=True)
    
    # Informations de livraison
    shipping_method = Column(String(100), nullable=True)
    tracking_number = Column(String(255), nullable=True)
    estimated_delivery = Column(DateTime(timezone=True), nullable=True)
    
    # Notes et commentaires
    customer_notes = Column(Text, nullable=True)
    internal_notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    paid_at = Column(DateTime(timezone=True), nullable=True)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    shipping_address = relationship("Address", foreign_keys=[shipping_address_id])
    billing_address = relationship("Address", foreign_keys=[billing_address_id])
    
    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status.value}', total={self.total_amount}€)>"
    
    @property
    def item_count(self) -> int:
        """Retourne le nombre d'articles dans la commande"""
        return sum(item.quantity for item in self.items)
    
    @property
    def is_paid(self) -> bool:
        """Vérifie si la commande est payée"""
        return self.payment_status == PaymentStatus.COMPLETED
    
    @property
    def is_shipped(self) -> bool:
        """Vérifie si la commande est expédiée"""
        return self.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]
    
    @property
    def is_cancellable(self) -> bool:
        """Vérifie si la commande peut être annulée"""
        return self.status in [OrderStatus.PENDING, OrderStatus.CONFIRMED]
    
    def calculate_totals(self) -> None:
        """Calcule tous les montants de la commande"""
        self.subtotal = sum(item.total_price for item in self.items)
        self.total_amount = self.subtotal + self.tax_amount + self.shipping_cost - self.discount_amount
    
    def can_update_status(self, new_status: OrderStatus) -> bool:
        """Vérifie si le changement de statut est autorisé"""
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
            OrderStatus.CONFIRMED: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.RETURNED],
            OrderStatus.DELIVERED: [OrderStatus.RETURNED],
            OrderStatus.CANCELLED: [],
            OrderStatus.RETURNED: [],
            OrderStatus.REFUNDED: []
        }
        return new_status in valid_transitions.get(self.status, [])
