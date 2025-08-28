"""
Security - Millésime Sans Frontières
Fonctions de sécurité et validation
"""

import re
import hashlib
import secrets
import base64
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List
from passlib.context import CryptContext
import jwt
from app.core.auth import verify_password as auth_verify_password, create_access_token as auth_create_access_token
from app.core.rate_limiting import rate_limit_middleware

# Configuration du contexte de hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuration JWT
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Mock Redis client pour les tests
class MockRedisClient:
    def __init__(self):
        self.data = {}
    
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value, ex=None):
        self.data[key] = value
        return True
    
    def incr(self, key):
        if key not in self.data:
            self.data[key] = 0
        self.data[key] += 1
        return self.data[key]
    
    def expire(self, key, seconds):
        return True

redis_client = MockRedisClient()

# Configuration de validation des mots de passe
MIN_PASSWORD_LENGTH = 8
REQUIRED_CHARS = {
    "uppercase": r"[A-Z]",
    "lowercase": r"[a-z]",
    "digits": r"\d",
    "special": r"[!@#$%^&*(),.?\":{}|<>]"
}


def hash_password(password: str) -> str:
    """Hache un mot de passe"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un mot de passe"""
    if not plain_password or not hashed_password:
        return False
    try:
        return auth_verify_password(plain_password, hashed_password)
    except:
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = None) -> str:
    """Crée un token d'accès JWT"""
    if secret_key is None:
        secret_key = SECRET_KEY
    
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = None) -> str:
    """Crée un token de rafraîchissement JWT"""
    if expires_delta is None:
        expires_delta = timedelta(days=7)
    
    if secret_key is None:
        secret_key = SECRET_KEY
    
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, secret_key: str = None) -> dict:
    """Vérifie un token JWT"""
    if secret_key is None:
        secret_key = SECRET_KEY
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expiré")
    except jwt.JWTError:
        raise ValueError("Token invalide")


def generate_secure_token(length: int = 64) -> str:
    """Génère un token sécurisé aléatoire"""
    return secrets.token_urlsafe(length)


def validate_password_strength(password: str) -> Dict[str, Any]:
    """Valide la force d'un mot de passe"""
    if not password:
        return {"is_valid": False, "errors": ["Le mot de passe ne peut pas être vide"]}
    
    errors = []
    
    if len(password) < MIN_PASSWORD_LENGTH:
        errors.append(f"Le mot de passe doit contenir au moins {MIN_PASSWORD_LENGTH} caractères")
    
    for char_type, pattern in REQUIRED_CHARS.items():
        if not re.search(pattern, password):
            if char_type == "uppercase":
                errors.append("Le mot de passe doit contenir au moins une majuscule")
            elif char_type == "lowercase":
                errors.append("Le mot de passe doit contenir au moins une minuscule")
            elif char_type == "digits":
                errors.append("Le mot de passe doit contenir au moins un chiffre")
            elif char_type == "special":
                errors.append("Le mot de passe doit contenir au moins un caractère spécial")
    
    is_valid = len(errors) == 0
    
    score = 0
    if len(password) >= 8:
        score += 1
    if re.search(REQUIRED_CHARS["uppercase"], password):
        score += 1
    if re.search(REQUIRED_CHARS["lowercase"], password):
        score += 1
    if re.search(REQUIRED_CHARS["digits"], password):
        score += 1
    if re.search(REQUIRED_CHARS["special"], password):
        score += 1
    
    return {
        "is_valid": is_valid,
        "is_strong": is_valid and len(password) >= 12,
        "score": score,
        "has_uppercase": bool(re.search(REQUIRED_CHARS["uppercase"], password)),
        "has_lowercase": bool(re.search(REQUIRED_CHARS["lowercase"], password)),
        "has_digits": bool(re.search(REQUIRED_CHARS["digits"], password)),
        "has_special": bool(re.search(REQUIRED_CHARS["special"], password)),
        "length": len(password),
        "errors": errors
    }


def sanitize_input(input_string: str) -> str:
    """Nettoie une chaîne d'entrée pour éviter les injections SQL et HTML"""
    if input_string is None:
        return ""
    
    sanitized = input_string
    
    # Supprimer les balises HTML
    sanitized = re.sub(r'<[^>]+>', '', sanitized)
    
    # Supprimer les caractères dangereux pour SQL
    dangerous_chars = ["'", '"', ';', '--', '/*', '*/', 'xp_', 'sp_']
    for char in dangerous_chars:
        sanitized = sanitized.replace(char, '')
    
    return sanitized


def validate_file_upload(file: Any, file_size: int = None) -> Dict[str, Any]:
    """Valide un fichier uploadé"""
    if not file:
        return {"is_valid": False, "errors": ["Aucun fichier fourni"]}
    
    errors = []
    
    # Validation du nom de fichier
    if hasattr(file, 'filename') and file.filename:
        if not re.match(r'^[a-zA-Z0-9._-]+$', file.filename):
            errors.append("Nom de fichier invalide")
    else:
        errors.append("Nom de fichier manquant")
    
    # Validation de la taille
    if file_size and file_size > 10 * 1024 * 1024:  # 10MB
        errors.append("Fichier trop volumineux (max 10MB)")
    elif file_size and file_size <= 0:
        errors.append("Taille de fichier invalide")
    
    # Validation du type
    if hasattr(file, 'content_type'):
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        if file.content_type not in allowed_types:
            errors.append("Type de fichier non autorisé")
    
    is_valid = len(errors) == 0
    
    return {
        "is_valid": is_valid,
        "errors": errors
    }


def check_permissions(user_role: str, required_role: str) -> bool:
    """Vérifie les permissions d'un utilisateur"""
    if user_role is None:
        return False
    
    role_hierarchy = {
        "admin": 3,
        "manager": 2,
        "user": 1,
        "customer": 1
    }
    
    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level


def rate_limit_check(client_id: str, endpoint: str = "default") -> bool:
    """Vérifie la limitation de débit"""
    try:
        return rate_limit_middleware(client_id, endpoint)
    except ImportError:
        # Fallback si le module de rate limiting n'est pas disponible
        return True


def validate_api_key(api_key: str) -> bool:
    """Valide une clé API"""
    if not api_key:
        return False
    
    # Vérification basique (dans un vrai projet, vérifier en base)
    return len(api_key) >= 32 and api_key.startswith("msf_")

def get_api_key_info(api_key: str) -> Dict[str, Any]:
    """Récupère les informations d'une clé API"""
    if not api_key:
        return {"valid": False, "error": "Clé API manquante"}
    
    is_valid = validate_api_key(api_key)
    
    if not is_valid:
        return {"valid": False, "error": "Clé API invalide"}
    
    # Mock des informations de clé API
    return {
        "valid": True,
        "key_id": f"key_{api_key[:8]}",
        "permissions": ["read", "write"],
        "expires_at": None,
        "is_active": True
    }


def encrypt_sensitive_data(data: str, encryption_key: str = None) -> str:
    """Chiffre des données sensibles"""
    if encryption_key is None:
        encryption_key = SECRET_KEY
    
    # Chiffrement simple avec la clé (dans un vrai projet, utiliser une méthode plus sécurisée)
    # Utiliser la clé pour créer un hash unique
    key_hash = hashlib.md5(encryption_key.encode()).hexdigest()[:8]
    encoded_data = base64.b64encode(data.encode()).decode()
    return f"encrypted_{key_hash}_{encoded_data}"


def decrypt_sensitive_data(encrypted_data: str, encryption_key: str = None) -> str:
    """Déchiffre des données sensibles"""
    if encryption_key is None:
        encryption_key = SECRET_KEY
    
    if not encrypted_data.startswith("encrypted_"):
        raise ValueError("Format de données chiffrées invalide")
    
    # Déchiffrement simple
    encoded_data = encrypted_data[10:]  # Supprimer "encrypted_"
    try:
        decoded_data = base64.b64decode(encoded_data).decode()
        return decoded_data
    except:
        raise ValueError("Impossible de déchiffrer les données")


def generate_csrf_token() -> str:
    """Génère un token CSRF"""
    return secrets.token_urlsafe(32)


def validate_csrf_token(token: str, session_token: str) -> bool:
    """Valide un token CSRF"""
    if not token or not session_token:
        return False
    
    # Vérification simple (dans un vrai projet, vérifier en session)
    return token == session_token


def get_csrf_token_info(token: str) -> Dict[str, Any]:
    """Récupère les informations d'un token CSRF"""
    if not token:
        return {"valid": False, "error": "Token manquant"}
    
    return {
        "valid": len(token) >= 32,
        "length": len(token),
        "created_at": datetime.utcnow().isoformat()
    }


def validate_session_token(token: str) -> bool:
    """Valide un token de session"""
    if not token:
        return False
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("type") == "session"
    except:
        return False


def validate_file_type(filename: str, content_type: str) -> Dict[str, Any]:
    """Valide le type d'un fichier"""
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
    
    # Vérifier l'extension du fichier
    file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
    extension_allowed = file_extension in ['jpg', 'jpeg', 'png', 'gif', 'pdf']
    
    # Vérifier le type MIME
    mime_allowed = content_type in allowed_types
    
    is_valid = extension_allowed and mime_allowed
    errors = []
    
    if not extension_allowed:
        errors.append(f"Extension de fichier non autorisée: {file_extension}")
    if not mime_allowed:
        errors.append(f"Type MIME non autorisé: {content_type}")
    
    return {
        "is_valid": is_valid,
        "errors": errors
    }


def validate_file_size(file_size: int, max_size: int = 10 * 1024 * 1024) -> Dict[str, Any]:
    """Valide la taille d'un fichier"""
    is_valid = file_size <= max_size
    errors = [] if is_valid else [f"Fichier trop volumineux (max {max_size // (1024*1024)}MB)"]
    
    return {
        "is_valid": is_valid,
        "errors": errors
    }


def validate_url(url: str) -> bool:
    """Valide une URL"""
    if not url:
        return False
    
    # Regex pour valider les URLs (HTTP, HTTPS, FTP)
    url_pattern = r'^(https?|ftp)://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
    return bool(re.match(url_pattern, url))


def validate_ip_address(ip: str) -> bool:
    """Valide une adresse IP"""
    if not ip:
        return False
    
    # Regex pour IPv4
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, ip):
        parts = ip.split('.')
        return all(0 <= int(part) <= 255 for part in parts)
    
    # Regex pour IPv6 (simplifiée)
    ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return bool(re.match(ipv6_pattern, ip))


def validate_phone_number(phone: str) -> bool:
    """Valide un numéro de téléphone"""
    if not phone:
        return False
    
    # Supprimer les espaces et caractères spéciaux
    clean_phone = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Vérifier que c'est un nombre avec 10-15 chiffres
    return bool(re.match(r'^\d{10,15}$', clean_phone))


def validate_credit_card(card_number: str) -> bool:
    """Valide un numéro de carte de crédit (algorithme de Luhn)"""
    if not card_number:
        return False
    
    # Supprimer les espaces
    card_number = card_number.replace(" ", "")
    
    if not card_number.isdigit():
        return False
    
    if len(card_number) < 13 or len(card_number) > 19:
        return False
    
    # Algorithme de Luhn
    total = 0
    is_even = False
    
    for digit in reversed(card_number):
        d = int(digit)
        if is_even:
            d *= 2
            if d > 9:
                d -= 9
        total += d
        is_even = not is_even
    
    return total % 10 == 0


def validate_postal_code(postal_code: str) -> bool:
    """Valide un code postal"""
    if not postal_code:
        return False
    
    # Regex pour différents formats de codes postaux
    patterns = [
        r'^\d{5}$',  # Format français
        r'^\d{5}-\d{4}$',  # Format US étendu
        r'^[A-Z]\d[A-Z] \d[A-Z]\d$',  # Format canadien
        r'^\d{4} [A-Z]{2}$',  # Format néerlandais
        r'^\d{5}$',  # Format allemand
        r'^\d{5} \d{2}$',  # Format européen avec espace
    ]
    
    return any(re.match(pattern, postal_code) for pattern in patterns)


def validate_tax_id(tax_id: str) -> bool:
    """Valide un numéro de TVA/SIRET"""
    if not tax_id:
        return False
    
    # Supprimer les espaces et caractères spéciaux
    clean_id = re.sub(r'[\s\-]', '', tax_id)
    
    # Vérifier que c'est un nombre avec 9-14 chiffres
    return bool(re.match(r'^\d{9,14}$', clean_id))


def validate_iban(iban: str) -> bool:
    """Valide un numéro IBAN"""
    if not iban:
        return False
    
    # Supprimer les espaces
    clean_iban = iban.replace(" ", "").upper()
    
    # Vérifier la longueur (généralement 15-34 caractères)
    if len(clean_iban) < 15 or len(clean_iban) > 34:
        return False
    
    # Vérifier le format (2 lettres pour le pays + chiffres)
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$', clean_iban):
        return False
    
    # Vérifications spécifiques par pays
    country_code = clean_iban[:2]
    if country_code == "FR" and len(clean_iban) != 27:
        return False
    
    return True


def validate_swift_code(swift: str) -> bool:
    """Valide un code SWIFT/BIC"""
    if not swift:
        return False
    
    # Format: 4 lettres (banque) + 2 lettres (pays) + 2 lettres/chiffres (localisation) + 3 lettres/chiffres (succursale)
    swift_pattern = r'^[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}[A-Z0-9]{3}$'
    return bool(re.match(swift_pattern, swift))


def calculate_shipping_cost(weight: float, distance: float, service: str = "standard") -> float:
    """Calcule le coût de livraison"""
    base_cost = 5.0
    
    # Coût par kg
    weight_cost = weight * 2.0
    
    # Coût par km
    distance_cost = distance * 0.1
    
    # Multiplicateur selon le service
    service_multipliers = {
        "standard": 1.0,
        "express": 1.5,
        "premium": 2.0
    }
    
    multiplier = service_multipliers.get(service, 1.0)
    
    return (base_cost + weight_cost + distance_cost) * multiplier


def calculate_insurance_cost(value: float, coverage: str = "basic") -> float:
    """Calcule le coût d'assurance"""
    # Pourcentage selon la couverture
    coverage_percentages = {
        "basic": 0.01,      # 1%
        "standard": 0.015,  # 1.5%
        "premium": 0.025    # 2.5%
    }
    
    percentage = coverage_percentages.get(coverage, 0.01)
    return value * percentage


def validate_volume(volume: float, min_volume: float = 0.0, max_volume: float = 1000.0) -> bool:
    """Valide un volume"""
    return min_volume <= volume <= max_volume


def validate_weight(weight: float, min_weight: float = 0.0, max_weight: float = 1000.0) -> bool:
    """Valide un poids"""
    return min_weight <= weight <= max_weight


def validate_price(price: float, min_price: float = 0.0, max_price: float = 1000000.0) -> bool:
    """Valide un prix"""
    return min_price <= price <= max_price


def validate_percentage(percentage: float, min_percentage: float = 0.0, max_percentage: float = 100.0) -> bool:
    """Valide un pourcentage"""
    return min_percentage <= percentage <= max_percentage
