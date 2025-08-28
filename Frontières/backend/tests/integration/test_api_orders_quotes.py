"""
Tests d'intégration pour les API des commandes et devis - Millésime Sans Frontières
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal
from datetime import date, timedelta

from app.main import app
from app.core.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.models.barrel import Barrel
from app.models.user import User
from app.models.address import Address


class TestOrderAPI:
    """Tests d'intégration pour l'API des commandes"""

    def test_get_orders_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de commandes réussie"""
        # Act
        response = client.get("/api/v1/orders", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data

    def test_get_orders_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de récupération de commandes sans authentification"""
        # Act
        response = client.get("/api/v1/orders")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_get_orders_with_filters(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de commandes avec filtres"""
        # Act
        response = client.get("/api/v1/orders?status=pending", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_order_by_id_success(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de récupération de commande par ID réussie"""
        # Act
        response = client.get(f"/api/v1/orders/{test_order.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_order.id
        assert data["order_number"] == test_order.order_number

    def test_get_order_by_id_not_found(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de commande par ID non trouvée"""
        # Act
        response = client.get("/api/v1/orders/nonexistent-id", headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_create_order_success(self, client: TestClient, db_session: Session, test_user: User, test_address: Address, test_barrel: Barrel, auth_headers: dict):
        """Test de création de commande réussie"""
        # Arrange
        order_data = {
            "shipping_address_id": str(test_address.id),
            "billing_address_id": str(test_address.id),
            "notes": "Commande de test",
            "shipping_method": "standard",
            "payment_method": "card",
            "items": [
                {
                    "barrel_id": str(test_barrel.id),
                    "quantity": 2,
                    "unit_price": 1500.00
                }
            ]
        }
        
        # Act
        response = client.post("/api/v1/orders", json=order_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["notes"] == order_data["notes"]
        assert data["shipping_method"] == order_data["shipping_method"]
        assert data["payment_method"] == order_data["payment_method"]
        assert len(data["items"]) == 1
        assert "id" in data

    def test_create_order_invalid_data(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de création de commande avec données invalides"""
        # Arrange
        order_data = {
            "items": []  # Liste vide
        }
        
        # Act
        response = client.post("/api/v1/orders", json=order_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_update_order_success(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de mise à jour de commande réussie"""
        # Arrange
        update_data = {"notes": "Nouvelles notes"}
        
        # Act
        response = client.put(f"/api/v1/orders/{test_order.id}", json=update_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["notes"] == update_data["notes"]

    def test_update_order_status_success(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de mise à jour de statut de commande réussie"""
        # Arrange
        status_data = {"status": "confirmed"}
        
        # Act
        response = client.patch(f"/api/v1/orders/{test_order.id}/status", json=status_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == status_data["status"]

    def test_update_order_status_invalid_transition(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de mise à jour de statut avec transition invalide"""
        # Arrange
        status_data = {"status": "delivered"}  # Transition invalide depuis "pending"
        
        # Act
        response = client.patch(f"/api/v1/orders/{test_order.id}/status", json=status_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_delete_order_success(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de suppression de commande réussie"""
        # Arrange
        # S'assurer que la commande peut être annulée
        test_order.status = "pending"
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/orders/{test_order.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_delete_order_not_cancellable(self, client: TestClient, db_session: Session, test_order: Order, auth_headers: dict):
        """Test de suppression de commande non annulable"""
        # Arrange
        # S'assurer que la commande ne peut pas être annulée
        test_order.status = "shipped"
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/orders/{test_order.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_search_orders_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de recherche de commandes réussie"""
        # Act
        response = client.get("/api/v1/orders/search?q=ORD-001", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_orders_by_user_success(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de récupération de commandes par utilisateur réussie"""
        # Act
        response = client.get(f"/api/v1/orders/user/{test_user.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_orders_by_status_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de commandes par statut réussie"""
        # Act
        response = client.get("/api/v1/orders/status/pending", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_order_statistics_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération des statistiques de commandes réussie"""
        # Act
        response = client.get("/api/v1/orders/statistics", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "total_orders" in data
        assert "total_revenue" in data


class TestQuoteAPI:
    """Tests d'intégration pour l'API des devis"""

    def test_get_quotes_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de devis réussie"""
        # Act
        response = client.get("/api/v1/quotes", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data

    def test_get_quotes_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de récupération de devis sans authentification"""
        # Act
        response = client.get("/api/v1/quotes")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_get_quotes_with_filters(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de devis avec filtres"""
        # Act
        response = client.get("/api/v1/quotes?status=draft", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_quote_by_id_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de récupération de devis par ID réussie"""
        # Act
        response = client.get(f"/api/v1/quotes/{test_quote.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_quote.id
        assert data["quote_number"] == test_quote.quote_number

    def test_get_quote_by_id_not_found(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de devis par ID non trouvé"""
        # Act
        response = client.get("/api/v1/quotes/nonexistent-id", headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_create_quote_success(self, client: TestClient, db_session: Session, test_user: User, test_barrel: Barrel, auth_headers: dict):
        """Test de création de devis réussie"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "description": "Devis pour fûts de chêne",
            "valid_until": (date.today() + timedelta(days=30)).isoformat(),
            "terms_conditions": "Conditions standard",
            "notes": "Devis de test",
            "shipping_cost": 50.00,
            "tax_rate": 20.00,
            "discount_percentage": 5.00,
            "items": [
                {
                    "barrel_id": str(test_barrel.id),
                    "quantity": 3,
                    "unit_price": 1400.00,
                    "description": "Fûts de chêne premium"
                }
            ]
        }
        
        # Act
        response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == quote_data["title"]
        assert data["description"] == quote_data["description"]
        assert len(data["items"]) == 1
        assert "id" in data

    def test_create_quote_invalid_data(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de création de devis avec données invalides"""
        # Arrange
        quote_data = {
            "items": []  # Liste vide
        }
        
        # Act
        response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_create_quote_past_validity_date(self, client: TestClient, db_session: Session, test_user: User, test_barrel: Barrel, auth_headers: dict):
        """Test de création de devis avec date de validité dans le passé"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "valid_until": (date.today() - timedelta(days=1)).isoformat(),  # Hier
            "items": [
                {
                    "barrel_id": str(test_barrel.id),
                    "quantity": 3,
                    "unit_price": 1400.00
                }
            ]
        }
        
        # Act
        response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_update_quote_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de mise à jour de devis réussie"""
        # Arrange
        update_data = {"title": "Nouveau titre"}
        
        # Act
        response = client.put(f"/api/v1/quotes/{test_quote.id}", json=update_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]

    def test_update_quote_status_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de mise à jour de statut de devis réussie"""
        # Arrange
        status_data = {"status": "sent"}
        
        # Act
        response = client.patch(f"/api/v1/quotes/{test_quote.id}/status", json=status_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == status_data["status"]

    def test_update_quote_status_invalid_transition(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de mise à jour de statut avec transition invalide"""
        # Arrange
        status_data = {"status": "accepted"}  # Transition invalide depuis "draft"
        
        # Act
        response = client.patch(f"/api/v1/quotes/{test_quote.id}/status", json=status_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_send_quote_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test d'envoi de devis réussi"""
        # Arrange
        # S'assurer que le devis peut être envoyé
        test_quote.status = "draft"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/send", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "sent"

    def test_send_quote_wrong_status(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test d'envoi de devis avec mauvais statut"""
        # Arrange
        # S'assurer que le devis ne peut pas être envoyé
        test_quote.status = "sent"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/send", headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_convert_quote_to_order_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de conversion de devis en commande réussie"""
        # Arrange
        # S'assurer que le devis peut être converti
        test_quote.status = "accepted"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/convert", headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["order_number"] is not None

    def test_convert_quote_to_order_wrong_status(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de conversion de devis avec mauvais statut"""
        # Arrange
        # S'assurer que le devis ne peut pas être converti
        test_quote.status = "draft"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/convert", headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_delete_quote_success(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de suppression de devis réussie"""
        # Arrange
        # S'assurer que le devis peut être supprimé
        test_quote.status = "draft"
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/quotes/{test_quote.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_delete_quote_not_deletable(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test de suppression de devis non supprimable"""
        # Arrange
        # S'assurer que le devis ne peut pas être supprimé
        test_quote.status = "sent"
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/quotes/{test_quote.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_search_quotes_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de recherche de devis réussie"""
        # Act
        response = client.get("/api/v1/quotes/search?q=QUO-001", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_quotes_by_user_success(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test de récupération de devis par utilisateur réussie"""
        # Act
        response = client.get(f"/api/v1/quotes/user/{test_user.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_quotes_by_status_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération de devis par statut réussie"""
        # Act
        response = client.get("/api/v1/quotes/status/draft", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_expired_quotes_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération des devis expirés réussie"""
        # Act
        response = client.get("/api/v1/quotes/expired", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_quote_statistics_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération des statistiques de devis réussie"""
        # Act
        response = client.get("/api/v1/quotes/statistics", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "total_quotes" in data
        assert "total_value" in data

    def test_quote_validation_constraints(self, client: TestClient, db_session: Session, test_user: User, test_barrel: Barrel, auth_headers: dict):
        """Test des contraintes de validation des devis"""
        # Arrange
        test_cases = [
            {
                "valid_until": (date.today() - timedelta(days=1)).isoformat(),  # Date passée
                "expected_status": 422
            },
            {
                "tax_rate": 150.00,  # Taux > 100%
                "expected_status": 422
            },
            {
                "discount_percentage": 150.00,  # Remise > 100%
                "expected_status": 422
            }
        ]
        
        base_data = {
            "title": "Devis de test",
            "valid_until": (date.today() + timedelta(days=30)).isoformat(),
            "items": [
                {
                    "barrel_id": str(test_barrel.id),
                    "quantity": 3,
                    "unit_price": 1400.00
                }
            ]
        }
        
        # Act & Assert
        for test_case in test_cases:
            quote_data = {**base_data, **test_case}
            response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
            assert response.status_code == test_case["expected_status"]

    def test_quote_enum_validation(self, client: TestClient, db_session: Session, test_user: User, test_barrel: Barrel, auth_headers: dict):
        """Test de validation des énumérations des devis"""
        # Arrange
        test_cases = [
            {
                "status": "invalid_status",
                "expected_status": 422
            }
        ]
        
        base_data = {
            "title": "Devis de test",
            "valid_until": (date.today() + timedelta(days=30)).isoformat(),
            "items": [
                {
                    "barrel_id": str(test_barrel.id),
                    "quantity": 3,
                    "unit_price": 1400.00
                }
            ]
        }
        
        # Act & Assert
        for test_case in test_cases:
            quote_data = {**base_data, **test_case}
            response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
            assert response.status_code == test_case["expected_status"]


class TestOrderQuoteIntegration:
    """Tests d'intégration entre commandes et devis"""

    def test_convert_quote_to_order_creates_order_items(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test que la conversion de devis en commande crée les éléments de commande"""
        # Arrange
        test_quote.status = "accepted"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/convert", headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        order_data = response.json()
        assert "items" in order_data
        assert len(order_data["items"]) > 0

    def test_convert_quote_to_order_updates_quote_status(self, client: TestClient, db_session: Session, test_quote: Quote, auth_headers: dict):
        """Test que la conversion de devis en commande met à jour le statut du devis"""
        # Arrange
        test_quote.status = "accepted"
        db_session.commit()
        
        # Act
        response = client.post(f"/api/v1/quotes/{test_quote.id}/convert", headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        
        # Vérifier que le statut du devis a été mis à jour
        quote_response = client.get(f"/api/v1/quotes/{test_quote.id}", headers=auth_headers)
        assert quote_response.status_code == 200
        quote_data = quote_response.json()
        assert quote_data["status"] == "converted"

    def test_order_creation_requires_valid_barrel(self, client: TestClient, db_session: Session, test_user: User, test_address: Address, auth_headers: dict):
        """Test que la création de commande nécessite un tonneau valide"""
        # Arrange
        order_data = {
            "shipping_address_id": str(test_address.id),
            "billing_address_id": str(test_address.id),
            "items": [
                {
                    "barrel_id": "nonexistent-barrel-id",
                    "quantity": 2,
                    "unit_price": 1500.00
                }
            ]
        }
        
        # Act
        response = client.post("/api/v1/orders", json=order_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_quote_creation_requires_valid_barrel(self, client: TestClient, db_session: Session, test_user: User, auth_headers: dict):
        """Test que la création de devis nécessite un tonneau valide"""
        # Arrange
        quote_data = {
            "title": "Devis de test",
            "valid_until": (date.today() + timedelta(days=30)).isoformat(),
            "items": [
                {
                    "barrel_id": "nonexistent-barrel-id",
                    "quantity": 3,
                    "unit_price": 1400.00
                }
            ]
        }
        
        # Act
        response = client.post("/api/v1/quotes", json=quote_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
