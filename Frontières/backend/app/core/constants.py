"""
Constantes et enums - Millésime Sans Frontières
Définitions centralisées des valeurs constantes
"""

from enum import Enum
from typing import List
from decimal import Decimal


class OrderStatus(str, Enum):
    """Statuts possibles d'une commande"""
    PENDING = "pending"           # En attente
    PROCESSING = "processing"     # En cours de traitement
    SHIPPED = "shipped"          # Expédiée
    DELIVERED = "delivered"      # Livrée
    CANCELLED = "cancelled"      # Annulée
    RETURNED = "returned"        # Retournée


class PaymentStatus(str, Enum):
    """Statuts possibles du paiement"""
    PENDING = "pending"          # En attente
    PAID = "paid"               # Payé
    FAILED = "failed"           # Échoué
    REFUNDED = "refunded"       # Remboursé
    PARTIALLY_REFUNDED = "partially_refunded"  # Partiellement remboursé


class QuoteStatus(str, Enum):
    """Statuts possibles d'un devis"""
    DRAFT = "draft"             # Brouillon
    SENT = "sent"               # Envoyé
    VIEWED = "viewed"           # Consulté
    ACCEPTED = "accepted"       # Accepté
    REJECTED = "rejected"       # Rejeté
    EXPIRED = "expired"         # Expiré
    CONVERTED = "converted"     # Converti en commande
    CANCELLED = "cancelled"     # Annulé


class UserRole(str, Enum):
    """Rôles possibles des utilisateurs"""
    ADMIN = "admin"             # Administrateur
    MANAGER = "manager"         # Gestionnaire
    SALES = "sales"             # Commercial
    CUSTOMER = "customer"       # Client
    GUEST = "guest"             # Invité


class BarrelCondition(str, Enum):
    """États possibles des tonneaux"""
    EXCELLENT = "excellent"     # Excellent
    GOOD = "good"               # Bon
    FAIR = "fair"               # Moyen
    POOR = "poor"               # Mauvais
    DAMAGED = "damaged"         # Endommagé


class WoodType(str, Enum):
    """Types de bois possibles"""
    OAK = "oak"                 # Chêne
    CHESTNUT = "chestnut"       # Châtaignier
    ACACIA = "acacia"           # Acacia
    CHERRY = "cherry"           # Cerisier
    ASH = "ash"                 # Frêne
    OTHER = "other"             # Autre


class PreviousContent(str, Enum):
    """Contenus précédents possibles"""
    RED_WINE = "red_wine"       # Vin rouge
    WHITE_WINE = "white_wine"   # Vin blanc
    ROSÉ_WINE = "rose_wine"     # Vin rosé
    CHAMPAGNE = "champagne"     # Champagne
    COGNAC = "cognac"           # Cognac
    WHISKEY = "whiskey"         # Whisky
    RUM = "rum"                 # Rhum
    OTHER = "other"             # Autre


# Constantes de pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
PAGINATION_DEFAULT_LIMIT = DEFAULT_PAGE_SIZE
PAGINATION_MAX_LIMIT = MAX_PAGE_SIZE

# Constantes de validation
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
PASSWORD_MIN_LENGTH = MIN_PASSWORD_LENGTH
PASSWORD_MAX_LENGTH = MAX_PASSWORD_LENGTH
MAX_EMAIL_LENGTH = 255
EMAIL_MAX_LENGTH = MAX_EMAIL_LENGTH
MAX_NAME_LENGTH = 100
NAME_MAX_LENGTH = MAX_NAME_LENGTH
MAX_COMPANY_NAME_LENGTH = 200
MAX_PHONE_LENGTH = 20
PHONE_MAX_LENGTH = MAX_PHONE_LENGTH
ADDRESS_MAX_LENGTH = 255
DESCRIPTION_MAX_LENGTH = 1000
NOTES_MAX_LENGTH = 500

# Constantes de prix
MIN_PRICE = Decimal('0.01')
MAX_PRICE = Decimal('999999.99')
MIN_VOLUME = Decimal('0.1')
MAX_VOLUME = Decimal('1000.0')
MIN_WEIGHT = Decimal('0.1')
MAX_WEIGHT = Decimal('1000.0')
MIN_STOCK = 0
MAX_STOCK = 999999

# Constantes spécifiques aux fûts
BARREL_MIN_VOLUME = Decimal('5.0')      # 5 litres minimum
BARREL_MAX_VOLUME = Decimal('500.0')    # 500 litres maximum
BARREL_MIN_PRICE = Decimal('50.0')      # 50€ minimum
BARREL_MAX_PRICE = Decimal('50000.0')   # 50000€ maximum
BARREL_MIN_STOCK = 0                    # Stock minimum
BARREL_MAX_STOCK = 9999                 # Stock maximum

# Constantes spécifiques aux commandes
ORDER_MIN_QUANTITY = 1                  # Quantité minimum par article
ORDER_MAX_QUANTITY = 1000               # Quantité maximum par article
ORDER_MIN_AMOUNT = Decimal('10.0')      # Montant minimum de commande
ORDER_MAX_AMOUNT = Decimal('100000.0')  # Montant maximum de commande

# Constantes spécifiques aux devis
QUOTE_MIN_VALIDITY_DAYS = 1             # Validité minimum en jours
QUOTE_MAX_VALIDITY_DAYS = 365           # Validité maximum en jours (1 an)
QUOTE_DEFAULT_VALIDITY_DAYS = 30        # Validité par défaut en jours
QUOTE_MIN_DISCOUNT_PERCENTAGE = 0.0     # Remise minimum en pourcentage
QUOTE_MAX_DISCOUNT_PERCENTAGE = 50.0    # Remise maximum en pourcentage
QUOTE_MIN_TAX_PERCENTAGE = 0.0          # Taxe minimum en pourcentage
QUOTE_MAX_TAX_PERCENTAGE = 30.0         # Taxe maximum en pourcentage

# Constantes de stock
MIN_STOCK_QUANTITY = 0
MAX_STOCK_QUANTITY = 999999

# Constantes de volume
MIN_VOLUME_LITERS = 0.1
MAX_VOLUME_LITERS = 10000.0

# Constantes de poids
MIN_WEIGHT_KG = 0.1
MAX_WEIGHT_KG = 10000.0

# Constantes de dates
QUOTE_DEFAULT_VALIDITY_DAYS = 30
ORDER_EXPIRY_DAYS = 7

# Constantes de fichiers
MAX_FILE_SIZE_MB = 10
ALLOWED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp"]
MAX_IMAGES_PER_BARREL = 10

# Constantes de sécurité
JWT_SECRET_KEY = "your-secret-key-here"
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
JWT_REFRESH_TOKEN_EXPIRE_DAYS = 7

# Constantes de cache
REDIS_DEFAULT_TTL = 3600  # 1 heure
REDIS_USER_TTL = 1800     # 30 minutes
REDIS_BARREL_TTL = 7200   # 2 heures

# Constantes d'API
API_VERSION = "v1"
API_PREFIX = f"/api/{API_VERSION}"

# Constantes de notification
EMAIL_NOTIFICATIONS_ENABLED = True
SMS_NOTIFICATIONS_ENABLED = False
PUSH_NOTIFICATIONS_ENABLED = False

# Constantes de monitoring
HEALTH_CHECK_INTERVAL = 60  # secondes
METRICS_COLLECTION_INTERVAL = 300  # secondes

# Constantes de déploiement
ENVIRONMENT = "development"  # development, staging, production
DEBUG_MODE = True
LOG_LEVEL = "INFO"

# Constantes de base de données
DB_POOL_SIZE = 20
DB_MAX_OVERFLOW = 30
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600

# Constantes de Redis
REDIS_POOL_SIZE = 10
REDIS_SOCKET_TIMEOUT = 5
REDIS_SOCKET_CONNECT_TIMEOUT = 5

# Constantes de CORS
ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Frontend local
    "http://localhost:8000",      # Backend local
    "https://millesime-sans-frontieres.com",  # Production
    "https://www.millesime-sans-frontieres.com"
]

ALLOWED_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
ALLOWED_HEADERS = ["*"]

# Constantes de rate limiting
RATE_LIMIT_REQUESTS = 100  # requêtes par minute
RATE_LIMIT_WINDOW = 60     # secondes

# Constantes de validation des données
MAX_SEARCH_TERM_LENGTH = 100
MAX_FILTER_VALUES = 50
MAX_BATCH_SIZE = 1000

# Constantes de formatage
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
CURRENCY_FORMAT = "€"
DECIMAL_PLACES = 2

# Constantes de localisation
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ["en", "fr", "es", "de"]
DEFAULT_TIMEZONE = "UTC"
SUPPORTED_TIMEZONES = ["UTC", "Europe/Paris", "America/New_York", "Asia/Tokyo"]

# Constantes de métriques
METRICS_ENABLED = True
METRICS_PORT = 9090
METRICS_PATH = "/metrics"

# Constantes de logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "logs/app.log"
LOG_MAX_SIZE = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5


class SecurityLevel(str, Enum):
    """Niveaux de sécurité"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    
    @property
    def description(self) -> str:
        """Description du niveau de sécurité"""
        descriptions = {
            "low": "Niveau de sécurité bas - accès public",
            "medium": "Niveau de sécurité moyen - accès authentifié",
            "high": "Niveau de sécurité élevé - accès restreint",
            "critical": "Niveau de sécurité critique - accès très restreint"
        }
        return descriptions.get(self.value, "Niveau de sécurité inconnu")
    
    @property
    def threshold(self) -> int:
        """Seuil numérique du niveau de sécurité"""
        thresholds = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }
        return thresholds.get(self.value, 0)
    
    def __lt__(self, other):
        """Permet la comparaison des niveaux de sécurité"""
        if not isinstance(other, SecurityLevel):
            return NotImplemented
        return self.threshold < other.threshold
