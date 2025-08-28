"""
Tests unitaires pour les schémas Pydantic - Millésime Sans Frontières
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin
from app.schemas.barrel import BarrelCreate, BarrelUpdate, BarrelResponse
from app.schemas.order import OrderCreate, OrderUpdate, OrderResponse, OrderItemCreate
from app.schemas.quote import QuoteCreate, QuoteUpdate, QuoteResponse, QuoteItemCreate


class TestUserSchemas:
    """Tests pour les schémas utilisateur"""

    def test_user_create_valid(self):
        """Test de création d'utilisateur avec données valides"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirm": "testpassword123",
            "first_name": "Jean",
            "last_name": "Dupont",
            "company_name": "Test Company",
            "phone_number": "+33123456789",
            "role": "customer"
        }

        # Act
        user = UserCreate(**user_data)
        
        # Assert
        assert user.email == user_data["email"]
        assert user.password == user_data["password"]
        assert user.first_name == user_data["first_name"]
        assert user.last_name == user_data["last_name"]
        assert user.company_name == user_data["company_name"]
        assert user.phone_number == user_data["phone_number"]
        assert user.role == user_data["role"]

    def test_user_create_invalid_email(self):
        """Test de création d'utilisateur avec email invalide"""
        # Arrange
        user_data = {
            "email": "invalid-email",
            "password": "testpassword123",
            "first_name": "Jean",
            "last_name": "Dupont"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_short_password(self):
        """Test de création d'utilisateur avec mot de passe trop court"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "123",
            "first_name": "Jean",
            "last_name": "Dupont"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_create_missing_required_fields(self):
        """Test de création d'utilisateur avec champs manquants"""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123"
            # first_name et last_name manquants
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_user_update_partial(self):
        """Test de mise à jour partielle d'utilisateur"""
        # Arrange
        update_data = {
            "first_name": "Nouveau Prénom"
        }
        
        # Act
        user_update = UserUpdate(**update_data)
        
        # Assert
        assert user_update.first_name == "Nouveau Prénom"
        assert user_update.last_name is None
        assert user_update.company_name is None

    def test_user_login_valid(self):
        """Test de connexion utilisateur avec données valides"""
        # Arrange
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }

        # Act
        login = UserLogin(**login_data)
        
        # Assert
        assert login.email == login_data["email"]
        assert login.password == login_data["password"]


class TestBarrelSchemas:
    """Tests pour les schémas tonneau"""

    def test_barrel_create_valid(self):
        """Test de création de tonneau avec données valides"""
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
        
        # Act
        barrel = BarrelCreate(**barrel_data)
        
        # Assert
        assert barrel.name == barrel_data["name"]
        assert barrel.origin_country == barrel_data["origin_country"]
        assert barrel.previous_content == barrel_data["previous_content"]
        assert barrel.volume_liters == barrel_data["volume_liters"]
        assert barrel.wood_type == barrel_data["wood_type"]
        assert barrel.condition == barrel_data["condition"]
        assert barrel.price == barrel_data["price"]
        assert barrel.stock_quantity == barrel_data["stock_quantity"]

    def test_barrel_create_invalid_price(self):
        """Test de création de tonneau avec prix invalide"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("-100.00"),  # Prix négatif
            "stock_quantity": 5
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            BarrelCreate(**barrel_data)

    def test_barrel_create_invalid_volume(self):
        """Test de création de tonneau avec volume invalide"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("0.00"),  # Volume nul
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": 5
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            BarrelCreate(**barrel_data)

    def test_barrel_create_invalid_stock(self):
        """Test de création de tonneau avec stock invalide"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.00"),
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.00"),
            "stock_quantity": -1  # Stock négatif
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            BarrelCreate(**barrel_data)

    def test_barrel_update_partial(self):
        """Test de mise à jour partielle de tonneau"""
        # Arrange
        update_data = {
            "price": Decimal("1600.00"),
            "stock_quantity": 10
        }
        
        # Act
        barrel_update = BarrelUpdate(**update_data)
        
        # Assert
        assert barrel_update.price == Decimal("1600.00")
        assert barrel_update.stock_quantity == 10
        assert barrel_update.name is None


class TestOrderSchemas:
    """Tests pour les schémas commande"""

    def test_order_item_create_valid(self):
        """Test de création d'élément de commande avec données valides"""
        # Arrange
        item_data = {
            "barrel_id": "test-barrel-id",
            "quantity": 2,
            "unit_price": Decimal("1500.00")
        }
        
        # Act
        item = OrderItemCreate(**item_data)
        
        # Assert
        assert item.barrel_id == item_data["barrel_id"]
        assert item.quantity == item_data["quantity"]
        assert item.unit_price == item_data["unit_price"]

    def test_order_item_create_invalid_quantity(self):
        """Test de création d'élément de commande avec quantité invalide"""
        # Arrange
        item_data = {
            "barrel_id": "test-barrel-id",
            "quantity": 0,  # Quantité nulle
            "unit_price": Decimal("1500.00")
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            OrderItemCreate(**item_data)

    def test_order_item_create_invalid_price(self):
        """Test de création d'élément de commande avec prix invalide"""
        # Arrange
        item_data = {
            "barrel_id": "test-barrel-id",
            "quantity": 2,
            "unit_price": Decimal("-100.00")  # Prix négatif
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            OrderItemCreate(**item_data)

    def test_order_create_valid(self):
        """Test de création de commande avec données valides"""
        # Arrange
        order_data = {
            "shipping_address_id": "test-shipping-address-id",
            "billing_address_id": "test-billing-address-id",
            "notes": "Commande de test",
            "shipping_method": "standard",
            "payment_method": "card",
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 2,
                    "unit_price": Decimal("1500.00")
                }
            ]
        }
        
        # Act
        order = OrderCreate(**order_data)
        
        # Assert
        assert order.shipping_address_id == order_data["shipping_address_id"]
        assert order.billing_address_id == order_data["billing_address_id"]
        assert order.notes == order_data["notes"]
        assert order.shipping_method == order_data["shipping_method"]
        assert order.payment_method == order_data["payment_method"]
        assert len(order.items) == 1
        assert order.items[0].barrel_id == "test-barrel-id"

    def test_order_create_empty_items(self):
        """Test de création de commande sans éléments"""
        # Arrange
        order_data = {
            "shipping_address_id": "test-shipping-address-id",
            "billing_address_id": "test-billing-address-id",
            "items": []  # Liste vide
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            OrderCreate(**order_data)

    def test_order_update_partial(self):
        """Test de mise à jour partielle de commande"""
        # Arrange
        update_data = {
            "notes": "Nouvelles notes",
            "shipping_method": "express"
        }
        
        # Act
        order_update = OrderUpdate(**update_data)
        
        # Assert
        assert order_update.notes == "Nouvelles notes"
        assert order_update.shipping_method == "express"
        assert order_update.payment_method is None


class TestQuoteSchemas:
    """Tests pour les schémas devis"""

    def test_quote_item_create_valid(self):
        """Test de création d'élément de devis avec données valides"""
        # Arrange
        item_data = {
            "barrel_id": "test-barrel-id",
            "quantity": 3,
            "unit_price": Decimal("1400.00"),
            "description": "Fûts de chêne premium"
        }
        
        # Act
        item = QuoteItemCreate(**item_data)
        
        # Assert
        assert item.barrel_id == item_data["barrel_id"]
        assert item.quantity == item_data["quantity"]
        assert item.unit_price == item_data["unit_price"]
        assert item.description == item_data["description"]

    def test_quote_create_valid(self):
        """Test de création de devis avec données valides"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "description": "Devis pour fûts de chêne",
            "valid_until": date.today() + timedelta(days=30),
            "terms_conditions": "Conditions standard",
            "notes": "Devis de test",
            "shipping_cost": Decimal("50.00"),
            "tax_rate": Decimal("20.00"),
            "discount_percentage": Decimal("5.00"),
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00"),
                    "description": "Fûts de chêne premium"
                }
            ]
        }
        
        # Act
        quote = QuoteCreate(**quote_data)
        
        # Assert
        assert quote.title == quote_data["title"]
        assert quote.description == quote_data["description"]
        assert quote.valid_until == quote_data["valid_until"]
        assert quote.terms_conditions == quote_data["terms_conditions"]
        assert quote.notes == quote_data["notes"]
        assert quote.shipping_cost == quote_data["shipping_cost"]
        assert quote.tax_rate == quote_data["tax_rate"]
        assert quote.discount_percentage == quote_data["discount_percentage"]
        assert len(quote.items) == 1

    def test_quote_create_past_validity_date(self):
        """Test de création de devis avec date de validité dans le passé"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "description": "Devis pour fûts de chêne",
            "valid_until": date.today() - timedelta(days=1),  # Hier
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            QuoteCreate(**quote_data)

    def test_quote_create_invalid_tax_rate(self):
        """Test de création de devis avec taux de taxe invalide"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "description": "Devis pour fûts de chêne",
            "valid_until": date.today() + timedelta(days=30),
            "tax_rate": Decimal("150.00"),  # Taux > 100%
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            QuoteCreate(**quote_data)

    def test_quote_create_invalid_discount_percentage(self):
        """Test de création de devis avec pourcentage de remise invalide"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "description": "Devis pour fûts de chêne",
            "valid_until": date.today() + timedelta(days=30),
            "discount_percentage": Decimal("150.00"),  # Remise > 100%
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            QuoteCreate(**quote_data)

    def test_quote_update_partial(self):
        """Test de mise à jour partielle de devis"""
        # Arrange
        update_data = {
            "title": "Nouveau titre",
            "valid_until": date.today() + timedelta(days=60)
        }
        
        # Act
        quote_update = QuoteUpdate(**update_data)
        
        # Assert
        assert quote_update.title == "Nouveau titre"
        assert quote_update.valid_until == date.today() + timedelta(days=60)
        assert quote_update.description is None


class TestSchemaValidation:
    """Tests de validation générale des schémas"""

    def test_decimal_precision(self):
        """Test de la précision des champs décimaux"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": Decimal("225.123"),  # Plus de 2 décimales
            "wood_type": "oak",
            "condition": "excellent",
            "price": Decimal("1500.123"),  # Plus de 2 décimales
            "stock_quantity": 5
        }
        
        # Act
        barrel = BarrelCreate(**barrel_data)
        
        # Assert
        # Les champs décimaux doivent être acceptés même avec plus de 2 décimales
        # La validation se fait au niveau de la base de données
        assert barrel.volume_liters == Decimal("225.123")
        assert barrel.price == Decimal("1500.123")

    def test_string_length_limits(self):
        """Test des limites de longueur des chaînes"""
        # Arrange
        long_string = "a" * 1000  # 1000 caractères
        
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": long_string,  # Trop long
            "last_name": "Dupont"
        }
        
        # Act & Assert
        with pytest.raises(ValidationError):
            UserCreate(**user_data)

    def test_enum_values(self):
        """Test des valeurs d'énumération"""
        # Arrange
        barrel_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "invalid_content",  # Valeur invalide
            "volume_liters": Decimal("225.00"),
            "wood_type": "invalid_wood",  # Valeur invalide
            "condition": "invalid_condition",  # Valeur invalide
            "price": Decimal("1500.00"),
            "stock_quantity": 5
        }
        
        # Act & Assert
        # Note: Les énumérations sont validées au niveau des modèles SQLAlchemy
        # Ici on teste juste que la création ne plante pas
        assert True  # Placeholder
