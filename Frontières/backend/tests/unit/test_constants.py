"""
Tests unitaires pour les constantes et enums - Millésime Sans Frontières
"""

import pytest
from decimal import Decimal
from app.core.constants import (
    OrderStatus, PaymentStatus, QuoteStatus, UserRole, BarrelCondition,
    WoodType, PreviousContent, SecurityLevel, BARREL_MIN_VOLUME, BARREL_MAX_VOLUME,
    BARREL_MIN_PRICE, BARREL_MAX_PRICE, BARREL_MIN_STOCK, BARREL_MAX_STOCK,
    ORDER_MIN_QUANTITY, ORDER_MAX_QUANTITY, QUOTE_MIN_VALIDITY_DAYS,
    QUOTE_MAX_VALIDITY_DAYS, QUOTE_MIN_DISCOUNT_PERCENTAGE, QUOTE_MAX_DISCOUNT_PERCENTAGE,
    QUOTE_MIN_TAX_PERCENTAGE, QUOTE_MAX_TAX_PERCENTAGE, NOTES_MAX_LENGTH,
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES, PAGINATION_DEFAULT_LIMIT, PAGINATION_MAX_LIMIT
)


class TestOrderStatus:
    """Tests pour l'enum OrderStatus"""

    def test_order_status_values(self):
        """Test des valeurs de statut de commande"""
        # Arrange
        expected_values = [
            "pending",
            "processing", 
            "shipped",
            "delivered",
            "cancelled",
            "returned"
        ]
        
        # Act
        actual_values = [status.value for status in OrderStatus]
        
        # Assert
        assert actual_values == expected_values
        assert len(OrderStatus) == 6

    def test_order_status_pending(self):
        """Test du statut en attente"""
        # Act & Assert
        assert OrderStatus.PENDING.value == "pending"

    def test_order_status_processing(self):
        """Test du statut en traitement"""
        # Act & Assert
        assert OrderStatus.PROCESSING.value == "processing"

    def test_order_status_shipped(self):
        """Test du statut expédié"""
        # Act & Assert
        assert OrderStatus.SHIPPED.value == "shipped"

    def test_order_status_delivered(self):
        """Test du statut livré"""
        # Act & Assert
        assert OrderStatus.DELIVERED.value == "delivered"

    def test_order_status_cancelled(self):
        """Test du statut annulé"""
        # Act & Assert
        assert OrderStatus.CANCELLED.value == "cancelled"

    def test_order_status_returned(self):
        """Test du statut retourné"""
        # Act & Assert
        assert OrderStatus.RETURNED.value == "returned"


class TestPaymentStatus:
    """Tests pour l'enum PaymentStatus"""

    def test_payment_status_values(self):
        """Test des valeurs de statut de paiement"""
        # Arrange
        expected_values = [
            "pending",
            "paid",
            "failed",
            "refunded",
            "partially_refunded"
        ]
        
        # Act
        actual_values = [status.value for status in PaymentStatus]
        
        # Assert
        assert actual_values == expected_values
        assert len(PaymentStatus) == 5

    def test_payment_status_pending(self):
        """Test du statut de paiement en attente"""
        # Act & Assert
        assert PaymentStatus.PENDING.value == "pending"

    def test_payment_status_paid(self):
        """Test du statut de paiement payé"""
        # Act & Assert
        assert PaymentStatus.PAID.value == "paid"

    def test_payment_status_failed(self):
        """Test du statut de paiement échoué"""
        # Act & Assert
        assert PaymentStatus.FAILED.value == "failed"

    def test_payment_status_refunded(self):
        """Test du statut de paiement remboursé"""
        # Act & Assert
        assert PaymentStatus.REFUNDED.value == "refunded"

    def test_payment_status_partially_refunded(self):
        """Test du statut de paiement partiellement remboursé"""
        # Act & Assert
        assert PaymentStatus.PARTIALLY_REFUNDED.value == "partially_refunded"


class TestQuoteStatus:
    """Tests pour l'enum QuoteStatus"""

    def test_quote_status_values(self):
        """Test des valeurs de statut de devis"""
        # Arrange
        expected_values = [
            "draft",
            "sent",
            "viewed",
            "accepted",
            "rejected",
            "expired",
            "converted",
            "cancelled"
        ]
        
        # Act
        actual_values = [status.value for status in QuoteStatus]
        
        # Assert
        assert actual_values == expected_values
        assert len(QuoteStatus) == 8

    def test_quote_status_draft(self):
        """Test du statut brouillon"""
        # Act & Assert
        assert QuoteStatus.DRAFT.value == "draft"

    def test_quote_status_sent(self):
        """Test du statut envoyé"""
        # Act & Assert
        assert QuoteStatus.SENT.value == "sent"

    def test_quote_status_viewed(self):
        """Test du statut consulté"""
        # Act & Assert
        assert QuoteStatus.VIEWED.value == "viewed"

    def test_quote_status_accepted(self):
        """Test du statut accepté"""
        # Act & Assert
        assert QuoteStatus.ACCEPTED.value == "accepted"

    def test_quote_status_rejected(self):
        """Test du statut rejeté"""
        # Act & Assert
        assert QuoteStatus.REJECTED.value == "rejected"

    def test_quote_status_expired(self):
        """Test du statut expiré"""
        # Act & Assert
        assert QuoteStatus.EXPIRED.value == "expired"

    def test_quote_status_converted(self):
        """Test du statut converti"""
        # Act & Assert
        assert QuoteStatus.CONVERTED.value == "converted"

    def test_quote_status_cancelled(self):
        """Test du statut annulé"""
        # Act & Assert
        assert QuoteStatus.CANCELLED.value == "cancelled"


class TestUserRole:
    """Tests pour l'enum UserRole"""

    def test_user_role_values(self):
        """Test des valeurs de rôle utilisateur"""
        # Arrange
        expected_values = [
            "admin",
            "manager",
            "sales",
            "customer",
            "guest"
        ]
        
        # Act
        actual_values = [role.value for role in UserRole]
        
        # Assert
        assert actual_values == expected_values
        assert len(UserRole) == 5

    def test_user_role_admin(self):
        """Test du rôle administrateur"""
        # Act & Assert
        assert UserRole.ADMIN.value == "admin"

    def test_user_role_manager(self):
        """Test du rôle manager"""
        # Act & Assert
        assert UserRole.MANAGER.value == "manager"

    def test_user_role_sales(self):
        """Test du rôle commercial"""
        # Act & Assert
        assert UserRole.SALES.value == "sales"

    def test_user_role_customer(self):
        """Test du rôle client"""
        # Act & Assert
        assert UserRole.CUSTOMER.value == "customer"

    def test_user_role_guest(self):
        """Test du rôle invité"""
        # Act & Assert
        assert UserRole.GUEST.value == "guest"


class TestBarrelCondition:
    """Tests pour l'enum BarrelCondition"""

    def test_barrel_condition_values(self):
        """Test des valeurs de condition de tonneau"""
        # Arrange
        expected_values = [
            "excellent",
            "good",
            "fair",
            "poor",
            "damaged"
        ]
        
        # Act
        actual_values = [condition.value for condition in BarrelCondition]
        
        # Assert
        assert actual_values == expected_values
        assert len(BarrelCondition) == 5

    def test_barrel_condition_excellent(self):
        """Test de la condition excellente"""
        # Act & Assert
        assert BarrelCondition.EXCELLENT.value == "excellent"

    def test_barrel_condition_good(self):
        """Test de la condition bonne"""
        # Act & Assert
        assert BarrelCondition.GOOD.value == "good"

    def test_barrel_condition_fair(self):
        """Test de la condition correcte"""
        # Act & Assert
        assert BarrelCondition.FAIR.value == "fair"

    def test_barrel_condition_poor(self):
        """Test de la condition médiocre"""
        # Act & Assert
        assert BarrelCondition.POOR.value == "poor"

    def test_barrel_condition_damaged(self):
        """Test de la condition endommagée"""
        # Act & Assert
        assert BarrelCondition.DAMAGED.value == "damaged"


class TestWoodType:
    """Tests pour l'enum WoodType"""

    def test_wood_type_values(self):
        """Test des valeurs de type de bois"""
        # Arrange
        expected_values = [
            "oak",
            "chestnut",
            "acacia",
            "cherry",
            "ash",
            "other"
        ]
        
        # Act
        actual_values = [wood.value for wood in WoodType]
        
        # Assert
        assert actual_values == expected_values
        assert len(WoodType) == 6

    def test_wood_type_oak(self):
        """Test du type de bois chêne"""
        # Act & Assert
        assert WoodType.OAK.value == "oak"

    def test_wood_type_chestnut(self):
        """Test du type de bois châtaignier"""
        # Act & Assert
        assert WoodType.CHESTNUT.value == "chestnut"

    def test_wood_type_acacia(self):
        """Test du type de bois acacia"""
        # Act & Assert
        assert WoodType.ACACIA.value == "acacia"

    def test_wood_type_cherry(self):
        """Test du type de bois cerisier"""
        # Act & Assert
        assert WoodType.CHERRY.value == "cherry"

    def test_wood_type_ash(self):
        """Test du type de bois frêne"""
        # Act & Assert
        assert WoodType.ASH.value == "ash"

    def test_wood_type_other(self):
        """Test du type de bois autre"""
        # Act & Assert
        assert WoodType.OTHER.value == "other"


class TestPreviousContent:
    """Tests pour l'enum PreviousContent"""

    def test_previous_content_values(self):
        """Test des valeurs de contenu précédent"""
        # Arrange
        expected_values = [
            "red_wine",
            "white_wine",
            "rose_wine",
            "champagne",
            "cognac",
            "whiskey",
            "rum",
            "other"
        ]
        
        # Act
        actual_values = [content.value for content in PreviousContent]
        
        # Assert
        assert actual_values == expected_values
        assert len(PreviousContent) == 8

    def test_previous_content_red_wine(self):
        """Test du contenu précédent vin rouge"""
        # Act & Assert
        assert PreviousContent.RED_WINE.value == "red_wine"

    def test_previous_content_white_wine(self):
        """Test du contenu précédent vin blanc"""
        # Act & Assert
        assert PreviousContent.WHITE_WINE.value == "white_wine"

    def test_previous_content_rose_wine(self):
        """Test du contenu précédent vin rosé"""
        # Act & Assert
        assert PreviousContent.ROSÉ_WINE.value == "rose_wine"

    def test_previous_content_champagne(self):
        """Test du contenu précédent champagne"""
        # Act & Assert
        assert PreviousContent.CHAMPAGNE.value == "champagne"

    def test_previous_content_cognac(self):
        """Test du contenu précédent cognac"""
        # Act & Assert
        assert PreviousContent.COGNAC.value == "cognac"

    def test_previous_content_whiskey(self):
        """Test du contenu précédent whiskey"""
        # Act & Assert
        assert PreviousContent.WHISKEY.value == "whiskey"

    def test_previous_content_rum(self):
        """Test du contenu précédent rhum"""
        # Act & Assert
        assert PreviousContent.RUM.value == "rum"

    def test_previous_content_other(self):
        """Test du contenu précédent autre"""
        # Act & Assert
        assert PreviousContent.OTHER.value == "other"


class TestSecurityLevel:
    """Tests pour l'enum SecurityLevel"""

    def test_security_level_values(self):
        """Test des valeurs de niveau de sécurité"""
        # Arrange
        expected_values = [
            "low",
            "medium",
            "high",
            "critical"
        ]
        
        # Act
        actual_values = [level.value for level in SecurityLevel]
        
        # Assert
        assert actual_values == expected_values
        assert len(SecurityLevel) == 4

    def test_security_level_low(self):
        """Test du niveau de sécurité faible"""
        # Act & Assert
        assert SecurityLevel.LOW.value == "low"

    def test_security_level_medium(self):
        """Test du niveau de sécurité moyen"""
        # Act & Assert
        assert SecurityLevel.MEDIUM.value == "medium"

    def test_security_level_high(self):
        """Test du niveau de sécurité élevé"""
        # Act & Assert
        assert SecurityLevel.HIGH.value == "high"

    def test_security_level_critical(self):
        """Test du niveau de sécurité critique"""
        # Act & Assert
        assert SecurityLevel.CRITICAL.value == "critical"


class TestBarrelValidationConstants:
    """Tests pour les constantes de validation des tonneaux"""

    def test_barrel_volume_constraints(self):
        """Test des contraintes de volume de tonneau"""
        # Act & Assert
        assert BARREL_MIN_VOLUME == Decimal("5.0")
        assert BARREL_MAX_VOLUME == Decimal("500.0")
        assert BARREL_MIN_VOLUME < BARREL_MAX_VOLUME
        assert BARREL_MIN_VOLUME > Decimal("0.00")

    def test_barrel_price_constraints(self):
        """Test des contraintes de prix de tonneau"""
        # Act & Assert
        assert BARREL_MIN_PRICE == Decimal("50.0")
        assert BARREL_MAX_PRICE == Decimal("50000.0")
        assert BARREL_MIN_PRICE < BARREL_MAX_PRICE
        assert BARREL_MIN_PRICE > Decimal("0.00")

    def test_barrel_stock_constraints(self):
        """Test des contraintes de stock de tonneau"""
        # Act & Assert
        assert BARREL_MIN_STOCK == 0
        assert BARREL_MAX_STOCK == 9999
        assert BARREL_MIN_STOCK < BARREL_MAX_STOCK
        assert BARREL_MIN_STOCK >= 0


class TestOrderValidationConstants:
    """Tests pour les constantes de validation des commandes"""

    def test_order_quantity_constraints(self):
        """Test des contraintes de quantité de commande"""
        # Act & Assert
        assert ORDER_MIN_QUANTITY == 1
        assert ORDER_MAX_QUANTITY == 1000
        assert ORDER_MIN_QUANTITY < ORDER_MAX_QUANTITY
        assert ORDER_MIN_QUANTITY > 0

    def test_order_quantity_range(self):
        """Test de la plage de quantités valides"""
        # Act & Assert
        assert ORDER_MIN_QUANTITY >= 1
        assert ORDER_MAX_QUANTITY <= 1000


class TestQuoteValidationConstants:
    """Tests pour les constantes de validation des devis"""

    def test_quote_validity_constraints(self):
        """Test des contraintes de validité des devis"""
        # Act & Assert
        assert QUOTE_MIN_VALIDITY_DAYS == 1
        assert QUOTE_MAX_VALIDITY_DAYS == 365
        assert QUOTE_MIN_VALIDITY_DAYS < QUOTE_MAX_VALIDITY_DAYS
        assert QUOTE_MIN_VALIDITY_DAYS > 0

    def test_quote_discount_constraints(self):
        """Test des contraintes de remise de devis"""
        # Act & Assert
        assert QUOTE_MIN_DISCOUNT_PERCENTAGE == Decimal("0.00")
        assert QUOTE_MAX_DISCOUNT_PERCENTAGE == Decimal("50.0")
        assert QUOTE_MIN_DISCOUNT_PERCENTAGE < QUOTE_MAX_DISCOUNT_PERCENTAGE
        assert QUOTE_MIN_DISCOUNT_PERCENTAGE >= Decimal("0.00")

    def test_quote_tax_constraints(self):
        """Test des contraintes de taxe de devis"""
        # Act & Assert
        assert QUOTE_MIN_TAX_PERCENTAGE == Decimal("0.00")
        assert QUOTE_MAX_TAX_PERCENTAGE == Decimal("30.0")
        assert QUOTE_MIN_TAX_PERCENTAGE < QUOTE_MAX_TAX_PERCENTAGE
        assert QUOTE_MIN_TAX_PERCENTAGE >= Decimal("0.00")


class TestGeneralConstants:
    """Tests pour les constantes générales"""

    def test_notes_max_length(self):
        """Test de la longueur maximale des notes"""
        # Act & Assert
        assert NOTES_MAX_LENGTH == 500
        assert NOTES_MAX_LENGTH > 0

    def test_jwt_token_expiry(self):
        """Test de l'expiration du token JWT"""
        # Act & Assert
        assert JWT_ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert JWT_ACCESS_TOKEN_EXPIRE_MINUTES > 0

    def test_pagination_constants(self):
        """Test des constantes de pagination"""
        # Act & Assert
        assert PAGINATION_DEFAULT_LIMIT == 20
        assert PAGINATION_MAX_LIMIT == 100
        assert PAGINATION_DEFAULT_LIMIT <= PAGINATION_MAX_LIMIT
        assert PAGINATION_DEFAULT_LIMIT > 0
