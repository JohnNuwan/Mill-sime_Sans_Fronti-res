"""
Modèle Address - Millésime Sans Frontières
Gestion des adresses des utilisateurs
"""

from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class Address(Base):
    """Modèle adresse"""
    
    __tablename__ = "addresses"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Clé étrangère vers l'utilisateur
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Informations de l'adresse
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state_province = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), nullable=False, default="France")
    
    # Type d'adresse
    address_type = Column(String(50), nullable=False, default="shipping")  # shipping, billing
    
    # Informations supplémentaires
    phone_number = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relations
    user = relationship("User", back_populates="addresses")
    
    def __repr__(self):
        return f"<Address(id={self.id}, city='{self.city}', country='{self.country}')>"
    
    @property
    def full_address(self) -> str:
        """Retourne l'adresse complète formatée"""
        parts = [self.address_line_1]
        if self.address_line_2:
            parts.append(self.address_line_2)
        parts.extend([self.city, self.state_province, self.postal_code, self.country])
        return ", ".join(filter(None, parts))
