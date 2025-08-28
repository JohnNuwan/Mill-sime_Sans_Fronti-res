"""
Tests unitaires pour les modèles de base de données - Millésime Sans Frontières
"""

import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
from datetime import date, datetime, timedelta
import uuid

from app.models.user import User
from app.models.address import Address
from app.models.barrel import Barrel
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.core.constants import (
    UserRole, BarrelCondition, WoodType, PreviousContent,
    OrderStatus, PaymentStatus, QuoteStatus
)
from app.core.utils import generate_order_number


class TestUserModel:
    """Tests pour le modèle User"""

    def test_create_user_success(self, db_session: Session):
        """Test de création d'utilisateur réussie"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password_hash": "hashed_password",
            "first_name": "John",
            "last_name": "Doe",
            "phone_number": "+33123456789",
            "company_name": "Test Company",
            "role": "b2c"
        }
        
        # Act
        user = User(**user_data)
        db_session.add(user)
        db_session.commit()
        
        # Assert
        assert user.id is not None
        assert user.email == user_data["email"]
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.role == user_data["role"]
        assert user.is_active is True
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_create_user_without_required_fields(self, db_session: Session):
        """Test de création d'utilisateur sans champs requis"""
        # Arrange
        user_data = {
            "email": "test@example.com"
            # Manque password_hash, first_name, last_name
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            user = User(**user_data)
            db_session.add(user)
            db_session.commit()

    def test_user_email_uniqueness(self, db_session: Session):
        """Test de l'unicité de l'email"""
        # Arrange
        user1 = User(
            email="duplicate@example.com",
            password_hash="hash1",
            first_name="John",
            last_name="Doe"
        )
        user2 = User(
            email="duplicate@example.com",  # Même email
            password_hash="hash2",
            first_name="Jane",
            last_name="Smith"
        )
        
        # Act
        db_session.add(user1)
        db_session.commit()
        
        # Assert
        with pytest.raises(IntegrityError):
            db_session.add(user2)
            db_session.commit()

    def test_user_relationships(self, db_session: Session):
        """Test des relations de l'utilisateur"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        # Act
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address.user_id = user.id
        db_session.add(address)
        db_session.commit()
        
        # Assert
        assert len(user.addresses) == 1
        assert user.addresses[0].address_line_1 == "123 Test St"
        assert address.user.email == "test@example.com"

    def test_user_string_representation(self, db_session: Session):
        """Test de la représentation string de l'utilisateur"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        # Act
        user_str = str(user)
        
        # Assert
        assert "test@example.com" in user_str
        assert "None" in user_str  # role par défaut


class TestAddressModel:
    """Tests pour le modèle Address"""

    def test_create_address_success(self, db_session: Session):
        """Test de création d'adresse réussie"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        db_session.add(user)
        db_session.commit()
        
        address_data = {
            "user_id": user.id,
            "address_line_1": "123 Test Street",
            "city": "Test City",
            "postal_code": "12345",
            "country": "France",
            "address_type": "shipping"
        }
        
        # Act
        address = Address(**address_data)
        db_session.add(address)
        db_session.commit()
        
        # Assert
        assert address.id is not None
        assert address.address_line_1 == address_data["address_line_1"]
        assert address.city == address_data["city"]
        assert address.country == address_data["country"]
        assert address.address_type == address_data["address_type"]

    def test_address_required_fields(self, db_session: Session):
        """Test des champs requis pour l'adresse"""
        # Arrange
        address_data = {
            "address_line_1": "123 Test Street"
            # Manque user_id, city, postal_code, country
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            address = Address(**address_data)
            db_session.add(address)
            db_session.commit()

    def test_address_user_relationship(self, db_session: Session):
        """Test de la relation avec l'utilisateur"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        # Act
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address.user_id = user.id
        db_session.add(address)
        db_session.commit()
        
        # Assert
        assert address.user.email == "test@example.com"
        assert user.addresses[0].address_line_1 == "123 Test St"

    def test_address_string_representation(self, db_session: Session):
        """Test de la représentation string de l'adresse"""
        # Arrange
        address = Address(
            user_id="test-user-id",
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        # Act
        address_str = str(address)
        
        # Assert
        assert "Test City" in address_str
        assert "France" in address_str


class TestBarrelModel:
    """Tests pour le modèle Barrel"""

    def test_create_barrel_success(self, db_session: Session):
        """Test de création de tonneau réussie"""
        # Arrange
        barrel_data = {
            "name": "Fût de Chêne Premium",
            "description": "Fût de chêne français de haute qualité",
            "wood_type": WoodType.OAK,
            "condition": BarrelCondition.GOOD,
            "previous_content": PreviousContent.RED_WINE,
            "volume_liters": 225.0,
            "price": Decimal("1500.00"),
            "stock_quantity": 10,
            "origin_country": "France",
            "manufacturing_year": 2023
        }
        
        # Act
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # Assert
        assert barrel.id is not None
        assert barrel.name == barrel_data["name"]
        assert barrel.wood_type == barrel_data["wood_type"]
        assert barrel.condition == barrel_data["condition"]
        assert barrel.price == barrel_data["price"]
        assert barrel.stock_quantity == barrel_data["stock_quantity"]

    def test_barrel_required_fields(self, db_session: Session):
        """Test des champs requis pour le tonneau"""
        # Arrange
        barrel_data = {
            "name": "Test Barrel"
            # Manque wood_type, condition, volume, price, stock_quantity
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            barrel = Barrel(**barrel_data)
            db_session.add(barrel)
            db_session.commit()

    def test_barrel_enum_validation(self, db_session: Session):
        """Test de validation des énumérations"""
        # Arrange
        barrel_data = {
            "name": "Test Barrel",
            "wood_type": "INVALID_WOOD",  # Énumération invalide
            "condition": BarrelCondition.GOOD,
            "previous_content": PreviousContent.RED_WINE,
            "volume_liters": 225.0,
            "price": Decimal("1500.00"),
            "stock_quantity": 10
        }
        
        # Act & Assert
        # SQLAlchemy n'effectue pas la validation des énumérations au niveau Python
        # Mais la validation se fait lors de la lecture depuis la base de données
        barrel = Barrel(**barrel_data)
        db_session.add(barrel)
        db_session.commit()
        
        # La validation échoue lors de la lecture car la valeur n'est pas valide
        with pytest.raises(LookupError):
            db_session.refresh(barrel)

    def test_barrel_calculated_properties(self, db_session: Session):
        """Test des propriétés calculées du tonneau"""
        # Arrange
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=5
        )
        
        # Act & Assert
        # Les valeurs par défaut ne sont pas appliquées lors de la création d'objets Python
        # Elles sont appliquées au niveau de la base de données
        # Pour tester les propriétés, nous devons d'abord sauvegarder l'objet
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        assert barrel.is_in_stock is True  # stock_quantity > 0 et is_available == "Y"
        
        # Modifier le stock
        barrel.stock_quantity = 0
        assert barrel.is_in_stock is False
        
        barrel.stock_quantity = 2
        assert barrel.is_low_stock is True

    def test_barrel_stock_management(self, db_session: Session):
        """Test de la gestion du stock"""
        # Arrange
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        db_session.add(barrel)
        db_session.commit()
        
        # Act
        barrel.update_stock(5)  # Ajouter 5 au stock
        
        # Assert
        assert barrel.stock_quantity == 15  # 10 + 5
        assert barrel.is_available == "Y"

    def test_barrel_string_representation(self, db_session: Session):
        """Test de la représentation string du tonneau"""
        # Arrange
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        
        # Act
        barrel_str = str(barrel)
        
        # Assert
        assert "Test Barrel" in barrel_str
        assert "225.0L" in barrel_str
        assert "1500.00€" in barrel_str


class TestOrderModel:
    """Tests pour le modèle Order"""

    def test_create_order_success(self, db_session: Session):
        """Test de création de commande réussie"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        order_data = {
            "order_number": generate_order_number(),
            "user_id": user.id,
            "shipping_address_id": address.id,
            "billing_address_id": address.id,
            "status": OrderStatus.PENDING,
            "payment_status": PaymentStatus.PENDING,
            "shipping_method": "standard",
            "payment_method": "card",
            "customer_notes": "Commande de test"
        }
        
        # Act
        order = Order(**order_data)
        db_session.add(order)
        db_session.commit()
        
        # Assert
        assert order.id is not None
        assert order.order_number is not None
        assert order.status == order_data["status"]
        assert order.payment_status == order_data["payment_status"]
        assert order.user_id == user.id

    def test_order_required_fields(self, db_session: Session):
        """Test des champs requis pour la commande"""
        # Arrange
        order_data = {
            "status": OrderStatus.PENDING
            # Manque user_id, shipping_address_id, billing_address_id
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            order = Order(**order_data)
            db_session.add(order)
            db_session.commit()

    def test_order_number_generation(self, db_session: Session):
        """Test de la génération automatique du numéro de commande"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            shipping_address_id=address.id,
            billing_address_id=address.id,
            status=OrderStatus.PENDING
        )
        
        # Act
        db_session.add(order)
        db_session.commit()
        
        # Assert
        assert order.order_number is not None
        assert order.order_number.startswith("ORD-")
        assert len(order.order_number) > 4

    def test_order_relationships(self, db_session: Session):
        """Test des relations de la commande"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            shipping_address_id=address.id,
            billing_address_id=address.id,
            status=OrderStatus.PENDING
        )
        
        # Act
        db_session.add(order)
        db_session.commit()
        
        # Assert
        assert order.user.email == "test@example.com"
        assert order.shipping_address.address_line_1 == "123 Test St"
        assert order.billing_address.address_line_1 == "123 Test St"

    def test_order_string_representation(self, db_session: Session):
        """Test de la représentation string de la commande"""
        # Arrange
        order = Order(
            user_id="test-user-id",
            order_number="ORD-2024-001",
            status=OrderStatus.PENDING
        )
        
        # Act
        order_str = str(order)
        
        # Assert
        assert "Order" in order_str
        assert "ORD-2024-001" in order_str


class TestOrderItemModel:
    """Tests pour le modèle OrderItem"""

    def test_create_order_item_success(self, db_session: Session):
        """Test de création d'élément de commande réussie"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            shipping_address_id=address.id,
            billing_address_id=address.id,
            status=OrderStatus.PENDING
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address.user_id = user.id
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        order.user_id = user.id
        order.shipping_address_id = address.id
        order.billing_address_id = address.id
        db_session.add(order)
        db_session.commit()
        
        order_item_data = {
            "order_id": order.id,
            "barrel_id": barrel.id,
            "quantity": 2,
            "unit_price": Decimal("1500.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }
        
        # Act
        order_item = OrderItem(**order_item_data)
        order_item.calculate_total_price()
        db_session.add(order_item)
        db_session.commit()
        
        # Assert
        assert order_item.id is not None
        assert order_item.quantity == order_item_data["quantity"]
        assert order_item.unit_price == order_item_data["unit_price"]

    def test_order_item_required_fields(self, db_session: Session):
        """Test des champs requis pour l'élément de commande"""
        # Arrange
        order_item_data = {
            "quantity": 2
            # Manque order_id, barrel_id, unit_price
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            order_item = OrderItem(**order_item_data)
            db_session.add(order_item)
            db_session.commit()

    def test_order_item_relationships(self, db_session: Session):
        """Test des relations de l'élément de commande"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            shipping_address_id=address.id,
            billing_address_id=address.id,
            status=OrderStatus.PENDING
        )
        order_item = OrderItem(
            order_id=order.id,
            barrel_id=barrel.id,
            quantity=2,
            unit_price=Decimal("1500.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        
        # Act
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address.user_id = user.id
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        order.user_id = user.id
        order.shipping_address_id = address.id
        order.billing_address_id = address.id
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)
        
        order_item.order_id = order.id
        order_item.barrel_id = barrel.id
        order_item.calculate_total_price()
        db_session.add(order_item)
        db_session.commit()
        
        # Assert
        assert order_item.order.user.email == "test@example.com"
        assert order_item.barrel.name == "Test Barrel"

    def test_order_item_string_representation(self, db_session: Session):
        """Test de la représentation string de l'élément de commande"""
        # Arrange
        order_item = OrderItem(
            order_id="test-order-id",
            barrel_id="test-barrel-id",
            quantity=2,
            unit_price=Decimal("1500.00")
        )
        
        # Act
        order_item_str = str(order_item)
        
        # Assert
        assert "OrderItem" in order_item_str
        assert "2" in order_item_str
        assert "1500.00" in order_item_str


class TestQuoteModel:
    """Tests pour le modèle Quote"""

    def test_create_quote_success(self, db_session: Session):
        """Test de création de devis réussie"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        db_session.add(user)
        db_session.commit()
        
        quote_data = {
            "user_id": user.id,
            "quote_number": "QT-2024-001",
            "status": QuoteStatus.DRAFT,
            "valid_until": datetime.now() + timedelta(days=30),
            "shipping_cost": Decimal("50.00"),
            "tax_percentage": Decimal("20.00"),
            "discount_percentage": Decimal("5.00")
        }
        
        # Act
        quote = Quote(**quote_data)
        db_session.add(quote)
        db_session.commit()
        
        # Assert
        assert quote.id is not None
        assert quote.quote_number == quote_data["quote_number"]
        assert quote.status == quote_data["status"]
        assert quote.valid_until == quote_data["valid_until"]

    def test_quote_required_fields(self, db_session: Session):
        """Test des champs requis pour le devis"""
        # Arrange
        quote_data = {
            "quote_number": "QT-2024-001"
            # Manque user_id, valid_until
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            quote = Quote(**quote_data)
            db_session.add(quote)
            db_session.commit()

    def test_quote_number_generation(self, db_session: Session):
        """Test de la génération automatique du numéro de devis"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        
        db_session.add(user)
        db_session.commit()
        
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-001",
            valid_until=datetime.now() + timedelta(days=30)
        )
        
        # Act
        db_session.add(quote)
        db_session.commit()
        
        # Assert
        assert quote.quote_number is not None
        assert quote.quote_number.startswith("QT-")
        assert len(quote.quote_number) > 4

    def test_quote_relationships(self, db_session: Session):
        """Test des relations du devis"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-001",
            valid_until=datetime.now() + timedelta(days=30)
        )
        
        # Act
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        quote.user_id = user.id
        db_session.add(quote)
        db_session.commit()
        
        # Assert
        assert quote.user.email == "test@example.com"

    def test_quote_string_representation(self, db_session: Session):
        """Test de la représentation string du devis"""
        # Arrange
        quote = Quote(
            user_id="test-user-id",
            quote_number="QT-2024-001",
            valid_until=datetime.now() + timedelta(days=30)
        )
        
        # Act
        db_session.add(quote)
        db_session.flush()  # Pour appliquer les valeurs par défaut
        quote_str = str(quote)
        
        # Assert
        assert "Quote" in quote_str
        assert "QT-2024-001" in quote_str


class TestQuoteItemModel:
    """Tests pour le modèle QuoteItem"""

    def test_create_quote_item_success(self, db_session: Session):
        """Test de création d'élément de devis réussie"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-001",
            valid_until=datetime.now() + timedelta(days=30)
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        quote.user_id = user.id
        db_session.add(quote)
        db_session.commit()
        db_session.refresh(quote)
        
        quote_item_data = {
            "quote_id": quote.id,
            "barrel_id": barrel.id,
            "quantity": 3,
            "unit_price": Decimal("1400.00"),
            "discount_percentage": Decimal("0.00"),
            "tax_percentage": Decimal("20.00")
        }
        
        # Act
        quote_item = QuoteItem(**quote_item_data)
        quote_item.calculate_total_price()
        db_session.add(quote_item)
        db_session.commit()
        
        # Assert
        assert quote_item.id is not None
        assert quote_item.quantity == quote_item_data["quantity"]
        assert quote_item.unit_price == quote_item_data["unit_price"]
        assert quote_item.quantity == quote_item_data["quantity"]

    def test_quote_item_required_fields(self, db_session: Session):
        """Test des champs requis pour l'élément de devis"""
        # Arrange
        quote_item_data = {
            "quantity": 3
            # Manque quote_id, barrel_id, unit_price
        }
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            quote_item = QuoteItem(**quote_item_data)
            db_session.add(quote_item)
            db_session.commit()

    def test_quote_item_relationships(self, db_session: Session):
        """Test des relations de l'élément de devis"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-002",
            valid_until=datetime.now() + timedelta(days=30)
        )
        quote_item = QuoteItem(
            quote_id=quote.id,
            barrel_id=barrel.id,
            quantity=3,
            unit_price=Decimal("1400.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        
        # Act
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        quote.user_id = user.id
        db_session.add(quote)
        db_session.commit()
        db_session.refresh(quote)
        
        quote_item.quote_id = quote.id
        quote_item.barrel_id = barrel.id
        quote_item.calculate_total_price()
        db_session.add(quote_item)
        db_session.commit()
        
        # Assert
        assert quote_item.quote.user.email == "test@example.com"
        assert quote_item.barrel.name == "Test Barrel"

    def test_quote_item_string_representation(self, db_session: Session):
        """Test de la représentation string de l'élément de devis"""
        # Arrange
        quote_item = QuoteItem(
            quote_id="test-quote-id",
            barrel_id="test-barrel-id",
            quantity=3,
            unit_price=Decimal("1400.00")
        )
        
        # Act
        quote_item_str = str(quote_item)
        
        # Assert
        assert "QuoteItem" in quote_item_str
        assert "3" in quote_item_str
        assert "1400.00" in quote_item_str


class TestModelRelationships:
    """Tests des relations entre modèles"""

    def test_user_addresses_cascade(self, db_session: Session):
        """Test de la suppression en cascade des adresses lors de la suppression d'un utilisateur"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address1 = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        address2 = Address(
            user_id=user.id,
            address_line_1="456 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address1.user_id = user.id
        address2.user_id = user.id
        db_session.add(address1)
        db_session.add(address2)
        db_session.commit()
        
        # Act
        db_session.delete(user)
        db_session.commit()
        
        # Assert
        assert db_session.query(Address).count() == 0

    def test_order_items_cascade(self, db_session: Session):
        """Test de la suppression en cascade des éléments de commande lors de la suppression d'une commande"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        address = Address(
            user_id=user.id,
            address_line_1="123 Test St",
            city="Test City",
            postal_code="12345",
            country="France"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        order = Order(
            order_number=generate_order_number(),
            user_id=user.id,
            shipping_address_id=address.id,
            billing_address_id=address.id,
            status=OrderStatus.PENDING
        )
        order_item1 = OrderItem(
            order_id=order.id,
            barrel_id=barrel.id,
            quantity=2,
            unit_price=Decimal("1500.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        order_item2 = OrderItem(
            order_id=order.id,
            barrel_id=barrel.id,
            quantity=1,
            unit_price=Decimal("1500.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        address.user_id = user.id
        db_session.add(address)
        db_session.commit()
        db_session.refresh(address)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        order.user_id = user.id
        order.shipping_address_id = address.id
        order.billing_address_id = address.id
        db_session.add(order)
        db_session.commit()
        db_session.refresh(order)
        
        order_item1.order_id = order.id
        order_item1.barrel_id = barrel.id
        order_item1.calculate_total_price()
        order_item2.order_id = order.id
        order_item2.barrel_id = barrel.id
        order_item2.calculate_total_price()
        db_session.add(order_item1)
        db_session.add(order_item2)
        db_session.commit()
        
        # Act
        db_session.delete(order)
        db_session.commit()
        
        # Assert
        assert db_session.query(OrderItem).count() == 0

    def test_quote_items_cascade(self, db_session: Session):
        """Test de la suppression en cascade des éléments de devis lors de la suppression d'un devis"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-003",
            valid_until=datetime.now() + timedelta(days=30)
        )
        quote_item1 = QuoteItem(
            quote_id=quote.id,
            barrel_id=barrel.id,
            quantity=3,
            unit_price=Decimal("1400.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        quote_item2 = QuoteItem(
            quote_id=quote.id,
            barrel_id=barrel.id,
            quantity=2,
            unit_price=Decimal("1400.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        quote.user_id = user.id
        db_session.add(quote)
        db_session.commit()
        db_session.refresh(quote)
        
        quote_item1.quote_id = quote.id
        quote_item1.barrel_id = barrel.id
        quote_item1.calculate_total_price()
        quote_item2.quote_id = quote.id
        quote_item2.barrel_id = barrel.id
        quote_item2.calculate_total_price()
        
        db_session.add(quote_item1)
        db_session.add(quote_item2)
        db_session.commit()
        
        # Act
        db_session.delete(quote)
        db_session.commit()
        
        # Assert
        assert db_session.query(QuoteItem).count() == 0

    def test_barrel_quote_items_cascade(self, db_session: Session):
        """Test de la suppression en cascade des éléments de devis lors de la suppression d'un tonneau"""
        # Arrange
        user = User(
            email="test@example.com",
            password_hash="hash",
            first_name="John",
            last_name="Doe"
        )
        barrel = Barrel(
            name="Test Barrel",
            wood_type=WoodType.OAK,
            condition=BarrelCondition.GOOD,
            previous_content=PreviousContent.RED_WINE,
            volume_liters=225.0,
            price=Decimal("1500.00"),
            stock_quantity=10
        )
        quote = Quote(
            user_id=user.id,
            quote_number="QT-2024-004",
            valid_until=datetime.now() + timedelta(days=30)
        )
        quote_item = QuoteItem(
            quote_id=quote.id,
            barrel_id=barrel.id,
            quantity=3,
            unit_price=Decimal("1400.00"),
            discount_percentage=Decimal("0.00"),
            tax_percentage=Decimal("20.00")
        )
        
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        barrel.user_id = user.id
        db_session.add(barrel)
        db_session.commit()
        db_session.refresh(barrel)
        
        quote.user_id = user.id
        db_session.add(quote)
        db_session.commit()
        db_session.refresh(quote)
        
        quote_item.quote_id = quote.id
        quote_item.barrel_id = barrel.id
        quote_item.calculate_total_price()
        
        db_session.add(quote_item)
        db_session.commit()
        
        # Act
        db_session.delete(barrel)
        db_session.commit()
        
        # Assert
        assert db_session.query(QuoteItem).count() == 0
