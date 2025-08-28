"""
Module d'utilitaires
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union
from decimal import Decimal

def generate_uuid() -> str:
    """Génère un UUID unique"""
    return str(uuid.uuid4())

def generate_order_number() -> str:
    """Génère un numéro de commande unique"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4())[:8]
    return f"ORD-{timestamp}-{random_part}"

def generate_quote_number() -> str:
    """Génère un numéro de devis unique"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_part = str(uuid.uuid4())[:8]
    return f"QT-{timestamp}-{random_part}"

def format_price(price: Union[float, Decimal], currency: str = "€") -> str:
    """Formate un prix avec la devise"""
    if isinstance(price, str):
        price = float(price)
    return f"{price:.2f} {currency}"

def format_date(date: Union[str, datetime], format_str: str = "%Y-%m-%d") -> str:
    """Formate une date"""
    if isinstance(date, str):
        date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    return date.strftime(format_str)

def calculate_total_price(items: List[Dict[str, Any]]) -> Decimal:
    """Calcule le prix total d'une liste d'articles"""
    total = Decimal('0.00')
    for item in items:
        price = Decimal(str(item.get('price', 0)))
        quantity = int(item.get('quantity', 1))
        total += price * quantity
    return total

def validate_phone_number(phone: str) -> bool:
    """Valide un numéro de téléphone"""
    import re
    # Supprime les espaces et caractères spéciaux
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    # Vérifie que c'est un numéro valide (8-15 chiffres)
    return re.match(r'^\d{8,15}$', cleaned) is not None

def sanitize_filename(filename: str) -> str:
    """Nettoie un nom de fichier"""
    import re
    # Remplace les caractères non autorisés
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limite la longueur
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        filename = name[:255-len(ext)-1] + ('.' + ext if ext else '')
    return filename

def chunk_list(items: List[Any], chunk_size: int) -> List[List[Any]]:
    """Divise une liste en chunks de taille donnée"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

def deep_merge(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """Fusionne deux dictionnaires en profondeur"""
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

def get_current_timestamp() -> datetime:
    """Retourne le timestamp actuel en UTC"""
    return datetime.now(timezone.utc)

def is_valid_email(email: str) -> bool:
    """Valide le format d'un email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def format_currency(amount: Union[float, Decimal], currency: str = "€") -> str:
    """Formate un montant en devise (alias pour compatibilité)"""
    return format_price(amount, currency)

def validate_email(email: str) -> bool:
    """Valide un email (alias pour compatibilité)"""
    return is_valid_email(email)

def validate_phone(phone: str) -> bool:
    """Valide un numéro de téléphone (alias pour compatibilité)"""
    return validate_phone_number(phone)

def calculate_tax(amount: Union[float, Decimal], tax_rate: float = 0.20) -> Decimal:
    """Calcule la taxe sur un montant"""
    if isinstance(amount, str):
        amount = Decimal(str(amount))
    return Decimal(str(amount)) * Decimal(str(tax_rate))

def calculate_discount(amount: Union[float, Decimal], discount_percentage: float) -> Decimal:
    """Calcule la remise sur un montant"""
    if isinstance(amount, str):
        amount = Decimal(str(amount))
    discount_rate = Decimal(str(discount_percentage)) / Decimal('100')
    return Decimal(str(amount)) * discount_rate

def validate_date_range(start_date: Union[str, datetime], end_date: Union[str, datetime]) -> bool:
    """Valide qu'une plage de dates est valide"""
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    
    return start_date < end_date

def sanitize_string(input_string: str) -> str:
    """Nettoie une chaîne de caractères (alias pour compatibilité)"""
    if input_string is None:
        return ""
    from .security import sanitize_input
    return sanitize_input(input_string)

def validate_postal_code(postal_code: str) -> bool:
    """Valide un code postal"""
    if not postal_code:
        return False
    
    postal_code = postal_code.strip()
    import re
    
    # Format français (5 chiffres)
    if re.match(r'^\d{5}$', postal_code):
        return True
    
    # Format US (5 chiffres ou 5-4)
    if re.match(r'^\d{5}(-\d{4})?$', postal_code):
        return True
    
    # Format canadien (A1B 2C3)
    if re.match(r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$', postal_code.upper()):
        return True
    
    # Format européen (lettres et chiffres, 3-10 caractères)
    if re.match(r'^[A-Z0-9]{3,10}$', postal_code.upper()):
        return True
    
    return False

def validate_country_code(country_code: str) -> bool:
    """Valide un code pays ISO 3166-1 alpha-2"""
    if not country_code or len(country_code) != 2:
        return False
    import re
    return re.match(r'^[A-Z]{2}$', country_code.upper()) is not None

def validate_currency_code(currency_code: str) -> bool:
    """Valide un code devise ISO 4217"""
    if not currency_code or len(currency_code) != 3:
        return False
    import re
    return re.match(r'^[A-Z]{3}$', currency_code.upper()) is not None

def validate_language_code(language_code: str) -> bool:
    """Valide un code langue ISO 639-1"""
    if not language_code or len(language_code) != 2:
        return False
    import re
    return re.match(r'^[a-z]{2}$', language_code.lower()) is not None

def calculate_shipping_cost(weight_kg: float, distance_km: float, shipping_method: str = "standard") -> Decimal:
    """Calcule le coût de livraison"""
    base_rate = Decimal('15.00')  # Taux de base en euros
    
    # Coût par kg par km
    weight_rate = Decimal(str(weight_kg)) * Decimal('0.05')
    
    # Coût par km
    distance_rate = Decimal(str(distance_km)) * Decimal('0.10')
    
    # Multiplicateur selon la méthode de livraison
    method_multipliers = {
        "standard": Decimal('1.0'),
        "express": Decimal('1.5'),
        "premium": Decimal('2.0')
    }
    
    multiplier = method_multipliers.get(shipping_method, Decimal('1.0'))
    
    total_cost = (base_rate + weight_rate + distance_rate) * multiplier
    
    # Arrondir à 2 décimales
    return total_cost.quantize(Decimal('0.01'))

def calculate_insurance_cost(item_value: Decimal, insurance_type: str = "basic") -> Decimal:
    """Calcule le coût de l'assurance"""
    insurance_rates = {
        "basic": Decimal('0.02'),      # 2%
        "standard": Decimal('0.03'),   # 3%
        "premium": Decimal('0.05')     # 5%
    }
    
    rate = insurance_rates.get(insurance_type, Decimal('0.02'))
    return (item_value * rate).quantize(Decimal('0.01'))

def validate_volume(volume: Union[float, Decimal, str]) -> bool:
    """Valide un volume"""
    try:
        if isinstance(volume, str):
            volume = Decimal(volume)
        elif isinstance(volume, float):
            volume = Decimal(str(volume))
        elif isinstance(volume, Decimal):
            pass
        else:
            return False
        
        return volume > 0 and volume <= Decimal('1000.0')
    except (ValueError, TypeError):
        return False

def validate_weight(weight: Union[float, Decimal, str]) -> bool:
    """Valide un poids"""
    try:
        if isinstance(weight, str):
            weight = Decimal(weight)
        elif isinstance(weight, float):
            weight = Decimal(str(weight))
        elif isinstance(weight, Decimal):
            pass
        else:
            return False
        
        return weight > 0 and weight <= Decimal('1000.0')
    except (ValueError, TypeError):
        return False

def validate_price(price: Union[float, Decimal, str]) -> bool:
    """Valide un prix"""
    try:
        if isinstance(price, str):
            price = Decimal(price)
        elif isinstance(price, float):
            price = Decimal(str(price))
        elif isinstance(price, Decimal):
            pass
        else:
            return False
        
        return price >= Decimal('0.01') and price <= Decimal('999999.99')
    except (ValueError, TypeError):
        return False

def validate_percentage(percentage: Union[float, Decimal, str]) -> bool:
    """Valide un pourcentage"""
    try:
        if isinstance(percentage, str):
            percentage = Decimal(percentage)
        elif isinstance(percentage, float):
            percentage = Decimal(str(percentage))
        elif isinstance(percentage, Decimal):
            pass
        else:
            return False
        
        return percentage >= Decimal('0.0') and percentage <= Decimal('100.0')
    except (ValueError, TypeError):
        return False

def generate_password_hash(password: str) -> str:
    """Génère un hash de mot de passe"""
    from .auth import get_password_hash
    return get_password_hash(password)

def verify_password_hash(plain_password: str, hashed_password: str) -> bool:
    """Vérifie un hash de mot de passe"""
    from .auth import verify_password
    return verify_password(plain_password, hashed_password)

def generate_secure_filename(original_filename: str) -> str:
    """Génère un nom de fichier sécurisé"""
    import os
    import uuid
    from datetime import datetime
    
    # Récupère l'extension
    _, ext = os.path.splitext(original_filename)
    
    # Génère un nom unique avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{timestamp}_{unique_id}{ext}"

def generate_jwt_token(payload: dict, secret_key: str, algorithm: str = "HS256", expires_in: int = 3600) -> str:
    """Génère un token JWT"""
    from .auth import create_access_token
    from datetime import timedelta
    
    expires_delta = timedelta(seconds=expires_in)
    return create_access_token(payload, expires_delta)

def verify_jwt_token(token: str, secret_key: str) -> dict:
    """Vérifie un token JWT"""
    from .auth import verify_token
    return verify_token(token)

def generate_api_key(prefix: str = "msf") -> str:
    """Génère une clé API sécurisée"""
    import secrets
    import string
    
    # Génère 32 caractères aléatoires
    alphabet = string.ascii_letters + string.digits
    random_part = ''.join(secrets.choice(alphabet) for _ in range(32))
    
    return f"{prefix}_{random_part}"

def decode_jwt_token(token: str, secret_key: str) -> dict:
    """Décode un token JWT"""
    from .auth import verify_token
    return verify_token(token)

def extract_jwt_payload(token: str) -> dict:
    """Extrait le payload d'un token JWT sans vérification"""
    import jwt
    from .constants import JWT_SECRET_KEY, JWT_ALGORITHM
    
    try:
        # Décode sans vérifier la signature (pour debug uniquement)
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except jwt.InvalidTokenError:
        return {}

def validate_jwt_format(token: str) -> bool:
    """Valide le format d'un token JWT"""
    if not token:
        return False
    
    # Vérifie qu'il y a 3 parties séparées par des points
    parts = token.split('.')
    if len(parts) != 3:
        return False
    
    # Vérifie que chaque partie est en base64
    import base64
    try:
        for part in parts:
            base64.b64decode(part + '==')  # Ajoute le padding
        return True
    except Exception:
        return False

def paginate_results(items: list, page: int = 1, size: int = 20) -> dict:
    """Pagine une liste de résultats"""
    from .constants import MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE
    
    # Validation des paramètres
    if page < 1:
        page = 1
    if size < 1:
        size = DEFAULT_PAGE_SIZE
    if size > MAX_PAGE_SIZE:
        size = MAX_PAGE_SIZE
    
    total = len(items)
    start = (page - 1) * size
    end = start + size
    
    # Calcul du nombre total de pages
    pages = (total + size - 1) // size
    
    # Extraction des éléments de la page
    page_items = items[start:end]
    
    return {
        "items": page_items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1
    }

def apply_filters(items: list, filters: dict) -> list:
    """Applique des filtres à une liste d'éléments"""
    if not filters:
        return items
    
    filtered_items = items.copy()
    
    for key, value in filters.items():
        if value is None:
            continue
            
        if isinstance(value, str) and value.strip() == "":
            continue
            
        # Filtrage basique par attribut
        filtered_items = [
            item for item in filtered_items 
            if hasattr(item, key) and getattr(item, key) == value
        ]
    
    return filtered_items

def sort_results(items: list, sort_by: str = None, sort_order: str = "asc") -> list:
    """Trie une liste de résultats"""
    if not items or not sort_by:
        return items
    
    # Vérifie que l'attribut de tri existe
    if not hasattr(items[0], sort_by):
        return items
    
    # Tri par attribut
    reverse = sort_order.lower() == "desc"
    
    try:
        sorted_items = sorted(items, key=lambda x: getattr(x, sort_by), reverse=reverse)
        return sorted_items
    except (TypeError, AttributeError):
        # En cas d'erreur de tri, retourne la liste originale
        return items

def search_results(items: list, search_term: str, search_fields: list = None) -> list:
    """Recherche dans une liste de résultats"""
    if not items or not search_term:
        return items
    
    search_term = search_term.lower().strip()
    if not search_term:
        return items
    
    # Champs de recherche par défaut
    if search_fields is None:
        search_fields = ["name", "description", "email"]
    
    # Recherche dans les champs spécifiés
    results = []
    for item in items:
        for field in search_fields:
            if hasattr(item, field):
                value = getattr(item, field)
                if value and search_term in str(value).lower():
                    results.append(item)
                    break
    
    return results

def validate_pagination_params(page: int, size: int) -> tuple[int, int]:
    """Valide et normalise les paramètres de pagination"""
    from .constants import MAX_PAGE_SIZE, DEFAULT_PAGE_SIZE
    
    # Validation de la page
    if page < 1:
        page = 1
    
    # Validation de la taille
    if size < 1:
        size = DEFAULT_PAGE_SIZE
    if size > MAX_PAGE_SIZE:
        size = MAX_PAGE_SIZE
    
    return page, size

def get_pagination_info(total: int, page: int, size: int) -> dict:
    """Génère les informations de pagination"""
    pages = (total + size - 1) // size if total > 0 else 0
    
    return {
        "total": total,
        "page": page,
        "size": size,
        "pages": pages,
        "has_next": page < pages,
        "has_prev": page > 1,
        "start_item": (page - 1) * size + 1 if total > 0 else 0,
        "end_item": min(page * size, total)
    }

def validate_url(url: str) -> bool:
    """Valide une URL"""
    if not url:
        return False
    
    import re
    # Pattern pour valider les URLs (incluant FTP)
    url_pattern = re.compile(
        r'^(https?|ftp)://'  # http://, https:// ou ftp://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domaine
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # port optionnel
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return bool(url_pattern.match(url))
