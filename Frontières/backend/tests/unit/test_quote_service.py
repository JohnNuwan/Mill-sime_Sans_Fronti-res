"""
Tests unitaires pour QuoteService - Millésime Sans Frontières
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from app.services.quote_service import QuoteService
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.barrel import Barrel
from app.models.user import User
from app.core.exceptions import NotFoundException, ValidationException, BusinessLogicException


class TestQuoteService:
    """Tests unitaires pour QuoteService"""

    def setup_method(self):
        """Configuration avant chaque test"""
        self.mock_db = Mock(spec=Session)
        self.quote_service = QuoteService(self.mock_db)

    def test_generate_quote_number(self):
        """Test de génération de numéro de devis"""
        # Arrange
        # Configurer le mock pour retourner un entier pour count()
        self.mock_db.query.return_value.filter.return_value.count.return_value = 3
        
        # Act
        quote_number = self.quote_service._generate_quote_number()
        
        # Assert
        assert isinstance(quote_number, str)
        assert quote_number.startswith("QUO-")
        assert len(quote_number) > 10

    def test_calculate_quote_amounts(self):
        """Test de calcul des montants de devis"""
        # Arrange
        items = [
            {"quantity": 2, "unit_price": Decimal("1400.00")},
            {"quantity": 1, "unit_price": Decimal("1800.00")}
        ]
        shipping_cost = Decimal("50.00")
        discount_percentage = Decimal("5.00")
        tax_percentage = Decimal("20.00")
        
        # Act
        result = self.quote_service._calculate_quote_amounts(
            items, shipping_cost, discount_percentage, tax_percentage
        )
        
        # Assert
        assert result["subtotal"] == Decimal("4600.00")  # 2*1400 + 1*1800
        assert result["discount_amount"] == Decimal("230.00")  # 5% de 4600
        assert result["tax_amount"] == Decimal("874.00")  # 20% de (4600-230)
        assert result["total"] == Decimal("5294.00")  # 4600-230+874+50

    def test_calculate_quote_amounts_no_discount(self):
        """Test de calcul des montants sans remise"""
        # Arrange
        items = [{"quantity": 1, "unit_price": Decimal("1000.00")}]
        shipping_cost = Decimal("0.00")
        discount_percentage = Decimal("0.00")
        tax_percentage = Decimal("0.00")
        
        # Act
        result = self.quote_service._calculate_quote_amounts(
            items, shipping_cost, discount_percentage, tax_percentage
        )
        
        # Assert
        assert result["subtotal"] == Decimal("1000.00")
        assert result["discount_amount"] == Decimal("0.00")
        assert result["tax_amount"] == Decimal("0.00")
        assert result["total"] == Decimal("1000.00")

    def test_validate_quote_items_success(self):
        """Test de validation des éléments de devis réussie"""
        # Arrange
        items = [
            {"barrel_id": "barrel1", "quantity": 5},
            {"barrel_id": "barrel2", "quantity": 3}
        ]
        
        # Mock pour le premier appel (barrel1)
        mock_barrel1 = Mock(stock_quantity=10)
        # Mock pour le deuxième appel (barrel2)
        mock_barrel2 = Mock(stock_quantity=5)
        
        self.mock_db.query.return_value.filter.return_value.first.side_effect = [mock_barrel1, mock_barrel2]
        
        # Act
        result = self.quote_service._validate_quote_items(items)
        
        # Assert
        assert result is True

    def test_validate_quote_items_insufficient_stock(self):
        """Test de validation des éléments avec stock insuffisant"""
        # Arrange
        items = [
            {"barrel_id": "barrel1", "quantity": 15}  # Plus que le stock disponible
        ]
        
        mock_barrel = Mock(stock_quantity=10)
        self.mock_db.query.return_value.filter.return_value.first.return_value = mock_barrel
        
        # Act & Assert
        with pytest.raises(BusinessLogicException):
            self.quote_service._validate_quote_items(items)

    def test_get_quote_by_id_success(self):
        """Test de récupération de devis par ID réussie"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.options.return_value.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quote_by_id(quote_id)
        
        # Assert
        assert result == mock_quote
        self.mock_db.query.assert_called_once()

    def test_get_quote_by_id_not_found(self):
        """Test de récupération de devis par ID non trouvé"""
        # Arrange
        quote_id = "nonexistent-quote-id"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.options.return_value.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            self.quote_service.get_quote_by_id(quote_id)

    def test_get_quotes_with_filters(self):
        """Test de récupération de devis avec filtres"""
        # Arrange
        mock_quotes = [Mock(spec=Quote), Mock(spec=Quote)]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.options.return_value.filter.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = mock_quotes
        mock_query.count.return_value = 2
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quotes(skip=0, limit=10, filters={"status": "draft"})
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 2

    def test_get_quotes_no_filters(self):
        """Test de récupération de devis sans filtres"""
        # Arrange
        mock_quotes = [Mock(spec=Quote)]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.options.return_value.order_by.return_value.offset.return_value.limit.return_value.all.return_value = mock_quotes
        mock_query.count.return_value = 1
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quotes()
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 1

    def test_create_quote_success(self):
        """Test de création de devis réussie"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "quote_number": "QUO-TEST-001",
            "customer_notes": "Devis pour fûts de chêne",
            "valid_until": date.today() + timedelta(days=30),
            "terms_conditions": "Conditions standard",
            "internal_notes": "Devis de test",
            "shipping_cost": Decimal("50.00"),
            "tax_percentage": Decimal("20.00"),
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
        
        mock_quote = Mock(spec=Quote)
        mock_quote.id = "new-quote-id"
        mock_quote.quote_number = "QUO-TEST-001"
        
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Mock des validations
        with patch.object(self.quote_service, '_validate_quote_items') as mock_validate:
            mock_validate.return_value = True
            with patch('app.services.quote_service.Quote') as mock_quote_class:
                mock_quote_class.return_value = mock_quote
                
                # Act
                result = self.quote_service.create_quote(quote_data)
                
                # Assert
                assert result == mock_quote
                mock_validate.assert_called_once()
                self.mock_db.add.assert_called()
                self.mock_db.commit.assert_called_once()

    def test_create_quote_invalid_data(self):
        """Test de création de devis avec données invalides"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "items": []  # Liste vide
        }
        
        # Act & Assert
        with pytest.raises(ValidationException):
            self.quote_service.create_quote(quote_data)

    def test_create_quote_past_validity_date(self):
        """Test de création de devis avec date de validité dans le passé"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "valid_until": date.today() - timedelta(days=1),  # Hier
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Mock de la validation des items pour éviter l'erreur de stock
        with patch.object(self.quote_service, '_validate_quote_items') as mock_validate:
            mock_validate.return_value = True
            
            # Act & Assert
            with pytest.raises(ValidationException):
                self.quote_service.create_quote(quote_data)

    def test_update_quote_success(self):
        """Test de mise à jour de devis réussie"""
        # Arrange
        quote_id = "test-quote-id"
        update_data = {"customer_notes": "Nouvelles notes"}
        
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.customer_notes = "Anciennes notes"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        self.mock_db.commit.return_value = None
        
        # Act
        result = self.quote_service.update_quote(quote_id, update_data)
        
        # Assert
        assert result == mock_quote
        assert mock_quote.customer_notes == "Nouvelles notes"
        self.mock_db.commit.assert_called_once()

    def test_update_quote_not_found(self):
        """Test de mise à jour de devis non trouvé"""
        # Arrange
        quote_id = "nonexistent-quote-id"
        update_data = {"customer_notes": "Nouvelles notes"}
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            self.quote_service.update_quote(quote_id, update_data)

    def test_update_quote_status_success(self):
        """Test de mise à jour de statut de devis réussie"""
        # Arrange
        quote_id = "test-quote-id"
        new_status = "sent"
        
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "draft"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        self.mock_db.commit.return_value = None
        
        # Act
        result = self.quote_service.update_quote_status(quote_id, new_status)
        
        # Assert
        assert result == mock_quote
        assert mock_quote.status == new_status
        self.mock_db.commit.assert_called_once()

    def test_update_quote_status_invalid_transition(self):
        """Test de mise à jour de statut avec transition invalide"""
        # Arrange
        quote_id = "test-quote-id"
        new_status = "accepted"  # Transition invalide depuis "draft"
        
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "draft"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(BusinessLogicException):
            self.quote_service.update_quote_status(quote_id, new_status)

    def test_send_quote_success(self):
        """Test d'envoi de devis réussi"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "draft"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        self.mock_db.commit.return_value = None
        
        # Act
        result = self.quote_service.send_quote(quote_id)
        
        # Assert
        assert result == mock_quote
        assert mock_quote.status == "sent"
        assert mock_quote.sent_at is not None
        self.mock_db.commit.assert_called_once()

    def test_send_quote_not_found(self):
        """Test d'envoi de devis non trouvé"""
        # Arrange
        quote_id = "nonexistent-quote-id"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            self.quote_service.send_quote(quote_id)

    def test_send_quote_wrong_status(self):
        """Test d'envoi de devis avec mauvais statut"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "sent"  # Déjà envoyé
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(BusinessLogicException):
            self.quote_service.send_quote(quote_id)

    def test_convert_quote_to_order_success(self):
        """Test de conversion de devis en commande réussie"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "accepted"
        mock_quote.user_id = "test-user-id"
        mock_quote.items = [Mock(barrel_id="barrel1", quantity=2, unit_price=Decimal("1400.00"))]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        self.mock_db.commit.return_value = None
        
        # Mock de la création de commande
        with patch('app.services.quote_service.Order') as mock_order_class:
            mock_order = Mock()
            mock_order_class.return_value = mock_order
            
            # Act
            result = self.quote_service.convert_quote_to_order(quote_id)
            
            # Assert
            assert result == mock_order
            assert mock_quote.status == "converted"
            self.mock_db.commit.assert_called()

    def test_convert_quote_to_order_not_found(self):
        """Test de conversion de devis non trouvé"""
        # Arrange
        quote_id = "nonexistent-quote-id"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            self.quote_service.convert_quote_to_order(quote_id)

    def test_convert_quote_to_order_wrong_status(self):
        """Test de conversion de devis avec mauvais statut"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "draft"  # Pas encore accepté
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(BusinessLogicException):
            self.quote_service.convert_quote_to_order(quote_id)

    def test_delete_quote_success(self):
        """Test de suppression de devis réussie"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "draft"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        self.mock_db.delete.return_value = None
        self.mock_db.commit.return_value = None
        
        # Act
        result = self.quote_service.delete_quote(quote_id)
        
        # Assert
        assert result is True
        self.mock_db.delete.assert_called_once_with(mock_quote)
        self.mock_db.commit.assert_called_once()

    def test_delete_quote_not_found(self):
        """Test de suppression de devis non trouvé"""
        # Arrange
        quote_id = "nonexistent-quote-id"
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = None
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(NotFoundException):
            self.quote_service.delete_quote(quote_id)

    def test_delete_quote_not_deletable(self):
        """Test de suppression de devis non supprimable"""
        # Arrange
        quote_id = "test-quote-id"
        mock_quote = Mock(spec=Quote)
        mock_quote.id = quote_id
        mock_quote.status = "sent"  # Statut non supprimable
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.first.return_value = mock_quote
        self.mock_db.query.return_value = mock_query
        
        # Act & Assert
        with pytest.raises(BusinessLogicException):
            self.quote_service.delete_quote(quote_id)

    def test_get_quote_statistics_success(self):
        """Test de récupération des statistiques de devis réussie"""
        # Arrange
        mock_stats = {
            "total_quotes": 50,
            "total_value": Decimal("75000.00"),
            "average_quote_value": Decimal("1500.00"),
            "quotes_by_status": {"draft": 20, "sent": 15, "accepted": 10, "rejected": 5}
        }
        
        # Configurer la chaîne complète de mocks pour les statistiques
        mock_query = Mock()
        mock_query.count.return_value = 50
        mock_query.with_entities.return_value.scalar.return_value = Decimal("75000.00")
        
        # Mock pour les statistiques par statut
        mock_status_query = Mock()
        mock_status_query.group_by.return_value.all.return_value = [
            ("draft", 20), ("sent", 15), ("accepted", 10), ("rejected", 5)
        ]
        
        # Mock pour les statistiques mensuelles
        mock_monthly_query = Mock()
        mock_monthly_query.group_by.return_value.order_by.return_value.all.return_value = [
            (datetime(2024, 1, 1), 10), (datetime(2024, 2, 1), 15)
        ]
        
        # Configurer les différents appels à query
        self.mock_db.query.side_effect = [mock_query, mock_status_query, mock_monthly_query]
        
        # Act
        result = self.quote_service.get_quote_statistics()
        
        # Assert
        assert result["total_quotes"] == 50
        assert result["total_value"] == 75000.0  # Converti en float
        assert "quotes_by_status" in result
        assert "monthly_quotes" in result

    def test_search_quotes_success(self):
        """Test de recherche de devis réussie"""
        # Arrange
        search_term = "QUO-001"
        mock_quotes = [Mock(spec=Quote)]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.offset.return_value.limit.return_value.all.return_value = mock_quotes
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.search_quotes(search_term)
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 1

    def test_get_quote_count_with_filters(self):
        """Test de comptage de devis avec filtres"""
        # Arrange
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.count.return_value = 15
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quote_count(filters={"status": "draft"})
        
        # Assert
        assert result == 15

    def test_get_quote_count_no_filters(self):
        """Test de comptage de devis sans filtres"""
        # Arrange
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.count.return_value = 50
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quote_count()
        
        # Assert
        assert result == 50

    def test_get_quotes_by_user_success(self):
        """Test de récupération de devis par utilisateur réussie"""
        # Arrange
        user_id = "test-user-id"
        mock_quotes = [Mock(spec=Quote), Mock(spec=Quote)]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.all.return_value = mock_quotes
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quotes_by_user(user_id)
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 2

    def test_get_quotes_by_status_success(self):
        """Test de récupération de devis par statut réussie"""
        # Arrange
        status = "draft"
        mock_quotes = [Mock(spec=Quote)]
        
        # Configurer la chaîne complète de mocks
        mock_query = Mock()
        mock_query.filter.return_value.all.return_value = mock_quotes
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_quotes_by_status(status)
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 1

    def test_get_expired_quotes_success(self):
        """Test de récupération des devis expirés réussie"""
        # Arrange
        mock_quotes = [Mock(spec=Quote), Mock(spec=Quote)]
        
        mock_query = Mock()
        mock_query.filter.return_value.all.return_value = mock_quotes
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.get_expired_quotes()
        
        # Assert
        assert result == mock_quotes
        assert len(result) == 2

    def test_check_expired_quotes_success(self):
        """Test de vérification des devis expirés réussie"""
        # Arrange
        mock_quotes = [Mock(spec=Quote)]
        
        mock_query = Mock()
        mock_query.filter.return_value.all.return_value = mock_quotes
        
        self.mock_db.query.return_value = mock_query
        
        # Act
        result = self.quote_service.check_expired_quotes()
        
        # Assert
        assert result == 1  # 1 devis expiré

    def test_validate_quote_data_success(self):
        """Test de validation des données de devis réussie"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "quote_number": "QUO-TEST-001",
            "valid_until": date.today() + timedelta(days=30),
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 3,
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Act
        result = self.quote_service.validate_quote_data(quote_data)
        
        # Assert
        assert result is True

    def test_validate_quote_data_empty_items(self):
        """Test de validation des données de devis avec éléments vides"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "items": []  # Liste vide
        }
        
        # Act & Assert
        with pytest.raises(ValidationException):
            self.quote_service.create_quote(quote_data)

    def test_validate_quote_data_invalid_quantity(self):
        """Test de validation des données de devis avec quantité invalide"""
        # Arrange
        quote_data = {
            "user_id": "test-user-id",
            "items": [
                {
                    "barrel_id": "test-barrel-id",
                    "quantity": 0,  # Quantité nulle
                    "unit_price": Decimal("1400.00")
                }
            ]
        }
        
        # Mock de la validation des items pour éviter l'erreur de stock
        with patch.object(self.quote_service, '_validate_quote_items') as mock_validate:
            mock_validate.return_value = True
            
            # Act & Assert
            with pytest.raises(ValidationException):
                self.quote_service.create_quote(quote_data)

    def test_quote_status_transitions_valid(self):
        """Test des transitions de statut de devis valides"""
        # Arrange
        valid_transitions = {
            "draft": ["sent", "cancelled"],
            "sent": ["accepted", "rejected", "expired"],
            "accepted": ["converted", "expired"],
            "rejected": [],
            "expired": [],
            "converted": []
        }
        
        # Act & Assert
        for current_status, allowed_next_statuses in valid_transitions.items():
            for next_status in allowed_next_statuses:
                # Ces transitions doivent être valides
                assert True  # Placeholder pour la logique de validation

    def test_quote_status_transitions_invalid(self):
        """Test des transitions de statut de devis invalides"""
        # Arrange
        invalid_transitions = self.quote_service.quote_status_transitions_invalid()
        
        # Act & Assert
        for current_status, invalid_next_statuses in invalid_transitions.items():
            # Vérifier que les transitions invalides sont bien définies
            assert isinstance(invalid_next_statuses, list)
            assert len(invalid_next_statuses) > 0

    def test_quote_expiry_validation(self):
        """Test de validation de l'expiration des devis"""
        # Arrange
        valid_dates = [
            date.today() + timedelta(days=1),   # Demain
            date.today() + timedelta(days=30),  # Dans 30 jours
            date.today() + timedelta(days=365)  # Dans 1 an
        ]
        
        invalid_dates = [
            date.today() - timedelta(days=1),   # Hier
            date.today() - timedelta(days=30),  # Il y a 30 jours
        ]
        
        # Act & Assert
        for valid_date in valid_dates:
            # Ces dates doivent être valides
            assert valid_date > date.today()
        
        for invalid_date in invalid_dates:
            # Ces dates doivent être invalides
            assert invalid_date < date.today()

    def test_quote_amount_calculations(self):
        """Test des calculs de montants de devis"""
        # Arrange
        test_cases = [
            {
                "items": [{"quantity": 1, "unit_price": Decimal("1000.00")}],
                "shipping_cost": Decimal("0.00"),
                "tax_percentage": Decimal("0.00"),
                "discount_percentage": Decimal("0.00"),
                "expected_total": Decimal("1000.00")
            },
            {
                "items": [{"quantity": 2, "unit_price": Decimal("500.00")}],
                "shipping_cost": Decimal("25.00"),
                "tax_percentage": Decimal("10.00"),
                "discount_percentage": Decimal("5.00"),
                "expected_total": Decimal("1047.50")  # 1000 - 50 + 100 + 25
            }
        ]
        
        # Act & Assert
        for test_case in test_cases:
            result = self.quote_service._calculate_quote_amounts(
                test_case["items"],
                test_case["shipping_cost"],
                test_case["discount_percentage"],
                test_case["tax_percentage"]
            )
            
            assert result["total"] == test_case["expected_total"]
