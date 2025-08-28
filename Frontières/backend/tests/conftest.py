"""
Configuration des tests - Millésime Sans Frontières
Fixtures et configuration communes pour tous les tests
"""

import pytest
import asyncio
from typing import Generator, Dict, Any
from unittest.mock import Mock, patch
from decimal import Decimal
from datetime import datetime, date, timedelta
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.config import Settings
from app.models.user import User
from app.models.address import Address
from app.models.barrel import Barrel
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.quote import Quote
from app.models.quote_item import QuoteItem
from app.services.auth_service import AuthService


# Configuration de la base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Crée une boucle d'événements pour les tests asynchrones"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Crée une session de base de données de test"""
    # Créer toutes les tables
    Base.metadata.create_all(bind=engine)
    
    # Créer une session
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        # Supprimer toutes les tables
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Crée un client de test FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_settings() -> Settings:
    """Configuration de test"""
    return Settings(
        DEBUG=True,
        DATABASE_URL=SQLALCHEMY_DATABASE_URL,
        SECRET_KEY="test-secret-key-for-testing-only",
        ACCESS_TOKEN_EXPIRE_MINUTES=30,
        ALLOWED_HOSTS=["*"]
    )


# Fixtures pour les données de test
@pytest.fixture
def sample_user_data() -> Dict[str, Any]:
    """Données d'utilisateur de test"""
    return {
        "email": "test@example.com",
        "password_hash": "hashed_password_123",  # Hash simulé pour les tests
        "first_name": "Jean",
        "last_name": "Dupont",
        "company_name": "Test Company",
        "phone_number": "+33123456789",
        "role": "customer"
    }


@pytest.fixture
def sample_address_data() -> Dict[str, Any]:
    """Données d'adresse de test"""
    return {
        "address_line_1": "123 Rue de la Paix",
        "city": "Paris",
        "postal_code": "75001",
        "country": "France",
        "address_type": "shipping"
    }


@pytest.fixture
def sample_barrel_data() -> Dict[str, Any]:
    """Données de tonneau de test"""
    return {
        "name": "Fût Chêne Premium",
        "origin_country": "France",
        "previous_content": "red_wine",
        "volume_liters": Decimal("225.00"),
        "wood_type": "oak",
        "condition": "excellent",
        "price": Decimal("1500.00"),
        "stock_quantity": 5,
        "description": "Fût de chêne premium en excellent état",
        "weight_kg": Decimal("45.00")
    }


@pytest.fixture
def sample_order_data() -> Dict[str, Any]:
    """Données de commande de test"""
    return {
        "shipping_address_id": str(uuid.uuid4()),
        "billing_address_id": str(uuid.uuid4()),
        "notes": "Commande de test",
        "shipping_method": "standard",
        "payment_method": "card",
        "items": [
            {
                "barrel_id": str(uuid.uuid4()),
                "quantity": 2,
                "unit_price": Decimal("1500.00")
            }
        ]
    }


@pytest.fixture
def sample_quote_data() -> Dict[str, Any]:
    """Données de devis de test"""
    return {
        "valid_until": date.today() + timedelta(days=30),
        "shipping_cost": Decimal("50.00"),
        "tax_percentage": Decimal("20.00"),
        "discount_percentage": Decimal("5.00"),
        "items": [
            {
                "barrel_id": str(uuid.uuid4()),
                "quantity": 3,
                "unit_price": Decimal("1400.00")
            }
        ]
    }


# Fixtures pour les objets de base de données
@pytest.fixture
def test_user(db_session: Session, sample_user_data: Dict[str, Any]) -> User:
    """Crée un utilisateur de test en base"""
    user = User(**sample_user_data)
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_address(db_session: Session, test_user: User, sample_address_data: Dict[str, Any]) -> Address:
    """Crée une adresse de test en base"""
    address = Address(**sample_address_data, user_id=test_user.id)
    db_session.add(address)
    db_session.commit()
    db_session.refresh(address)
    return address


@pytest.fixture
def test_barrel(db_session: Session, sample_barrel_data: Dict[str, Any]) -> Barrel:
    """Crée un tonneau de test en base"""
    barrel = Barrel(**sample_barrel_data)
    db_session.add(barrel)
    db_session.commit()
    db_session.refresh(barrel)
    return barrel


@pytest.fixture
def test_order(db_session: Session, test_user: User, test_address: Address, test_barrel: Barrel) -> Order:
    """Crée une commande de test en base"""
    order = Order(
        user_id=test_user.id,
        shipping_address_id=test_address.id,
        billing_address_id=test_address.id,
        order_number="ORD-TEST-001",
        status="pending",
        payment_status="pending",
        subtotal=Decimal("3000.00"),
        total_amount=Decimal("3000.00"),
        shipping_cost=Decimal("0.00"),
        tax_amount=Decimal("0.00"),
        discount_amount=Decimal("0.00")
    )
    db_session.add(order)
    db_session.commit()
    db_session.refresh(order)
    
    # Créer un élément de commande
    order_item = OrderItem(
        order_id=order.id,
        barrel_id=test_barrel.id,
        quantity=2,
        unit_price=Decimal("1500.00"),
        total_price=Decimal("3000.00")  # quantity * unit_price
    )
    db_session.add(order_item)
    db_session.commit()
    
    return order


@pytest.fixture
def test_quote(db_session: Session, test_user: User, test_barrel: Barrel) -> Quote:
    """Crée un devis de test en base"""
    quote = Quote(
        user_id=test_user.id,
        quote_number="QUO-TEST-001",
        status="draft",
        valid_until=date.today() + timedelta(days=30),
        subtotal=Decimal("4200.00"),
        discount_percentage=Decimal("5.00"),
        discount_amount=Decimal("210.00"),
        tax_percentage=Decimal("20.00"),
        tax_amount=Decimal("798.00"),
        total_amount=Decimal("4788.00")
    )
    db_session.add(quote)
    db_session.commit()
    db_session.refresh(quote)
    
    # Créer un élément de devis
    quote_item = QuoteItem(
        quote_id=quote.id,
        barrel_id=test_barrel.id,
        quantity=3,
        unit_price=Decimal("1400.00"),
        total_price=Decimal("4200.00")  # quantity * unit_price
    )
    db_session.add(quote_item)
    db_session.commit()
    
    return quote


# Fixtures pour les mocks
@pytest.fixture
def mock_auth_service():
    """Mock du service d'authentification"""
    with patch('app.services.auth_service.AuthService') as mock:
        yield mock


@pytest.fixture
def mock_user_service():
    """Mock du service utilisateur"""
    with patch('app.services.user_service.UserService') as mock:
        yield mock


@pytest.fixture
def mock_barrel_service():
    """Mock du service tonneau"""
    with patch('app.services.barrel_service.BarrelService') as mock:
        yield mock


@pytest.fixture
def mock_order_service():
    """Mock du service commande"""
    with patch('app.services.order_service.OrderService') as mock:
        yield mock


@pytest.fixture
def mock_quote_service():
    """Mock du service devis"""
    with patch('app.services.quote_service.QuoteService') as mock:
        yield mock


# Fixtures pour les tokens d'authentification
@pytest.fixture
def auth_headers(test_user: User) -> Dict[str, str]:
    """En-têtes d'authentification pour les tests"""
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(test_user: User) -> Dict[str, str]:
    """En-têtes d'authentification admin pour les tests"""
    test_user.role = "admin"
    token = AuthService.create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {token}"}


# Fixtures pour les tests d'API
@pytest.fixture
def api_client(client: TestClient) -> TestClient:
    """Client API de test avec gestion des erreurs"""
    return client


@pytest.fixture
def authenticated_client(client: TestClient, auth_headers: Dict[str, str]) -> TestClient:
    """Client API authentifié pour les tests"""
    client.headers.update(auth_headers)
    return client


@pytest.fixture
def admin_client(client: TestClient, admin_headers: Dict[str, str]) -> TestClient:
    """Client API admin pour les tests"""
    client.headers.update(admin_headers)
    return client


# Configuration des marqueurs pytest
def pytest_configure(config):
    """Configure les marqueurs pytest personnalisés"""
    config.addinivalue_line(
        "markers", "unit: marque les tests unitaires"
    )
    config.addinivalue_line(
        "markers", "integration: marque les tests d'intégration"
    )
    config.addinivalue_line(
        "markers", "slow: marque les tests lents"
    )
    config.addinivalue_line(
        "markers", "api: marque les tests des API"
    )
    config.addinivalue_line(
        "markers", "database: marque les tests de base de données"
    )
    config.addinivalue_line(
        "markers", "auth: marque les tests d'authentification"
    )
    config.addinivalue_line(
        "markers", "users: marque les tests des utilisateurs"
    )
    config.addinivalue_line(
        "markers", "barrels: marque les tests des tonneaux"
    )
    config.addinivalue_line(
        "markers", "orders: marque les tests des commandes"
    )
    config.addinivalue_line(
        "markers", "quotes: marque les tests des devis"
    )
