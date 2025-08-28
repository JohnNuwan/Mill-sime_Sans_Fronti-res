"""
Core - Millésime Sans Frontières
Module principal contenant toutes les fonctionnalités de base
"""

# Imports from constants
from .constants import (
    OrderStatus, PaymentStatus, QuoteStatus, UserRole,
    BarrelCondition, WoodType, PreviousContent, SecurityLevel
)

# Imports from database
from .database import (
    Base, engine, SessionLocal, get_db, create_tables, drop_tables
)

# Imports from config
from .config import settings

# Imports from auth
from .auth import (
    verify_password, get_password_hash, create_access_token, verify_token, 
    get_current_user, get_current_active_user, get_current_user_optional, is_token_expired
)

# Imports from security
from .security import (
    hash_password, generate_secure_token, validate_password_strength,
    sanitize_input, validate_file_upload, check_permissions, rate_limit_check, 
    validate_api_key, encrypt_sensitive_data, decrypt_sensitive_data,
    validate_csrf_token, generate_csrf_token, get_csrf_token_info, validate_session_token,
    validate_file_type, validate_file_size, validate_url, validate_ip_address,
    validate_phone_number, validate_credit_card, validate_postal_code,
    validate_tax_id, validate_iban, validate_swift_code,
    calculate_shipping_cost, calculate_insurance_cost,
    validate_volume, validate_weight, validate_price, validate_percentage
)

# Imports from utils
from .utils import (
    generate_uuid, generate_order_number, generate_quote_number,
    format_price, format_date, calculate_total_price,
    validate_phone_number as utils_validate_phone_number,
    sanitize_filename, chunk_list, deep_merge,
    get_current_timestamp, validate_email, format_currency,
    validate_url
)

# Imports from exceptions
from .exceptions import (
    BaseAppException, NotFoundException, ValidationException,
    AuthenticationException, AuthorizationException, BusinessLogicException,
    handle_app_exception
)

# Imports from rate_limiting
from .rate_limiting import rate_limit_middleware, get_rate_limit_info, reset_rate_limit

# Imports from cors
from .cors import setup_cors, get_cors_headers, validate_origin

# Imports from logging
from .logging import setup_logging, get_logger, log_request, log_response, log_error, log_performance

# Imports from monitoring
from .monitoring import setup_monitoring, get_metrics_summary, reset_metrics, record_request_metric, record_database_metric

# Imports from middleware_dependencies
from .middleware_dependencies import (
    setup_cors as setup_cors_middleware,
    setup_logging as setup_logging_middleware,
    setup_monitoring as setup_monitoring_middleware,
    rate_limit_middleware as rate_limit_middleware_dep,
    get_db_dependency, get_current_user_dependency,
    get_current_active_user_dependency, setup_middleware_order,
    setup_middleware_does_not_interfere, handle_rate_limiting_redis_error,
    handle_auth_dependency_malformed_token, handle_auth_dependency_expired_token,
    test_rate_limiting_middleware_performance, test_auth_dependency_performance
)

__all__ = [
    # Constants
    "OrderStatus", "PaymentStatus", "QuoteStatus", "UserRole",
    "BarrelCondition", "WoodType", "PreviousContent", "SecurityLevel",
    
    # Database
    "Base", "engine", "SessionLocal", "get_db", "create_tables", "drop_tables",
    
    # Config
    "settings",
    
    # Auth
    "verify_password", "get_password_hash", "create_access_token", "verify_token",
    "get_current_user", "get_current_active_user", "get_current_user_optional", "is_token_expired",
    
    # Security
    "hash_password", "generate_secure_token", "validate_password_strength",
    "sanitize_input", "validate_file_upload", "check_permissions", "rate_limit_check",
    "validate_api_key", "encrypt_sensitive_data", "decrypt_sensitive_data",
    "validate_csrf_token", "generate_csrf_token", "get_csrf_token_info", "validate_session_token",
    "validate_file_type", "validate_file_size", "validate_url", "validate_ip_address",
    "validate_phone_number", "validate_credit_card", "validate_postal_code",
    "validate_tax_id", "validate_iban", "validate_swift_code",
    "calculate_shipping_cost", "calculate_insurance_cost",
    "validate_volume", "validate_weight", "validate_price", "validate_percentage",
    
    # Utils
    "generate_uuid", "generate_order_number", "generate_quote_number",
    "format_price", "format_date", "calculate_total_price",
    "utils_validate_phone_number", "sanitize_filename", "chunk_list", "deep_merge",
    "get_current_timestamp", "validate_email", "format_currency", "validate_url",
    
    # Exceptions
    "BaseAppException", "NotFoundException", "ValidationException",
    "AuthenticationException", "AuthorizationException", "BusinessLogicException",
    "handle_app_exception",
    
    # Rate limiting functions
    "rate_limit_middleware", "get_rate_limit_info", "reset_rate_limit",
    
    # CORS functions
    "setup_cors", "get_cors_headers", "validate_origin",
    
    # Logging functions
    "setup_logging", "get_logger", "log_request", "log_response", "log_error", "log_performance",
    
    # Monitoring functions
    "setup_monitoring", "get_metrics_summary", "reset_metrics", "record_request_metric", "record_database_metric",
    
    # Middleware dependencies
    "setup_cors_middleware", "setup_logging_middleware", "setup_monitoring_middleware",
    "rate_limit_middleware_dep", "get_db_dependency", "get_current_user_dependency",
    "get_current_active_user_dependency", "setup_middleware_order",
    "setup_middleware_does_not_interfere", "handle_rate_limiting_redis_error",
    "handle_auth_dependency_malformed_token", "handle_auth_dependency_expired_token",
    "test_rate_limiting_middleware_performance", "test_auth_dependency_performance"
]
