"""
Order Service - Millésime Sans Frontières
Gestion des commandes et de la logique métier
"""

from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.barrel import Barrel
from app.models.user import User
from app.schemas.order import OrderCreate, OrderUpdate, OrderStatusUpdate
from app.core.exceptions import NotFoundException, ValidationException, BusinessLogicException
from app.core.constants import OrderStatus, PaymentStatus
from app.core.utils import generate_order_number


class OrderService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_order_number(self) -> str:
        """Génère un numéro de commande unique"""
        timestamp = datetime.now().strftime("%Y%m%d")
        count = self.db.query(Order).filter(
            Order.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        return f"ORD-{timestamp}-{count + 1:04d}"

    def _calculate_order_amounts(self, items: List[Dict], discount_percentage: Decimal = Decimal("0"), tax_percentage: Decimal = Decimal("20")) -> Dict[str, Decimal]:
        """Calcule les montants de la commande"""
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
        discount_amount = subtotal * (discount_percentage / Decimal("100"))
        tax_amount = (subtotal - discount_amount) * (tax_percentage / Decimal("100"))
        total = subtotal - discount_amount + tax_amount
        
        return {
            "subtotal": subtotal,
            "discount_amount": discount_amount,
            "tax_amount": tax_amount,
            "total": total
        }

    def _validate_stock_availability(self, items: List[Dict]) -> bool:
        """Valide la disponibilité du stock pour les articles"""
        for item in items:
            barrel = self.db.query(Barrel).filter(Barrel.id == item['barrel_id']).first()
            if not barrel or barrel.stock_quantity < item['quantity']:
                return False
        return True

    def _update_stock_after_order(self, items: List[Dict]) -> None:
        """Met à jour le stock après une commande"""
        for item in items:
            barrel = self.db.query(Barrel).filter(Barrel.id == item['barrel_id']).first()
            if barrel:
                barrel.stock_quantity -= item['quantity']
                self.db.commit()

    def get_order_by_id(self, order_id: str) -> Order:
        """Récupère une commande par son ID"""
        order = self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        ).filter(Order.id == order_id).first()
        
        if not order:
            raise NotFoundException("Commande non trouvée")
        
        return order

    def get_orders(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 100) -> List[Order]:
        """Récupère une liste de commandes avec filtres optionnels"""
        query = self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        )
        
        if filters:
            if filters.get("status"):
                query = query.filter(Order.status == filters["status"])
            if filters.get("user_id"):
                query = query.filter(Order.user_id == filters["user_id"])
            if filters.get("date_from"):
                query = query.filter(Order.created_at >= filters["date_from"])
            if filters.get("date_to"):
                query = query.filter(Order.created_at <= filters["date_to"])
        
        return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def get_orders_no_filters(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Récupère une liste de commandes sans filtres"""
        return self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def get_order_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Compte le nombre total de commandes"""
        query = self.db.query(Order)
        
        if filters:
            if filters.get("status"):
                query = query.filter(Order.status == filters["status"])
            if filters.get("user_id"):
                query = query.filter(Order.user_id == filters["user_id"])
        
        return query.count()

    def create_order(self, order_data: Union[OrderCreate, Dict], user_id: Optional[str] = None) -> Order:
        """Crée une nouvelle commande"""
        if isinstance(order_data, dict):
            # Si c'est un dict, extraire les données
            items_data = order_data.get("items", [])
            discount_percentage = Decimal(str(order_data.get("discount_percentage", 0)))
            tax_percentage = Decimal(str(order_data.get("tax_percentage", 20)))
            notes = order_data.get("notes", "")
        else:
            # Si c'est un Pydantic model
            items_data = order_data.items
            discount_percentage = order_data.discount_percentage
            tax_percentage = order_data.tax_percentage
            notes = order_data.notes or ""
            user_id = user_id or order_data.user_id

        if not items_data:
            raise ValidationException("Une commande doit contenir au moins un article")

        # Valider le stock
        if not self._validate_stock_availability(items_data):
            raise ValidationException("Stock insuffisant pour certains articles")

        # Calculer les montants
        amounts = self._calculate_order_amounts(items_data, discount_percentage, tax_percentage)

        # Créer la commande
        order = Order(
            order_number=self._generate_order_number(),
            user_id=user_id,
            status=OrderStatus.PENDING,
            payment_status=PaymentStatus.PENDING,
            subtotal=amounts["subtotal"],
            discount_percentage=discount_percentage,
            discount_amount=amounts["discount_amount"],
            tax_percentage=tax_percentage,
            tax_amount=amounts["tax_amount"],
            total=amounts["total"],
            notes=notes
        )

        self.db.add(order)
        self.db.flush()

        # Créer les articles de commande
        for item_data in items_data:
            order_item = OrderItem(
                order_id=order.id,
                barrel_id=item_data["barrel_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            self.db.add(order_item)

        # Mettre à jour le stock
        self._update_stock_after_order(items_data)

        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order(self, order_id: str, update_data: Union[OrderUpdate, Dict]) -> Order:
        """Met à jour une commande existante"""
        order = self.get_order_by_id(order_id)
        
        if isinstance(update_data, dict):
            # Si c'est un dict, extraire les données
            for field, value in update_data.items():
                if hasattr(order, field) and value is not None:
                    setattr(order, field, value)
        else:
            # Si c'est un Pydantic model
            for field, value in update_data.dict(exclude_unset=True).items():
                if hasattr(order, field):
                    setattr(order, field, value)

        self.db.commit()
        self.db.refresh(order)
        return order

    def update_order_status(self, order_id: str, status_data: Union[OrderStatusUpdate, str]) -> Order:
        """Met à jour le statut d'une commande"""
        order = self.get_order_by_id(order_id)
        
        if isinstance(status_data, str):
            new_status = status_data
            notes = None
        else:
            new_status = status_data.status
            notes = status_data.notes

        # Vérifier la transition de statut
        valid_transitions = {
            OrderStatus.PENDING: [OrderStatus.PROCESSING, OrderStatus.CANCELLED],
            OrderStatus.PROCESSING: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
            OrderStatus.SHIPPED: [OrderStatus.DELIVERED, OrderStatus.RETURNED],
            OrderStatus.DELIVERED: [OrderStatus.RETURNED],
            OrderStatus.CANCELLED: [],
            OrderStatus.RETURNED: []
        }

        if new_status not in valid_transitions.get(order.status, []):
            raise BusinessLogicException(
                f"Transition de statut invalide: {order.status} -> {new_status}"
            )

        order.status = new_status
        if notes:
            order.notes = notes

        self.db.commit()
        self.db.refresh(order)
        return order

    def delete_order(self, order_id: str) -> bool:
        """Supprime une commande (annulation)"""
        order = self.get_order_by_id(order_id)
        
        # Seules les commandes en attente peuvent être annulées
        if order.status != OrderStatus.PENDING:
            raise BusinessLogicException(
                f"Impossible d'annuler une commande avec le statut: {order.status}"
            )

        # Remettre le stock
        for item in order.items:
            barrel = self.db.query(Barrel).filter(Barrel.id == item.barrel_id).first()
            if barrel:
                barrel.stock_quantity += item.quantity

        self.db.delete(order)
        self.db.commit()
        return True

    def get_orders_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Récupère les commandes d'un utilisateur"""
        return self.db.query(Order).options(
            joinedload(Order.items)
        ).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def get_orders_by_status(self, status: OrderStatus, skip: int = 0, limit: int = 100) -> List[Order]:
        """Récupère les commandes par statut"""
        return self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        ).filter(Order.status == status).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def get_orders_by_date_range(self, start_date: datetime, end_date: datetime, skip: int = 0, limit: int = 100) -> List[Order]:
        """Récupère les commandes dans une plage de dates"""
        return self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        ).filter(
            and_(Order.created_at >= start_date, Order.created_at <= end_date)
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def get_order_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques des commandes"""
        total_orders = self.db.query(Order).count()
        total_revenue = self.db.query(func.sum(Order.total_amount)).scalar() or Decimal("0")
        
        # Compter par statut
        status_counts = self.db.query(Order.status, func.count(Order.id)).group_by(Order.status).all()
        orders_by_status = {status: count for status, count in status_counts}
        
        # Compter par mois (derniers 12 mois)
        twelve_months_ago = datetime.now() - timedelta(days=365)
        monthly_orders = self.db.query(
            func.date_trunc('month', Order.created_at).label('month'),
            func.count(Order.id).label('count')
        ).filter(Order.created_at >= twelve_months_ago).group_by(
            func.date_trunc('month', Order.created_at)
        ).order_by('month').all()
        
        return {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "orders_by_status": orders_by_status,
            "monthly_orders": [{"month": str(m.month), "count": m.count} for m in monthly_orders]
        }

    def search_orders(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Order]:
        """Recherche des commandes par terme"""
        return self.db.query(Order).options(
            joinedload(Order.items),
            joinedload(Order.user)
        ).filter(
            or_(
                Order.order_number.ilike(f"%{search_term}%"),
                Order.customer_notes.ilike(f"%{search_term}%"),
                Order.internal_notes.ilike(f"%{search_term}%")
            )
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    def validate_order_data(self, order_data: Dict[str, Any]) -> bool:
        """Valide les données d'une commande"""
        if not order_data.get("items"):
            raise ValidationException("Une commande doit contenir au moins un article")
        
        for item in order_data["items"]:
            if item.get("quantity", 0) <= 0:
                raise ValidationException("La quantité doit être supérieure à 0")
            if item.get("unit_price", 0) <= 0:
                raise ValidationException("Le prix unitaire doit être supérieur à 0")
        
        return True
