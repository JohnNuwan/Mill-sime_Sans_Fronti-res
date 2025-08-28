"""
Modèle Barrel - Millésime Sans Frontières
Gestion des fûts de vin et spiritueux
"""

from sqlalchemy import Column, String, Numeric, Integer, Text, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from decimal import Decimal

from app.core.database import Base
from app.core.constants import BarrelCondition, WoodType, PreviousContent


class Barrel(Base):
    """Modèle fût"""
    
    __tablename__ = "barrels"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Informations de base
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    # Caractéristiques physiques
    volume_liters = Column(Numeric(10, 2), nullable=False)  # Volume en litres
    weight_kg = Column(Numeric(8, 2), nullable=True)  # Poids en kg
    height_cm = Column(Numeric(6, 2), nullable=True)  # Hauteur en cm
    diameter_cm = Column(Numeric(6, 2), nullable=True)  # Diamètre en cm
    
    # Matériaux et fabrication
    wood_type = Column(Enum(WoodType), nullable=False)
    previous_content = Column(Enum(PreviousContent), nullable=False)
    manufacturing_year = Column(Integer, nullable=True)
    origin_country = Column(String(100), nullable=False, default="France")
    
    # État et condition
    condition = Column(Enum(BarrelCondition), nullable=False, default=BarrelCondition.GOOD)
    age_years = Column(Integer, nullable=True)
    
    # Stock et prix
    stock_quantity = Column(Integer, nullable=False, default=1)
    price = Column(Numeric(10, 2), nullable=False)  # Prix en euros
    currency = Column(String(3), nullable=False, default="EUR")
    
    # Informations commerciales
    sku = Column(String(100), nullable=True, unique=True)
    is_available = Column(String(1), nullable=False, default="Y")  # Y/N pour SQLite
    is_featured = Column(String(1), nullable=False, default="N")  # Y/N pour SQLite
    
    # Images et documents
    image_urls = Column(Text, nullable=True)  # URLs séparées par des virgules
    documents = Column(Text, nullable=True)  # URLs des documents séparées par des virgules
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relations
    order_items = relationship("OrderItem", back_populates="barrel", cascade="all, delete-orphan")
    quote_items = relationship("QuoteItem", back_populates="barrel", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Barrel(id={self.id}, name='{self.name}', volume={self.volume_liters}L, price={self.price}€)>"
    
    @property
    def is_in_stock(self) -> bool:
        """Vérifie si le fût est en stock"""
        return self.stock_quantity > 0 and self.is_available == "Y"
    
    @property
    def is_low_stock(self) -> bool:
        """Vérifie si le stock est faible (moins de 5 unités)"""
        return 0 < self.stock_quantity < 5
    
    @property
    def formatted_price(self) -> str:
        """Retourne le prix formaté"""
        return f"{self.price} {self.currency}"
    
    @property
    def formatted_volume(self) -> str:
        """Retourne le volume formaté"""
        return f"{self.volume_liters}L"
    
    def update_stock(self, quantity: int) -> bool:
        """Met à jour le stock"""
        new_stock = self.stock_quantity + quantity
        if new_stock < 0:
            return False
        self.stock_quantity = new_stock
        return True
    
    def reserve_stock(self, quantity: int) -> bool:
        """Réserve du stock pour une commande"""
        if self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            return True
        return False
    
    def release_stock(self, quantity: int) -> None:
        """Libère du stock réservé"""
        self.stock_quantity += quantity
