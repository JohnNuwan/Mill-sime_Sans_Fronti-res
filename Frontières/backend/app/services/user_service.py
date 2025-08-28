"""
Service utilisateur - Millésime Sans Frontières
Gestion des comptes utilisateurs
"""

from typing import Optional, List, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID

from app.models.user import User
from app.models.address import Address
from app.schemas.user import UserUpdate
from app.core.exceptions import NotFoundException, ValidationException


class UserService:
    """Service de gestion des utilisateurs"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Récupère un utilisateur par son ID"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("Utilisateur non trouvé")
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email"""
        user = self.db.query(User).filter(User.email == email).first()
        if not user:
            raise NotFoundException("Utilisateur non trouvé")
        return user
    
    def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[User]:
        """Récupère une liste d'utilisateurs avec filtres"""
        query = self.db.query(User)
        
        if filters:
            if "role" in filters:
                query = query.filter(User.role == filters["role"])
            if "is_active" in filters:
                query = query.filter(User.is_active == filters["is_active"])
        
        return query.offset(skip).limit(limit).all()
    
    def create_user(self, user_data: dict) -> User:
        """Crée un nouvel utilisateur"""
        # Vérifier si l'email est déjà pris
        if self.is_email_taken(user_data["email"]):
            raise ValidationException("Cet email est déjà utilisé")
        
        # Créer l'utilisateur sans le mot de passe (géré séparément)
        user_data_without_password = {k: v for k, v in user_data.items() if k != "password"}
        db_user = User(**user_data_without_password)
        
        # Hasher le mot de passe si fourni
        if "password" in user_data:
            from app.core.auth import get_password_hash
            db_user.hashed_password = get_password_hash(user_data["password"])
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def update_user(self, user_id: UUID, user_data: Union[UserUpdate, dict]) -> Optional[User]:
        """Met à jour un utilisateur"""
        user = self.get_user_by_id(user_id)
        
        # Mise à jour des champs fournis
        if hasattr(user_data, 'dict'):
            update_data = user_data.dict(exclude_unset=True)
        else:
            update_data = user_data
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: UUID) -> bool:
        """Supprime un utilisateur (désactivation)"""
        user = self.get_user_by_id(user_id)
        
        user.is_active = False
        self.db.commit()
        return True
    
    def activate_user(self, user_id: UUID) -> User:
        """Active un utilisateur"""
        user = self.get_user_by_id(user_id)
        
        user.is_active = True
        self.db.commit()
        return user
    
    def change_user_role(self, user_id: UUID, new_role: str) -> User:
        """Change le rôle d'un utilisateur"""
        user = self.get_user_by_id(user_id)
        
        # Valider le nouveau rôle
        valid_roles = ["admin", "manager", "sales", "customer", "guest"]
        if new_role not in valid_roles:
            raise ValidationException(f"Rôle invalide: {new_role}")
        
        user.role = new_role
        self.db.commit()
        return user
    
    def get_users_by_role(self, role: str) -> List[User]:
        """Récupère tous les utilisateurs d'un rôle spécifique"""
        return self.db.query(User).filter(
            and_(User.role == role, User.is_active == True)
        ).all()
    
    def get_b2b_users(self) -> List[User]:
        """Récupère tous les utilisateurs B2B actifs"""
        return self.get_users_by_role("b2b")
    
    def get_admin_users(self) -> List[User]:
        """Récupère tous les utilisateurs administrateurs actifs"""
        return self.get_users_by_role("admin")
    
    def search_users(
        self,
        search_term: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Recherche des utilisateurs par nom, email ou entreprise"""
        query = self.db.query(User).filter(
            and_(
                User.is_active == True,
                (
                    User.first_name.ilike(f"%{search_term}%") |
                    User.last_name.ilike(f"%{search_term}%") |
                    User.email.ilike(f"%{search_term}%") |
                    User.company_name.ilike(f"%{search_term}%")
                )
            )
        )
        
        return query.offset(skip).limit(limit).all()
    
    def get_user_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Compte le nombre d'utilisateurs (optionnellement par rôle)"""
        query = self.db.query(User).filter(User.is_active == True)
        
        if filters and "role" in filters:
            query = query.filter(User.role == filters["role"])
        
        return query.count()
    
    def is_email_taken(self, email: str, exclude_user_id: Optional[UUID] = None) -> bool:
        """Vérifie si un email est déjà utilisé"""
        query = self.db.query(User).filter(User.email == email)
        
        if exclude_user_id:
            query = query.filter(User.id != exclude_user_id)
        
        return query.first() is not None
    
    def get_user_addresses(self, user_id: UUID) -> List[Address]:
        """Récupère les adresses d'un utilisateur"""
        user = self.get_user_by_id(user_id)
        return self.db.query(Address).filter(Address.user_id == user_id).all()
