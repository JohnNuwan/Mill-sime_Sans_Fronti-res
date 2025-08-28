"""
Tests d'intégration pour l'API des tonneaux - Millésime Sans Frontières
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decimal import Decimal

from app.main import app
from app.core.database import get_db
from app.models.barrel import Barrel
from app.models.user import User


class TestBarrelAPI:
    """Tests d'intégration pour l'API des tonneaux"""

    def test_get_barrels_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux réussie"""
        # Act
        response = client.get("/api/v1/barrels")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data
        assert "page" in data
        assert "size" in data

    def test_get_barrels_with_pagination(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux avec pagination"""
        # Act
        response = client.get("/api/v1/barrels?page=1&size=5")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["page"] == 1
        assert data["size"] == 5

    def test_get_barrels_with_filters(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux avec filtres"""
        # Act
        response = client.get("/api/v1/barrels?wood_type=oak&condition=excellent")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_barrel_by_id_success(self, client: TestClient, db_session: Session, test_barrel: Barrel):
        """Test de récupération de tonneau par ID réussie"""
        # Act
        response = client.get(f"/api/v1/barrels/{test_barrel.id}")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_barrel.id
        assert data["name"] == test_barrel.name
        assert data["origin_country"] == test_barrel.origin_country

    def test_get_barrel_by_id_not_found(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneau par ID non trouvé"""
        # Act
        response = client.get("/api/v1/barrels/nonexistent-id")
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_create_barrel_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de création de tonneau réussie"""
        # Arrange
        barrel_data = {
            "name": "Nouveau Fût",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": 225.00,
            "wood_type": "oak",
            "condition": "excellent",
            "price": 1500.00,
            "stock_quantity": 5,
            "description": "Fût de chêne premium",
            "dimensions": "H: 95cm, D: 60cm",
            "weight_kg": 45.00
        }
        
        # Act
        response = client.post("/api/v1/barrels", json=barrel_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == barrel_data["name"]
        assert data["origin_country"] == barrel_data["origin_country"]
        assert data["previous_content"] == barrel_data["previous_content"]
        assert data["volume_liters"] == barrel_data["volume_liters"]
        assert data["wood_type"] == barrel_data["wood_type"]
        assert data["condition"] == barrel_data["condition"]
        assert data["price"] == barrel_data["price"]
        assert data["stock_quantity"] == barrel_data["stock_quantity"]
        assert "id" in data

    def test_create_barrel_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de création de tonneau sans authentification"""
        # Arrange
        barrel_data = {
            "name": "Nouveau Fût",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": 225.00,
            "wood_type": "oak",
            "condition": "excellent",
            "price": 1500.00,
            "stock_quantity": 5
        }
        
        # Act
        response = client.post("/api/v1/barrels", json=barrel_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_create_barrel_invalid_data(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de création de tonneau avec données invalides"""
        # Arrange
        barrel_data = {
            "name": "",  # Nom vide
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": -1,  # Volume négatif
            "wood_type": "oak",
            "condition": "excellent",
            "price": 0,  # Prix nul
            "stock_quantity": -1  # Stock négatif
        }
        
        # Act
        response = client.post("/api/v1/barrels", json=barrel_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_update_barrel_success(self, client: TestClient, db_session: Session, test_barrel: Barrel, auth_headers: dict):
        """Test de mise à jour de tonneau réussie"""
        # Arrange
        update_data = {
            "price": 1600.00,
            "stock_quantity": 10
        }
        
        # Act
        response = client.put(f"/api/v1/barrels/{test_barrel.id}", json=update_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == update_data["price"]
        assert data["stock_quantity"] == update_data["stock_quantity"]

    def test_update_barrel_not_found(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de mise à jour de tonneau non trouvé"""
        # Arrange
        update_data = {"price": 1600.00}
        
        # Act
        response = client.put("/api/v1/barrels/nonexistent-id", json=update_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_update_barrel_unauthenticated(self, client: TestClient, db_session: Session, test_barrel: Barrel):
        """Test de mise à jour de tonneau sans authentification"""
        # Arrange
        update_data = {"price": 1600.00}
        
        # Act
        response = client.put(f"/api/v1/barrels/{test_barrel.id}", json=update_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_delete_barrel_success(self, client: TestClient, db_session: Session, test_barrel: Barrel, auth_headers: dict):
        """Test de suppression de tonneau réussie"""
        # Arrange
        # S'assurer que le tonneau n'a pas de stock
        test_barrel.stock_quantity = 0
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/barrels/{test_barrel.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data

    def test_delete_barrel_not_found(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de suppression de tonneau non trouvé"""
        # Act
        response = client.delete("/api/v1/barrels/nonexistent-id", headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_delete_barrel_with_stock(self, client: TestClient, db_session: Session, test_barrel: Barrel, auth_headers: dict):
        """Test de suppression de tonneau avec stock"""
        # Arrange
        # S'assurer que le tonneau a du stock
        test_barrel.stock_quantity = 5
        db_session.commit()
        
        # Act
        response = client.delete(f"/api/v1/barrels/{test_barrel.id}", headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_delete_barrel_unauthenticated(self, client: TestClient, db_session: Session, test_barrel: Barrel):
        """Test de suppression de tonneau sans authentification"""
        # Act
        response = client.delete(f"/api/v1/barrels/{test_barrel.id}")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_search_barrels_success(self, client: TestClient, db_session: Session):
        """Test de recherche de tonneaux réussie"""
        # Act
        response = client.get("/api/v1/barrels/search?q=chêne")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_search_barrels_empty_query(self, client: TestClient, db_session: Session):
        """Test de recherche de tonneaux avec requête vide"""
        # Act
        response = client.get("/api/v1/barrels/search?q=")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_origin_countries_success(self, client: TestClient, db_session: Session):
        """Test de récupération des pays d'origine réussie"""
        # Act
        response = client.get("/api/v1/barrels/origin-countries")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_wood_types_success(self, client: TestClient, db_session: Session):
        """Test de récupération des types de bois réussie"""
        # Act
        response = client.get("/api/v1/barrels/wood-types")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_barrels_by_condition_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux par condition réussie"""
        # Act
        response = client.get("/api/v1/barrels/condition/excellent")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_barrels_by_condition_invalid(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux par condition invalide"""
        # Act
        response = client.get("/api/v1/barrels/condition/invalid-condition")
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_get_barrels_by_price_range_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux par gamme de prix réussie"""
        # Act
        response = client.get("/api/v1/barrels/price-range?min_price=1000&max_price=2000")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_barrels_by_price_range_invalid(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux par gamme de prix invalide"""
        # Act
        response = client.get("/api/v1/barrels/price-range?min_price=2000&max_price=1000")
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_get_barrels_by_volume_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux par volume réussie"""
        # Act
        response = client.get("/api/v1/barrels/volume-range?min_volume=200&max_volume=300")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_available_barrels_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux disponibles réussie"""
        # Act
        response = client.get("/api/v1/barrels/available")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_low_stock_barrels_success(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux en stock limité réussie"""
        # Act
        response = client.get("/api/v1/barrels/low-stock?threshold=3")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_get_low_stock_barrels_default_threshold(self, client: TestClient, db_session: Session):
        """Test de récupération de tonneaux en stock limité avec seuil par défaut"""
        # Act
        response = client.get("/api/v1/barrels/low-stock")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data

    def test_update_stock_success(self, client: TestClient, db_session: Session, test_barrel: Barrel, auth_headers: dict):
        """Test de mise à jour du stock réussie"""
        # Arrange
        stock_data = {"quantity_change": 5}
        
        # Act
        response = client.patch(f"/api/v1/barrels/{test_barrel.id}/stock", json=stock_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "stock_quantity" in data

    def test_update_stock_insufficient(self, client: TestClient, db_session: Session, test_barrel: Barrel, auth_headers: dict):
        """Test de mise à jour du stock insuffisant"""
        # Arrange
        stock_data = {"quantity_change": -15}  # Diminution de 15
        
        # S'assurer que le tonneau n'a que 10 en stock
        test_barrel.stock_quantity = 10
        db_session.commit()
        
        # Act
        response = client.patch(f"/api/v1/barrels/{test_barrel.id}/stock", json=stock_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data

    def test_update_stock_not_found(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de mise à jour du stock de tonneau non trouvé"""
        # Arrange
        stock_data = {"quantity_change": 5}
        
        # Act
        response = client.patch("/api/v1/barrels/nonexistent-id/stock", json=stock_data, headers=auth_headers)
        
        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    def test_update_stock_unauthenticated(self, client: TestClient, db_session: Session, test_barrel: Barrel):
        """Test de mise à jour du stock sans authentification"""
        # Arrange
        stock_data = {"quantity_change": 5}
        
        # Act
        response = client.patch(f"/api/v1/barrels/{test_barrel.id}/stock", json=stock_data)
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_get_barrel_statistics_success(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de récupération des statistiques de tonneaux réussie"""
        # Act
        response = client.get("/api/v1/barrels/statistics", headers=auth_headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "total_barrels" in data
        assert "total_value" in data
        assert "average_price" in data

    def test_get_barrel_statistics_unauthenticated(self, client: TestClient, db_session: Session):
        """Test de récupération des statistiques sans authentification"""
        # Act
        response = client.get("/api/v1/barrels/statistics")
        
        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "detail" in data

    def test_get_barrel_count_success(self, client: TestClient, db_session: Session):
        """Test de comptage de tonneaux réussie"""
        # Act
        response = client.get("/api/v1/barrels/count")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)

    def test_get_barrel_count_with_filters(self, client: TestClient, db_session: Session):
        """Test de comptage de tonneaux avec filtres réussie"""
        # Act
        response = client.get("/api/v1/barrels/count?wood_type=oak")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert isinstance(data["count"], int)

    def test_barrel_validation_constraints(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test des contraintes de validation des tonneaux"""
        # Arrange
        test_cases = [
            {
                "name": "",  # Nom vide
                "expected_status": 422
            },
            {
                "volume_liters": -1,  # Volume négatif
                "expected_status": 422
            },
            {
                "price": 0,  # Prix nul
                "expected_status": 422
            },
            {
                "stock_quantity": -1,  # Stock négatif
                "expected_status": 422
            }
        ]
        
        base_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": 225.00,
            "wood_type": "oak",
            "condition": "excellent",
            "price": 1500.00,
            "stock_quantity": 5
        }
        
        # Act & Assert
        for test_case in test_cases:
            barrel_data = {**base_data, **test_case}
            response = client.post("/api/v1/barrels", json=barrel_data, headers=auth_headers)
            assert response.status_code == test_case["expected_status"]

    def test_barrel_enum_validation(self, client: TestClient, db_session: Session, auth_headers: dict):
        """Test de validation des énumérations des tonneaux"""
        # Arrange
        test_cases = [
            {
                "wood_type": "invalid_wood",
                "expected_status": 422
            },
            {
                "condition": "invalid_condition",
                "expected_status": 422
            },
            {
                "previous_content": "invalid_content",
                "expected_status": 422
            }
        ]
        
        base_data = {
            "name": "Fût de Test",
            "origin_country": "France",
            "previous_content": "red_wine",
            "volume_liters": 225.00,
            "wood_type": "oak",
            "condition": "excellent",
            "price": 1500.00,
            "stock_quantity": 5
        }
        
        # Act & Assert
        for test_case in test_cases:
            barrel_data = {**base_data, **test_case}
            response = client.post("/api/v1/barrels", json=barrel_data, headers=auth_headers)
            assert response.status_code == test_case["expected_status"]

    def test_barrel_pagination_limits(self, client: TestClient, db_session: Session):
        """Test des limites de pagination des tonneaux"""
        # Act
        response = client.get("/api/v1/barrels?size=1000")  # Taille trop grande
        
        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_barrel_search_special_characters(self, client: TestClient, db_session: Session):
        """Test de recherche avec caractères spéciaux"""
        # Act
        response = client.get("/api/v1/barrels/search?q=chêne&é")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
