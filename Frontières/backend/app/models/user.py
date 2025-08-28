"""
Modèle User - Millésime Sans Frontières
Gestion des utilisateurs (B2C, B2B, administrateurs)
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from app.core.database import Base


class User(Base):
    """Modèle utilisateur"""
    
    __tablename__ = "users"
    
    # Identifiant unique
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Informations de connexion
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Informations personnelles
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    company_name = Column(String(255), nullable=True)  # Pour les clients B2B
    phone_number = Column(String(50), nullable=True)
    
    # Rôle et statut
    role = Column(String(50), nullable=False, default="b2c")  # admin, b2b, b2c
    is_active = Column(Boolean, nullable=False, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relations
    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    quotes = relationship("Quote", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>"
    
    @property
    def full_name(self) -> str:
        """Retourne le nom complet de l'utilisateur"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.email
    
    @property
    def is_b2b(self) -> bool:
        """Vérifie si l'utilisateur est un client B2B"""
        return self.role == "b2b"
    
    @property
    def is_admin(self) -> bool:
        """Vérifie si l'utilisateur est un administrateur"""
        return self.role == "admin"
