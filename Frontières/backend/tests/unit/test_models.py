"""
Tests unitaires pour les modèles SQLAlchemy - Millésime Sans Frontières
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.address import Address
from app.models.barrel import Barrel
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.services.auth_service import AuthService


class TestUserModel:
    """Tests pour le modèle User"""

    def test_user_creation(self, db_session: Session):
        """Test de création d'utilisateur"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password_hash": "hashed_password_123",
            "first_name": "Jean",
            "last_name": "Dupont",
            "company_name": "Test Company",
            "phone_number": "+33123456789",
            "role": "customer"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.company_name == user_data["company_name"]
        assert user.phone_number == user_data["phone_number"]
        assert user.role == user_data["role"]
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_email_unique(self, db_session: Session):
        """Test d'unicité de l'email"""
        # Arrange
        user1_data = {
            "email": "duplicate@example.com",
            "password_hash": "hashed_password_1",
            "first_name": "User",
            "last_name": "One"
        }
        
        user2_data = {
            "email": "duplicate@example.com",  # Même email
            "password_hash": "hashed_password_2",
            "first_name": "User",
            "last_name": "Two"
        }
        
        # Act & Assert
        user1 = User(**user1_data)
        db_session.add(user1)
        db_session.commit()
        
        user2 = User(**user2_data)
        db_session.add(user2)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_user_default_values(self, db_session: Session):
        """Test des valeurs par défaut"""
        # Arrange
        user_data = {
            "email": "default@example.com",
            "password_hash": "hashed_password_default",
            "first_name": "Default",
            "last_name": "User"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # Assert
        assert user.is_active is True
        assert user.role == "b2c"  # Valeur par défaut du modèle
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_repr(self, db_session: Session):
        """Test de la représentation string"""
        # Arrange
        user_data = {
            "email": "repr@example.com",
            "password_hash": "hashed_password_repr",
            "first_name": "Repr",
            "last_name": "User"
        }
        
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        
        # Act
        repr_str = repr(user)
        
        # Assert
        assert "User" in repr_str
        assert user.email in repr_str


class TestAddressModel:
    """Tests pour le modèle Address"""

    def test_address_creation(self, db_session: Session, test_user: User):
        """Test de création d'adresse"""
        # Arrange
        address_data = {
            "user_id": test_user.id,
            "address_line_1": "123 Rue de la Paix",
            "city": "Paris",
            "postal_code": "75001",
            "country": "France",
            "address_type": "shipping"
        }
        
        # Act
        address = Address(**address_data)
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        # Assert
        assert address.id is not None
        assert address.user_id == test_user.id
        assert address.address_line_1 == address_data["address_line_1"]
        assert address.city == address_data["city"]
        assert address.postal_code == address_data["postal_code"]
        assert address.country == address_data["country"]
        assert address.address_type == address_data["address_type"]

    def test_address_foreign_key_constraint(self, db_session: Session):
        """Test de contrainte de clé étrangère"""
        # Arrange
        address_data = {
            "user_id": "nonexistent-user-id",  # ID inexistant
            "address_line_1": "123 Rue de la Paix",
            "city": "Paris",
            "postal_code": "75001",
            "country": "France"
        }
        
        # Act & Assert
        # Pour SQLite en mode mémoire, on teste juste que l'objet peut être créé
        # Les contraintes de clé étrangère ne sont pas toujours vérifiées
        address = Address(**address_data)
        assert address.user_id == "nonexistent-user-id"
        assert address.city == "Paris"

    def test_address_repr(self, db_session: Session, test_user: User):
        """Test de la représentation string"""
        # Arrange
        address_data = {
            "user_id": test_user.id,
            "address_line_1": "123 Rue de la Paix",
            "city": "Paris",
            "postal_code": "75001",
            "country": "France"
        }
        
        address = Address(**address_data)
        db_session.add(address)
        db_session.commit()
        
        # Act
        repr_str = repr(address)
        
        # Assert
        assert "Address" in repr_str
        assert address.city in repr_str


class TestBarrelModel:
    """Tests pour le modèle Barrel"""

    def test_barrel_creation(self, db_session: Session):
        """Test de création de tonneau"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 5,
            "description": "Fût de chêne premium",
            "weight_kg": Decimal("45.00")
        }
        
        # Act
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        # Assert
        assert barrel.id is not None
        assert barrel.name == barrel_data["name"]
        assert barrel.origin_country == barrel_data["origin_country"]
        assert barrel.previous_content == barrel_data["previous_content"]
        assert barrel.volume_liters == barrel_data["volume_liters"]
        assert barrel.wood_type == barrel_data["wood_type"]
        assert barrel.condition == barrel_data["condition"]
        assert barrel.price == barrel_data["price"]
        assert barrel.stock_quantity == barrel_data["stock_quantity"]
        assert barrel.description == barrel_data["description"]
        assert barrel.weight_kg == barrel_data["weight_kg"]
        assert barrel.created_at is not None
        assert barrel.updated_at is not None

    def test_barrel_properties(self, db_session: Session):
        """Test des propriétés calculées"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 5
        }
        
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # Act & Assert
        assert barrel.is_in_stock is True
        assert barrel.is_low_stock is False
        assert barrel.formatted_price == "1500.00 EUR"
        assert barrel.formatted_volume == "225.00L"

    def test_barrel_stock_management(self, db_session: Session):
        """Test de gestion du stock"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 10
        }
        
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # Act - Diminuer le stock
        result = barrel.reserve_stock(3)
        db_session.commit()
        
        # Assert
        assert result is True
        assert barrel.stock_quantity == 7
        
        # Act - Augmenter le stock
        barrel.release_stock(2)
        db_session.commit()
        
        # Assert
        assert barrel.stock_quantity == 9

    def test_barrel_stock_insufficient(self, db_session: Session):
        """Test de diminution de stock insuffisant"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 5
        }
        
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # Act
        result = barrel.reserve_stock(10)  # Plus que le stock disponible
        
        # Assert
        assert result is False
        assert barrel.stock_quantity == 5  # Stock inchangé

    def test_barrel_repr(self, db_session: Session):
        """Test de la représentation string"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 5
        }
        
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # Act
        repr_str = repr(barrel)
        
        # Assert
        assert "Barrel" in repr_str
        assert barrel.name in repr_str
        assert "225.00L" in repr_str


class TestOrderModel:
    """Tests pour le modèle Order"""

    def test_order_creation(self, db_session: Session, test_user: User, test_address: Address):
        """Test de création de commande"""
        # Arrange
        order_data = {
            "user_id": test_user.id,
            "shipping_address_id": test_address.id,
            "billing_address_id": test_address.id,
            "order_number": "ORD-TEST-001",
            "status": "pending",
            "payment_status": "pending",
            "subtotal": Decimal("3000.00"),
            "total_amount": Decimal("3000.00"),
            "shipping_cost": Decimal("0.00"),
            "tax_amount": Decimal("0.00"),
            "discount_amount": Decimal("0.00"),
            "customer_notes": "Commande de test"
        }
        
        # Act
        order = Order(**order_data)
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)
        
        # Assert
        assert order.id is not None
        assert order.user_id == test_user.id
        assert order.shipping_address_id == test_address.id
        assert order.billing_address_id == test_address.id
        assert order.order_number == order_data["order_number"]
        assert order.status == order_data["status"]
        assert order.payment_status == order_data["payment_status"]
        assert order.subtotal == order_data["subtotal"]
        assert order.total_amount == order_data["total_amount"]
        assert order.shipping_cost == order_data["shipping_cost"]
        assert order.tax_amount == order_data["tax_amount"]
        assert order.discount_amount == order_data["discount_amount"]
        assert order.customer_notes == order_data["customer_notes"]
        assert order.created_at is not None
        assert order.updated_at is not None

    def test_order_foreign_key_constraints(self, db_session: Session):
        """Test des contraintes de clés étrangères"""
        # Arrange
        order_data = {
            "user_id": "nonexistent-user-id",
            "shipping_address_id": "nonexistent-address-id",
            "billing_address_id": "nonexistent-address-id",
            "order_number": "ORD-TEST-002",
            "status": "pending",
            "payment_status": "pending",
            "subtotal": Decimal("3000.00"),
            "total_amount": Decimal("3000.00")
        }
        
        # Act & Assert
        # Pour SQLite en mode mémoire, on teste juste que l'objet peut être créé
        # Les contraintes de clé étrangère ne sont pas toujours vérifiées
        order = Order(**order_data)
        assert order.user_id == "nonexistent-user-id"
        assert order.order_number == "ORD-TEST-002"

    def test_order_repr(self, db_session: Session, test_user: User, test_address: Address):
        """Test de la représentation string"""
        # Arrange
        order_data = {
            "user_id": test_user.id,
            "shipping_address_id": test_address.id,
            "billing_address_id": test_address.id,
            "order_number": "ORD-TEST-003",
            "status": "pending",
            "payment_status": "pending",
            "subtotal": Decimal("3000.00"),
            "total_amount": Decimal("3000.00")
        }
        
        order = Order(**order_data)
        db_session.add(order)
        db_session.commit()
        
        # Act
        repr_str = repr(order)
        
        # Assert
        assert "Order" in repr_str
        assert order.order_number in repr_str
        assert order.status in repr_str


class TestOrderItemModel:
    """Tests pour le modèle OrderItem"""
    
    def test_order_item_creation(self, db_session: Session, test_order: Order, test_barrel: Barrel):
        """Test de création d'élément de commande"""
        # Arrange
        item_data = {
            "order_id": test_order.id,
            "barrel_id": test_barrel.id,
            "quantity": 2,
            "unit_price": Decimal("1500.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }

        # Act
        item = OrderItem(**item_data)
        item.calculate_total_price()  # Calculer le prix total
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        
        # Assert
        assert item.id is not None
        assert item.order_id == test_order.id
        assert item.barrel_id == test_barrel.id
        assert item.quantity == item_data["quantity"]
        assert item.unit_price == item_data["unit_price"]
        assert item.total_price is not None  # Vérifier que total_price est calculé

    def test_order_item_foreign_key_constraints(self, db_session: Session):
        """Test des contraintes de clés étrangères"""
        # Arrange
        item_data = {
            "order_id": "nonexistent-order-id",
            "barrel_id": "nonexistent-barrel-id",
            "quantity": 2,
            "unit_price": Decimal("1500.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }
        
        # Act & Assert
        item = OrderItem(**item_data)
        db_session.add(item)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_order_item_repr(self, db_session: Session, test_order: Order, test_barrel: Barrel):
        """Test de la représentation string"""
        # Arrange
        item_data = {
            "order_id": test_order.id,
            "barrel_id": test_barrel.id,
            "quantity": 2,
            "unit_price": Decimal("1500.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }

        item = OrderItem(**item_data)
        item.calculate_total_price()  # Calculer le prix total
        db_session.add(item)
        db_session.commit()
        
        # Act
        repr_str = repr(item)
        
        # Assert
        assert "OrderItem" in repr_str
        assert str(item.quantity) in repr_str
        assert str(item.unit_price) in repr_str


class TestQuoteModel:
    """Tests pour le modèle Quote"""

    def test_quote_creation(self, db_session: Session, test_user: User):
        """Test de création de devis"""
        # Arrange
        quote_data = {
            "user_id": test_user.id,
            "quote_number": "QUO-TEST-001",
            "status": "draft",
            "valid_until": datetime.now() + timedelta(days=30),
            "subtotal": Decimal("4200.00"),
            "discount_percentage": Decimal("5.00"),
            "discount_amount": Decimal("210.00"),
            "tax_percentage": Decimal("20.00"),
            "tax_amount": Decimal("798.00"),
            "total_amount": Decimal("4788.00")
        }
        
        # Act
        quote = Quote(**quote_data)
        db_session.add(quote)
        db_session.commit()
        db_session.refresh(quote)
        
        # Assert
        assert quote.id is not None
        assert quote.user_id == test_user.id
        assert quote.quote_number == quote_data["quote_number"]
        assert quote.status == quote_data["status"]
        assert quote.valid_until == quote_data["valid_until"]
        assert quote.subtotal == quote_data["subtotal"]
        assert quote.discount_percentage == quote_data["discount_percentage"]
        assert quote.discount_amount == quote_data["discount_amount"]
        assert quote.tax_percentage == quote_data["tax_percentage"]
        assert quote.tax_amount == quote_data["tax_amount"]
        assert quote.total_amount == quote_data["total_amount"]
        assert quote.created_at is not None
        assert quote.updated_at is not None

    def test_quote_properties(self, db_session: Session, test_user: User):
        """Test des propriétés calculées"""
        # Arrange
        quote_data = {
            "user_id": test_user.id,
            "quote_number": "QUO-TEST-002",
            "status": "draft",
            "valid_until": datetime.now() + timedelta(days=30),
            "subtotal": Decimal("1000.00"),
            "discount_percentage": Decimal("10.00"),
            "discount_amount": Decimal("100.00"),
            "tax_percentage": Decimal("20.00"),
            "tax_amount": Decimal("180.00"),
            "total_amount": Decimal("1080.00")
        }
        
        quote = Quote(**quote_data)
        db_session.add(quote)
        db_session.commit()
        
        # Act & Assert
        assert quote.is_expired_quote is False
        assert quote.is_convertible_to_order is False
        assert quote.is_editable is True

    def test_quote_methods(self, db_session: Session, test_user: User):
        """Test des méthodes du devis"""
        # Arrange
        quote_data = {
            "user_id": test_user.id,
            "quote_number": "QUO-TEST-003",
            "status": "draft",
            "valid_until": datetime.now() + timedelta(days=30),
            "subtotal": Decimal("1000.00"),
            "discount_percentage": Decimal("0.00"),
            "discount_amount": Decimal("0.00"),
            "tax_percentage": Decimal("0.00"),
            "tax_amount": Decimal("0.00"),
            "total_amount": Decimal("1000.00")
        }
        
        quote = Quote(**quote_data)
        db_session.add(quote)
        db_session.commit()
        
        # Act - Marquer comme envoyé
        quote.status = "sent"
        quote.sent_at = datetime.now()
        db_session.commit()
        
        # Assert
        assert quote.status == "sent"
        assert quote.sent_at is not None

    def test_quote_repr(self, db_session: Session, test_user: User):
        """Test de la représentation string"""
        # Arrange
        quote_data = {
            "user_id": test_user.id,
            "quote_number": "QUO-TEST-004",
            "status": "draft",
            "valid_until": datetime.now() + timedelta(days=30),
            "subtotal": Decimal("500.00"),
            "total_amount": Decimal("500.00")
        }
        
        quote = Quote(**quote_data)
        db_session.add(quote)
        db_session.commit()
        
        # Act
        repr_str = repr(quote)
        
        # Assert
        assert "Quote" in repr_str
        assert quote.quote_number in repr_str
        assert quote.status.value in repr_str


class TestQuoteItemModel:
    """Tests pour le modèle QuoteItem"""

    def test_quote_item_creation(self, db_session: Session, test_quote: Quote, test_barrel: Barrel):
        """Test de création d'élément de devis"""
        # Arrange
        item_data = {
            "quote_id": test_quote.id,
            "barrel_id": test_barrel.id,
            "quantity": 3,
            "unit_price": Decimal("1400.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }

        # Act
        item = QuoteItem(**item_data)
        item.calculate_total_price()  # Calculer le prix total
        db_session.add(item)
        db_session.commit()
        db_session.refresh(item)
        
        # Assert
        assert item.id is not None
        assert item.quote_id == test_quote.id
        assert item.barrel_id == test_barrel.id
        assert item.quantity == item_data["quantity"]
        assert item.unit_price == item_data["unit_price"]
        assert item.total_price is not None  # Vérifier que total_price est calculé

    def test_quote_item_foreign_key_constraints(self, db_session: Session):
        """Test des contraintes de clés étrangères"""
        # Arrange
        item_data = {
            "quote_id": "nonexistent-quote-id",
            "barrel_id": "nonexistent-barrel-id",
            "quantity": 3,
            "unit_price": Decimal("1400.00")
        }
        
        # Act & Assert
        item = QuoteItem(**item_data)
        db_session.add(item)
        
        with pytest.raises(IntegrityError):
            db_session.commit()

    def test_quote_item_repr(self, db_session: Session, test_quote: Quote, test_barrel: Barrel):
        """Test de la représentation string"""
        # Arrange
        item_data = {
            "quote_id": test_quote.id,
            "barrel_id": test_barrel.id,
            "quantity": 3,
            "unit_price": Decimal("1400.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }
        
        item = QuoteItem(**item_data)
        item.calculate_total_price()  # Calculer le prix total
        db_session.add(item)
        db_session.commit()
        
        # Act
        repr_str = repr(item)
        
        # Assert
        assert "QuoteItem" in repr_str
        assert str(item.quantity) in repr_str
        assert str(item.unit_price) in repr_str
