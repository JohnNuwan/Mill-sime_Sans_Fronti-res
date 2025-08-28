"""
Service Barrel - Millésime Sans Frontières
Gestion de la logique métier des fûts
"""

from typing import Optional, List, Tuple, Dict, Any, Union
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from uuid import UUID
from decimal import Decimal

from app.models.barrel import Barrel
from app.schemas.barrel import BarrelCreate, BarrelUpdate, BarrelFilter
from app.core.exceptions import NotFoundException, BusinessLogicException


class BarrelService:
    """Service de gestion des fûts"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_barrel_by_id(self, barrel_id: UUID) -> Optional[Barrel]:
        """Récupère un fût par son ID"""
        barrel = self.db.query(Barrel).filter(Barrel.id == barrel_id).first()
        if not barrel:
            raise NotFoundException("Fût non trouvé")
        return barrel
    
    def get_barrels(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Barrel]:
        """Récupère une liste de fûts avec pagination"""
        query = self.db.query(Barrel)
        
        if filters:
            if "origin_country" in filters:
                query = query.filter(Barrel.origin_country.ilike(f"%{filters['origin_country']}%"))
            if "wood_type" in filters:
                query = query.filter(Barrel.wood_type.ilike(f"%{filters['wood_type']}%"))
            if "condition" in filters:
                query = query.filter(Barrel.condition.ilike(f"%{filters['condition']}%"))
            if "min_price" in filters:
                query = query.filter(Barrel.price >= filters["min_price"])
            if "max_price" in filters:
                query = query.filter(Barrel.price <= filters["max_price"])
            if "in_stock" in filters and filters["in_stock"]:
                query = query.filter(Barrel.stock_quantity > 0)
        
        return query.offset(skip).limit(limit).all()
    
    def get_barrels_with_filters(
        self,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[BarrelFilter] = None
    ) -> Tuple[List[Barrel], int]:
        """Récupère des fûts avec filtres et pagination"""
        query = self.db.query(Barrel)
        
        if filters:
            # Filtres de base
            if filters.origin_country:
                query = query.filter(Barrel.origin_country.ilike(f"%{filters.origin_country}%"))
            
            if filters.previous_content:
                query = query.filter(Barrel.previous_content.ilike(f"%{filters.previous_content}%"))
            
            if filters.wood_type:
                query = query.filter(Barrel.wood_type.ilike(f"%{filters.wood_type}%"))
            
            if filters.condition:
                query = query.filter(Barrel.condition.ilike(f"%{filters.condition}%"))
            
            # Filtres de prix
            if filters.min_price is not None:
                query = query.filter(Barrel.price >= filters.min_price)
            
            if filters.max_price is not None:
                query = query.filter(Barrel.price <= filters.max_price)
            
            # Filtres de volume
            if filters.min_volume is not None:
                query = query.filter(Barrel.volume_liters >= filters.min_volume)
            
            if filters.max_volume is not None:
                query = query.filter(Barrel.volume_liters <= filters.max_volume)
            
            # Filtre de stock
            if filters.in_stock:
                query = query.filter(Barrel.stock_quantity > 0)
            
            # Recherche textuelle
            if filters.search:
                search_term = f"%{filters.search}%"
                query = query.filter(
                    or_(
                        Barrel.name.ilike(search_term),
                        Barrel.description.ilike(search_term),
                        Barrel.origin_country.ilike(search_term),
                        Barrel.previous_content.ilike(search_term)
                    )
                )
        
        # Compte total pour la pagination
        total = query.count()
        
        # Application de la pagination
        barrels = query.offset(skip).limit(limit).all()
        
        return barrels, total
    
    def create_barrel(self, barrel_data: Union[BarrelCreate, dict]) -> Barrel:
        """Crée un nouveau fût"""
        if hasattr(barrel_data, 'dict'):
            data = barrel_data.dict()
        else:
            data = barrel_data
            
        db_barrel = Barrel(**data)
        self.db.add(db_barrel)
        self.db.commit()
        self.db.refresh(db_barrel)
        return db_barrel
    
    def update_barrel(self, barrel_id: UUID, barrel_data: Union[BarrelUpdate, dict]) -> Optional[Barrel]:
        """Met à jour un fût"""
        barrel = self.get_barrel_by_id(barrel_id)
        
        # Mise à jour des champs fournis
        if hasattr(barrel_data, 'dict'):
            update_data = barrel_data.dict(exclude_unset=True)
        else:
            update_data = barrel_data
            
        for field, value in update_data.items():
            setattr(barrel, field, value)
        
        self.db.commit()
        self.db.refresh(barrel)
        return barrel
    
    def delete_barrel(self, barrel_id: UUID) -> bool:
        """Supprime un fût"""
        barrel = self.get_barrel_by_id(barrel_id)
        
        # Vérifier si le fût a du stock
        if barrel.stock_quantity > 0:
            raise BusinessLogicException("Impossible de supprimer un fût avec du stock")
        
        self.db.delete(barrel)
        self.db.commit()
        return True
    
    def search_barrels(self, search_term: str, limit: int = 20) -> List[Barrel]:
        """Recherche des fûts par terme textuel"""
        query = self.db.query(Barrel).filter(
            or_(
                Barrel.name.ilike(f"%{search_term}%"),
                Barrel.description.ilike(f"%{search_term}%"),
                Barrel.origin_country.ilike(f"%{search_term}%"),
                Barrel.previous_content.ilike(f"%{search_term}%"),
                Barrel.wood_type.ilike(f"%{search_term}%")
            )
        )
        
        return query.limit(limit).all()
    
    def get_origin_countries(self) -> List[str]:
        """Récupère la liste des pays d'origine"""
        countries = self.db.query(Barrel.origin_country).distinct().all()
        # Retourner les noms complets des pays
        country_mapping = {
            "F": "France",
            "E": "Espagne",
            "I": "Italie",
            "P": "Portugal",
            "D": "Allemagne",
            "US": "États-Unis",
            "CA": "Canada"
        }
        return [country_mapping.get(country[0], country[0]) for country in countries if country[0]]
    
    def get_wood_types(self) -> List[str]:
        """Récupère la liste des types de bois"""
        wood_types = self.db.query(Barrel.wood_type).distinct().all()
        # Retourner les noms complets des types de bois
        wood_mapping = {
            "o": "oak",
            "c": "chestnut",
            "a": "acacia",
            "ch": "cherry",
            "ash": "ash"
        }
        return [wood_mapping.get(wood[0], wood[0]) for wood in wood_types if wood[0]]
    
    def get_available_barrels(self) -> List[Barrel]:
        """Récupère tous les fûts disponibles en stock"""
        return self.db.query(Barrel).filter(Barrel.stock_quantity > 0).all()
    
    def get_low_stock_barrels(self, threshold: int = 5) -> List[Barrel]:
        """Récupère les fûts avec un stock faible"""
        return self.db.query(Barrel).filter(
            and_(Barrel.stock_quantity > 0, Barrel.stock_quantity <= threshold)
        ).all()
    
    def update_stock(self, barrel_id: UUID, quantity: int) -> Barrel:
        """Met à jour le stock d'un fût"""
        barrel = self.get_barrel_by_id(barrel_id)
        
        new_stock = barrel.stock_quantity + quantity
        if new_stock < 0:
            raise BusinessLogicException("Stock insuffisant")
        
        barrel.stock_quantity = new_stock
        self.db.commit()
        return barrel
    
    def decrease_stock(self, barrel_id: UUID, quantity: int) -> bool:
        """Diminue le stock d'un fût"""
        try:
            self.update_stock(barrel_id, -quantity)
            return True
        except BusinessLogicException:
            return False
    
    def get_barrels_by_price_range(self, min_price: float, max_price: float) -> List[Barrel]:
        """Récupère les fûts dans une fourchette de prix"""
        return self.db.query(Barrel).filter(
            and_(Barrel.price >= min_price, Barrel.price <= max_price)
        ).all()
    
    def get_barrels_by_volume_range(self, min_volume: float, max_volume: float) -> List[Barrel]:
        """Récupère les fûts dans une fourchette de volume"""
        return self.db.query(Barrel).filter(
            and_(Barrel.volume_liters >= min_volume, Barrel.volume_liters <= max_volume)
        ).all()
    
    def get_featured_barrels(self, limit: int = 6) -> List[Barrel]:
        """Récupère les fûts mis en avant (ex: meilleur rapport qualité/prix)"""
        # Logique simple : fûts avec le meilleur rapport qualité/prix
        return self.db.query(Barrel).filter(
            Barrel.stock_quantity > 0
        ).order_by(
            func.coalesce(Barrel.stock_quantity, 0).desc()
        ).limit(limit).all()
    
    def get_barrel_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Compte le nombre de fûts avec filtres optionnels"""
        query = self.db.query(Barrel)
        
        if filters:
            if "origin_country" in filters:
                query = query.filter(Barrel.origin_country.ilike(f"%{filters['origin_country']}%"))
            if "wood_type" in filters:
                query = query.filter(Barrel.wood_type.ilike(f"%{filters['wood_type']}%"))
            if "condition" in filters:
                query = query.filter(Barrel.condition.ilike(f"%{filters['condition']}%"))
            if "in_stock" in filters and filters["in_stock"]:
                query = query.filter(Barrel.stock_quantity > 0)
        
        return query.count()
    
    def get_barrels_by_condition(self, condition: str) -> List[Barrel]:
        """Récupère les fûts par condition"""
        return self.db.query(Barrel).filter(Barrel.condition == condition).all()
    
    def get_barrels_by_volume(self, min_volume: float, max_volume: float) -> List[Barrel]:
        """Récupère les fûts par volume"""
        return self.get_barrels_by_volume_range(min_volume, max_volume)
    
    def get_barrel_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques des fûts"""
        total_barrels = self.db.query(Barrel).count()
        available_barrels = self.db.query(Barrel).filter(Barrel.stock_quantity > 0).count()
        total_value = self.db.query(func.sum(Barrel.price * Barrel.stock_quantity)).scalar() or 0
        
        return {
            "total_barrels": total_barrels,
            "available_barrels": available_barrels,
            "total_value": float(total_value)
        }
