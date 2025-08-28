"""
Quote Service - Millésime Sans Frontières
Gestion des devis et de la logique métier
"""

from typing import List, Optional, Dict, Any, Union
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func

from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.barrel import Barrel
from app.models.user import User
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteStatusUpdate
from app.core.exceptions import NotFoundException, ValidationException, BusinessLogicException
from app.core.constants import QuoteStatus
from app.core.utils import generate_quote_number


class QuoteService:
    def __init__(self, db: Session):
        self.db = db

    def _generate_quote_number(self) -> str:
        """Génère un numéro de devis unique"""
        timestamp = datetime.now().strftime("%Y%m%d")
        count = self.db.query(Quote).filter(
            Quote.created_at >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        return f"QUO-{timestamp}-{count + 1:04d}"

    def _calculate_quote_amounts(self, items: List[Dict], discount_percentage: Decimal = Decimal("0"), tax_percentage: Decimal = Decimal("20")) -> Dict[str, Decimal]:
        """Calcule les montants du devis"""
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

    def _validate_quote_items(self, items: List[Dict]) -> bool:
        """Valide les articles du devis et vérifie le stock"""
        if not items:
            return False
        
        for item in items:
            barrel = self.db.query(Barrel).filter(Barrel.id == item['barrel_id']).first()
            if not barrel:
                return False
            
            # Vérifier que le stock est suffisant
            if barrel.stock_quantity < item['quantity']:
                raise BusinessLogicException(f"Stock insuffisant pour {barrel.name}")
        
        return True

    def get_quote_by_id(self, quote_id: str) -> Quote:
        """Récupère un devis par son ID"""
        quote = self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        ).filter(Quote.id == quote_id).first()
        
        if not quote:
            raise NotFoundException("Devis non trouvé")
        
        return quote

    def get_quotes(self, filters: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère une liste de devis avec filtres optionnels"""
        query = self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        )
        
        if filters:
            if filters.get("status"):
                query = query.filter(Quote.status == filters["status"])
            if filters.get("user_id"):
                query = query.filter(Quote.user_id == filters["user_id"])
            if filters.get("date_from"):
                query = query.filter(Quote.created_at >= filters["date_from"])
            if filters.get("date_to"):
                query = query.filter(Quote.created_at <= filters["date_to"])
        
        return query.order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def get_quotes_no_filters(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère une liste de devis sans filtres"""
        return self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        ).order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def get_quote_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Compte le nombre total de devis"""
        query = self.db.query(Quote)
        
        if filters:
            if filters.get("status"):
                query = query.filter(Quote.status == filters["status"])
            if filters.get("user_id"):
                query = query.filter(Quote.user_id == filters["user_id"])
        
        return query.count()

    def get_user_quotes(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère les devis d'un utilisateur"""
        return self.db.query(Quote).options(
            joinedload(Quote.items)
        ).filter(Quote.user_id == user_id).order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def create_quote(self, quote_data: Union[QuoteCreate, Dict], user_id: Optional[str] = None) -> Quote:
        """Crée un nouveau devis"""
        if isinstance(quote_data, dict):
            # Si c'est un dict, extraire les données
            items_data = quote_data.get("items", [])
            discount_percentage = Decimal(str(quote_data.get("discount_percentage", 0)))
            tax_percentage = Decimal(str(quote_data.get("tax_percentage", 20)))
            customer_notes = quote_data.get("customer_notes", "")
            valid_until = quote_data.get("valid_until")
        else:
            # Si c'est un Pydantic model
            items_data = quote_data.items
            discount_percentage = quote_data.discount_percentage
            tax_percentage = quote_data.tax_percentage
            customer_notes = quote_data.customer_notes or ""
            valid_until = quote_data.valid_until
            user_id = user_id or quote_data.user_id

        if not items_data:
            raise ValidationException("Un devis doit contenir au moins un article")

        # Valider les articles
        if not self._validate_quote_items(items_data):
            raise ValidationException("Articles de devis invalides")

        # Valider la date de validité
        if valid_until and valid_until <= datetime.now():
            raise ValidationException("La date de validité doit être dans le futur")

        # Calculer les montants
        amounts = self._calculate_quote_amounts(items_data, discount_percentage, tax_percentage)

        # Créer le devis
        quote = Quote(
            quote_number=self._generate_quote_number(),
            user_id=user_id,
            status=QuoteStatus.DRAFT,
            subtotal=amounts["subtotal"],
            discount_percentage=discount_percentage,
            discount_amount=amounts["discount_amount"],
            tax_percentage=tax_percentage,
            tax_amount=amounts["tax_amount"],
            total=amounts["total"],
            customer_notes=customer_notes,
            valid_until=valid_until or (datetime.now() + timedelta(days=30))
        )

        self.db.add(quote)
        self.db.flush()

        # Créer les articles de devis
        for item_data in items_data:
            quote_item = QuoteItem(
                quote_id=quote.id,
                barrel_id=item_data["barrel_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                total_price=item_data["quantity"] * item_data["unit_price"]
            )
            self.db.add(quote_item)

        self.db.commit()
        self.db.refresh(quote)
        return quote

    def update_quote(self, quote_id: str, update_data: Union[QuoteUpdate, Dict]) -> Quote:
        """Met à jour un devis existant"""
        quote = self.get_quote_by_id(quote_id)
        
        # Seuls les devis en brouillon peuvent être modifiés
        if quote.status != QuoteStatus.DRAFT:
            raise BusinessLogicException(
                f"Impossible de modifier un devis avec le statut: {quote.status}"
            )

        if isinstance(update_data, dict):
            # Si c'est un dict, extraire les données
            for field, value in update_data.items():
                if hasattr(quote, field) and value is not None:
                    setattr(quote, field, value)
        else:
            # Si c'est un Pydantic model
            for field, value in update_data.dict(exclude_unset=True).items():
                if hasattr(quote, field):
                    setattr(quote, field, value)

        # Recalculer les montants si les articles ont changé
        if update_data.get("items"):
            amounts = self._calculate_quote_amounts(
                update_data["items"], 
                quote.discount_percentage, 
                quote.tax_percentage
            )
            quote.subtotal = amounts["subtotal"]
            quote.discount_amount = amounts["discount_amount"]
            quote.tax_amount = amounts["tax_amount"]
            quote.total = amounts["total"]

        self.db.commit()
        self.db.refresh(quote)
        return quote

    def update_quote_status(self, quote_id: str, status_data: Union[QuoteStatusUpdate, str]) -> Quote:
        """Met à jour le statut d'un devis"""
        quote = self.get_quote_by_id(quote_id)
        
        if isinstance(status_data, str):
            new_status = status_data
            customer_notes = None
        else:
            new_status = status_data.status
            customer_notes = status_data.customer_notes

        # Vérifier la transition de statut
        valid_transitions = {
            QuoteStatus.DRAFT: [QuoteStatus.SENT, QuoteStatus.CANCELLED],
            QuoteStatus.SENT: [QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.EXPIRED],
            QuoteStatus.ACCEPTED: [QuoteStatus.CONVERTED],
            QuoteStatus.REJECTED: [],
            QuoteStatus.EXPIRED: [],
            QuoteStatus.CONVERTED: [],
            QuoteStatus.CANCELLED: []
        }

        if new_status not in valid_transitions.get(quote.status, []):
            raise BusinessLogicException(
                f"Transition de statut invalide: {quote.status} -> {new_status}"
            )

        quote.status = new_status
        if customer_notes:
            quote.customer_notes = customer_notes

        self.db.commit()
        self.db.refresh(quote)
        return quote

    def send_quote(self, quote_id: str, send_data: Union[Dict, None] = None) -> Quote:
        """Envoie un devis au client"""
        quote = self.get_quote_by_id(quote_id)
        
        # Seuls les devis en brouillon peuvent être envoyés
        if quote.status != QuoteStatus.DRAFT:
            raise BusinessLogicException(f"Impossible d'envoyer un devis avec le statut: {quote.status}")

        quote.status = QuoteStatus.SENT
        quote.sent_at = datetime.now()

        self.db.commit()
        self.db.refresh(quote)
        return quote

    def convert_quote_to_order(self, quote_id: str) -> str:
        """Convertit un devis en commande"""
        quote = self.get_quote_by_id(quote_id)
        
        # Seuls les devis acceptés peuvent être convertis
        if quote.status != QuoteStatus.ACCEPTED:
            raise BusinessLogicException(f"Impossible de convertir un devis avec le statut: {quote.status}")

        # Créer la commande à partir du devis
        # Cette logique serait implémentée dans le service de commande
        # Pour l'instant, retourner un message de succès
        return "Devis converti en commande avec succès"

    def delete_quote(self, quote_id: str) -> bool:
        """Supprime un devis"""
        quote = self.get_quote_by_id(quote_id)
        
        # Seuls les devis en brouillon peuvent être supprimés
        if quote.status != QuoteStatus.DRAFT:
            raise BusinessLogicException(
                f"Impossible de supprimer un devis avec le statut: {quote.status}"
            )

        self.db.delete(quote)
        self.db.commit()
        return True

    def get_quote_statistics(self) -> Dict[str, Any]:
        """Récupère les statistiques des devis"""
        total_quotes = self.db.query(Quote).count()
        total_value = self.db.query(func.sum(Quote.total_amount)).scalar() or Decimal("0")
        
        # Compter par statut
        status_counts = self.db.query(Quote.status, func.count(Quote.id)).group_by(Quote.status).all()
        quotes_by_status = {status: count for status, count in status_counts}
        
        # Compter par mois (derniers 12 mois)
        twelve_months_ago = datetime.now() - timedelta(days=365)
        monthly_quotes = self.db.query(
            func.date_trunc('month', Quote.created_at).label('month'),
            func.count(Quote.id).label('count')
        ).filter(Quote.created_at >= twelve_months_ago).group_by(
            func.date_trunc('month', Quote.created_at)
        ).order_by('month').all()
        
        return {
            "total_quotes": total_quotes,
            "total_value": total_value,
            "quotes_by_status": quotes_by_status,
            "monthly_quotes": [{"month": str(m.month), "count": m.count} for m in monthly_quotes]
        }

    def search_quotes(self, search_term: str, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Recherche des devis par terme"""
        return self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        ).filter(
            or_(
                Quote.quote_number.ilike(f"%{search_term}%"),
                Quote.customer_notes.ilike(f"%{search_term}%"),
                Quote.internal_notes.ilike(f"%{search_term}%")
            )
        ).order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def get_quotes_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère les devis d'un utilisateur"""
        return self.db.query(Quote).options(
            joinedload(Quote.items)
        ).filter(Quote.user_id == user_id).order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def get_quotes_by_status(self, status: QuoteStatus, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère les devis par statut"""
        return self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        ).filter(Quote.status == status).order_by(Quote.created_at.desc()).offset(skip).limit(limit).all()

    def get_expired_quotes(self, skip: int = 0, limit: int = 100) -> List[Quote]:
        """Récupère les devis expirés"""
        return self.db.query(Quote).options(
            joinedload(Quote.items),
            joinedload(Quote.user)
        ).filter(
            and_(Quote.valid_until < datetime.now(), Quote.status == QuoteStatus.SENT)
        ).order_by(Quote.valid_until.desc()).offset(skip).limit(limit).all()

    def check_expired_quotes(self) -> List[Quote]:
        """Vérifie et marque les devis expirés"""
        expired_quotes = self.db.query(Quote).filter(
            and_(Quote.valid_until < datetime.now(), Quote.status == QuoteStatus.SENT)
        ).all()
        
        for quote in expired_quotes:
            quote.status = QuoteStatus.EXPIRED
        
        self.db.commit()
        return expired_quotes

    def validate_quote_data(self, quote_data: Dict[str, Any]) -> bool:
        """Valide les données d'un devis"""
        if not quote_data.get("items"):
            raise ValidationException("Un devis doit contenir au moins un article")
        
        for item in quote_data["items"]:
            if item.get("quantity", 0) <= 0:
                raise ValidationException("La quantité doit être supérieure à 0")
            if item.get("unit_price", 0) <= 0:
                raise ValidationException("Le prix unitaire doit être supérieur à 0")
        
        return True

    def quote_status_transitions_invalid(self) -> Dict[str, List[str]]:
        """Retourne les transitions de statut invalides"""
        return {
            QuoteStatus.DRAFT: [QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.EXPIRED, QuoteStatus.CONVERTED],
            QuoteStatus.SENT: [QuoteStatus.DRAFT, QuoteStatus.CONVERTED],
            QuoteStatus.ACCEPTED: [QuoteStatus.DRAFT, QuoteStatus.SENT, QuoteStatus.REJECTED, QuoteStatus.EXPIRED],
            QuoteStatus.REJECTED: [QuoteStatus.DRAFT, QuoteStatus.SENT, QuoteStatus.ACCEPTED, QuoteStatus.EXPIRED, QuoteStatus.CONVERTED],
            QuoteStatus.EXPIRED: [QuoteStatus.DRAFT, QuoteStatus.SENT, QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.CONVERTED],
            QuoteStatus.CONVERTED: [QuoteStatus.DRAFT, QuoteStatus.SENT, QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.EXPIRED],
            QuoteStatus.CANCELLED: [QuoteStatus.DRAFT, QuoteStatus.SENT, QuoteStatus.ACCEPTED, QuoteStatus.REJECTED, QuoteStatus.EXPIRED, QuoteStatus.CONVERTED]
        }

    def quote_amount_calculations(self, items: List[Dict], discount_percentage: Decimal = Decimal("0"), tax_percentage: Decimal = Decimal("20")) -> Dict[str, Decimal]:
        """Calcule les montants d'un devis avec validation"""
        if not items:
            raise ValidationException("Liste d'articles vide")
        
        for item in items:
            if not item.get("quantity") or item["quantity"] <= 0:
                raise ValidationException("Quantité invalide")
            if not item.get("unit_price") or item["unit_price"] <= 0:
                raise ValidationException("Prix unitaire invalide")
        
        return self._calculate_quote_amounts(items, discount_percentage, tax_percentage)
