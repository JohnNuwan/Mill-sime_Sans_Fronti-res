"""
Tests unitaires pour la sécurité et les validations - Millésime Sans Frontières
"""

import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta
import re
from decimal import Decimal

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
    generate_secure_token,
    validate_password_strength,
    sanitize_input,
    validate_file_upload,
    check_permissions,
    rate_limit_check,
    validate_api_key,
    encrypt_sensitive_data,
    decrypt_sensitive_data,
    validate_csrf_token,
    generate_csrf_token,
    validate_file_type,
    validate_file_size,
    validate_url,
    validate_ip_address,
    validate_phone_number,
    validate_postal_code,
    validate_credit_card,
    validate_iban
)
from app.core.constants import UserRole, SecurityLevel


class TestPasswordSecurity:
    """Tests pour la sécurité des mots de passe"""

    def test_hash_password_creates_hash(self):
        """Test que hash_password crée un hash sécurisé"""
        # Arrange
        password = "MySecurePassword123!"
        
        # Act
        hashed = hash_password(password)
        
        # Assert
        assert hashed != password
        assert len(hashed) > 50  # Hash bcrypt typique
        assert hashed.startswith("$2b$")  # Format bcrypt

    def test_verify_password_correct_password(self):
        """Test de vérification avec mot de passe correct"""
        # Arrange
        password = "MySecurePassword123!"
        hashed = hash_password(password)
        
        # Act
        result = verify_password(password, hashed)
        
        # Assert
        assert result is True

    def test_verify_password_incorrect_password(self):
        """Test de vérification avec mot de passe incorrect"""
        # Arrange
        correct_password = "MySecurePassword123!"
        incorrect_password = "WrongPassword123!"
        hashed = hash_password(correct_password)
        
        # Act
        result = verify_password(incorrect_password, hashed)
        
        # Assert
        assert result is False

    def test_hash_password_unique_for_same_password(self):
        """Test que le même mot de passe génère des hash différents"""
        # Arrange
        password = "MySecurePassword123!"
        
        # Act
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        
        # Assert
        assert hash1 != hash2  # Salt différent à chaque fois

    def test_verify_password_with_none_values(self):
        """Test de vérification avec valeurs None"""
        # Act & Assert
        assert verify_password(None, "hash") is False
        assert verify_password("password", None) is False
        assert verify_password(None, None) is False


class TestTokenSecurity:
    """Tests pour la sécurité des tokens"""

    def test_create_access_token_creates_valid_token(self):
        """Test que create_access_token crée un token valide"""
        # Arrange
        data = {"sub": "user123", "email": "user@example.com"}
        secret_key = "test_secret_key"
        expires_delta = timedelta(minutes=30)
        
        # Act
        token = create_access_token(data, secret_key, expires_delta)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_refresh_token_creates_valid_token(self):
        """Test que create_refresh_token crée un token valide"""
        # Arrange
        data = {"sub": "user123"}
        secret_key = "test_secret_key"
        expires_delta = timedelta(days=7)
        
        # Act
        token = create_refresh_token(data, secret_key, expires_delta)
        
        # Assert
        assert isinstance(token, str)
        assert len(token) > 0

    def test_verify_token_valid_token(self):
        """Test de vérification d'un token valide"""
        # Arrange
        data = {"sub": "user123"}
        secret_key = "test_secret_key"
        expires_delta = timedelta(minutes=30)
        token = create_access_token(data, secret_key, expires_delta)
        
        # Act
        result = verify_token(token, secret_key)
        
        # Assert
        assert result["sub"] == "user123"

    def test_verify_token_expired_token(self):
        """Test de vérification d'un token expiré"""
        # Arrange
        data = {"sub": "user123"}
        secret_key = "test_secret_key"
        expires_delta = timedelta(milliseconds=1)  # Expire très rapidement
        
        token = create_access_token(data, secret_key, expires_delta)
        
        # Act & Assert
        import time
        time.sleep(0.1)  # Attendre que le token expire
        
        with pytest.raises(Exception):
            verify_token(token, secret_key)

    def test_verify_token_invalid_token(self):
        """Test de vérification d'un token invalide"""
        # Arrange
        invalid_token = "invalid.jwt.token"
        secret_key = "test_secret_key"
        
        # Act & Assert
        with pytest.raises(Exception):
            verify_token(invalid_token, secret_key)

    def test_verify_token_wrong_secret(self):
        """Test de vérification avec une mauvaise clé secrète"""
        # Arrange
        data = {"sub": "user123"}
        correct_secret = "correct_secret"
        wrong_secret = "wrong_secret"
        token = create_access_token(data, correct_secret)
        
        # Act & Assert
        with pytest.raises(Exception):
            verify_token(token, wrong_secret)


class TestSecureTokenGeneration:
    """Tests pour la génération de tokens sécurisés"""

    def test_generate_secure_token_creates_token(self):
        """Test que generate_secure_token crée un token"""
        # Act
        token = generate_secure_token()
        
        # Assert
        assert isinstance(token, str)
        assert len(token) >= 32  # Token d'au moins 32 caractères

    def test_generate_secure_token_unique(self):
        """Test que generate_secure_token génère des tokens uniques"""
        # Act
        token1 = generate_secure_token()
        token2 = generate_secure_token()
        
        # Assert
        assert token1 != token2

    def test_generate_secure_token_with_length(self):
        """Test de génération avec longueur personnalisée"""
        # Arrange
        length = 64
        
        # Act
        token = generate_secure_token(length=length)
        
        # Assert
        assert len(token) == length


class TestPasswordStrengthValidation:
    """Tests pour la validation de la force des mots de passe"""

    def test_validate_password_strength_strong_password(self):
        """Test de validation d'un mot de passe fort"""
        # Arrange
        strong_passwords = [
            "MySecurePassword123!",
            "Complex@Password#2023",
            "Str0ng!P@ssw0rd"
        ]
        
        # Act & Assert
        for password in strong_passwords:
            result = validate_password_strength(password)
            assert result["is_strong"] is True
            assert result["score"] >= 8

    def test_validate_password_strength_weak_password(self):
        """Test de validation d'un mot de passe faible"""
        # Arrange
        weak_passwords = [
            "password",
            "123456",
            "abc",
            "qwerty"
        ]
        
        # Act & Assert
        for password in weak_passwords:
            result = validate_password_strength(password)
            assert result["is_strong"] is False
            assert result["score"] < 6

    def test_validate_password_strength_requirements(self):
        """Test des exigences de force des mots de passe"""
        # Arrange
        password = "MySecurePassword123!"
        
        # Act
        result = validate_password_strength(password)
        
        # Assert
        assert result["has_uppercase"] is True
        assert result["has_lowercase"] is True
        assert result["has_digit"] is True
        assert result["has_special"] is True
        assert result["length_ok"] is True

    def test_validate_password_strength_edge_cases(self):
        """Test de cas limites pour la validation de force"""
        # Arrange
        edge_cases = [
            "",  # Mot de passe vide
            "a" * 100,  # Mot de passe très long
            "1234567890",  # Seulement des chiffres
            "ABCDEFGHIJ",  # Seulement des majuscules
        ]
        
        # Act & Assert
        for password in edge_cases:
            result = validate_password_strength(password)
            assert isinstance(result, dict)
            assert "is_strong" in result
            assert "score" in result


class TestInputSanitization:
    """Tests pour la sanitisation des entrées"""

    def test_sanitize_input_removes_html(self):
        """Test de suppression des balises HTML"""
        # Arrange
        input_text = "<script>alert('xss')</script>Hello World"
        
        # Act
        result = sanitize_input(input_text)
        
        # Assert
        assert "<script>" not in result
        assert "alert('xss')" not in result
        assert "Hello World" in result

    def test_sanitize_input_removes_sql_injection(self):
        """Test de suppression des tentatives d'injection SQL"""
        # Arrange
        input_text = "'; DROP TABLE users; --"
        
        # Act
        result = sanitize_input(input_text)
        
        # Assert
        assert "DROP TABLE" not in result
        assert ";" not in result

    def test_sanitize_input_preserves_safe_text(self):
        """Test de préservation du texte sûr"""
        # Arrange
        safe_text = "Hello World! This is safe text with numbers 123 and symbols @#$%"
        
        # Act
        result = sanitize_input(safe_text)
        
        # Assert
        assert "Hello World" in result
        assert "123" in result

    def test_sanitize_input_handles_none(self):
        """Test de gestion des valeurs None"""
        # Arrange
        input_text = None
        
        # Act
        result = sanitize_input(input_text)
        
        # Assert
        assert result == ""

    def test_sanitize_input_handles_empty_string(self):
        """Test de gestion des chaînes vides"""
        # Arrange
        input_text = ""
        
        # Act
        result = sanitize_input(input_text)
        
        # Assert
        assert result == ""


class TestFileUploadValidation:
    """Tests pour la validation des uploads de fichiers"""

    def test_validate_file_upload_valid_file(self):
        """Test de validation d'un fichier valide"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = "document.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024 * 1024  # 1MB
        
        # Act
        result = validate_file_upload(mock_file)
        
        # Assert
        assert result["is_valid"] is True
        assert result["errors"] == []

    def test_validate_file_upload_invalid_type(self):
        """Test de validation avec type de fichier invalide"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = "script.exe"
        mock_file.content_type = "application/x-msdownload"
        mock_file.size = 1024 * 1024
        
        # Act
        result = validate_file_upload(mock_file)
        
        # Assert
        assert result["is_valid"] is False
        assert "file type" in str(result["errors"]).lower()

    def test_validate_file_upload_too_large(self):
        """Test de validation avec fichier trop volumineux"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = "large_file.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.size = 100 * 1024 * 1024  # 100MB
        
        # Act
        result = validate_file_upload(mock_file)
        
        # Assert
        assert result["is_valid"] is False
        assert "size" in str(result["errors"]).lower()

    def test_validate_file_upload_no_filename(self):
        """Test de validation sans nom de fichier"""
        # Arrange
        mock_file = Mock()
        mock_file.filename = ""
        mock_file.content_type = "application/pdf"
        mock_file.size = 1024
        
        # Act
        result = validate_file_upload(mock_file)
        
        # Assert
        assert result["is_valid"] is False
        assert "filename" in str(result["errors"]).lower()


class TestPermissionChecking:
    """Tests pour la vérification des permissions"""

    def test_check_permissions_admin_access(self):
        """Test d'accès administrateur"""
        # Arrange
        user = Mock()
        user.role = UserRole.ADMIN
        required_permission = "user:delete"
        
        # Act
        result = check_permissions(user, required_permission)
        
        # Assert
        assert result is True

    def test_check_permissions_customer_access(self):
        """Test d'accès client"""
        # Arrange
        user = Mock()
        user.role = UserRole.CUSTOMER
        required_permission = "order:create"
        
        # Act
        result = check_permissions(user, required_permission)
        
        # Assert
        assert result is True

    def test_check_permissions_insufficient_permissions(self):
        """Test avec permissions insuffisantes"""
        # Arrange
        user = Mock()
        user.role = UserRole.CUSTOMER
        required_permission = "user:delete"
        
        # Act
        result = check_permissions(user, required_permission)
        
        # Assert
        assert result is False

    def test_check_permissions_none_user(self):
        """Test avec utilisateur None"""
        # Arrange
        user = None
        required_permission = "order:create"
        
        # Act
        result = check_permissions(user, required_permission)
        
        # Assert
        assert result is False


class TestRateLimitChecking:
    """Tests pour la vérification des limites de taux"""

    def test_rate_limit_check_allows_request(self):
        """Test d'autorisation de requête normale"""
        # Arrange
        user_id = "user123"
        endpoint = "/api/v1/orders"
        
        # Act
        with patch('app.core.security.redis_client') as mock_redis:
            mock_redis.get.return_value = "5"  # 5 requêtes dans la fenêtre
            mock_redis.incr.return_value = 6   # 6ème requête
            
            result = rate_limit_check(user_id, endpoint)
        
        # Assert
        assert result["allowed"] is True
        assert result["remaining"] > 0

    def test_rate_limit_check_blocks_request(self):
        """Test de blocage de requête en cas de dépassement"""
        # Arrange
        user_id = "user123"
        endpoint = "/api/v1/orders"
        
        # Act
        with patch('app.core.security.redis_client') as mock_redis:
            mock_redis.get.return_value = "100"  # Limite dépassée
            mock_redis.incr.return_value = 101
            
            result = rate_limit_check(user_id, endpoint)
        
        # Assert
        assert result["allowed"] is False
        assert result["remaining"] == 0

    def test_rate_limit_check_different_users(self):
        """Test que les limites sont séparées par utilisateur"""
        # Arrange
        user1 = "user123"
        user2 = "user456"
        endpoint = "/api/v1/orders"
        
        # Act
        with patch('app.core.security.redis_client') as mock_redis:
            mock_redis.get.return_value = "5"
            mock_redis.incr.return_value = 6
            
            result1 = rate_limit_check(user1, endpoint)
            result2 = rate_limit_check(user2, endpoint)
        
        # Assert
        assert result1["allowed"] is True
        assert result2["allowed"] is True


class TestAPIKeyValidation:
    """Tests pour la validation des clés API"""

    def test_validate_api_key_valid_key(self):
        """Test de validation d'une clé API valide"""
        # Arrange
        api_key = "valid_api_key_12345"
        
        # Act
        with patch('app.core.security.get_api_key_info') as mock_get_info:
            mock_get_info.return_value = {
                "user_id": "user123",
                "permissions": ["read", "write"],
                "is_active": True
            }
            
            result = validate_api_key(api_key)
        
        # Assert
        assert result["is_valid"] is True
        assert result["user_id"] == "user123"

    def test_validate_api_key_invalid_key(self):
        """Test de validation d'une clé API invalide"""
        # Arrange
        api_key = "invalid_key"
        
        # Act
        with patch('app.core.security.get_api_key_info') as mock_get_info:
            mock_get_info.return_value = None
            
            result = validate_api_key(api_key)
        
        # Assert
        assert result["is_valid"] is False

    def test_validate_api_key_inactive_key(self):
        """Test de validation d'une clé API inactive"""
        # Arrange
        api_key = "inactive_api_key"
        
        # Act
        with patch('app.core.security.get_api_key_info') as mock_get_info:
            mock_get_info.return_value = {
                "user_id": "user123",
                "permissions": ["read"],
                "is_active": False
            }
            
            result = validate_api_key(api_key)
        
        # Assert
        assert result["is_valid"] is False


class TestDataEncryption:
    """Tests pour le chiffrement des données sensibles"""

    def test_encrypt_sensitive_data_encrypts_data(self):
        """Test que encrypt_sensitive_data chiffre les données"""
        # Arrange
        sensitive_data = "credit_card_number_1234"
        encryption_key = "test_encryption_key"
        
        # Act
        encrypted = encrypt_sensitive_data(sensitive_data, encryption_key)
        
        # Assert
        assert encrypted != sensitive_data
        assert isinstance(encrypted, str)
        assert len(encrypted) > 0

    def test_decrypt_sensitive_data_decrypts_data(self):
        """Test que decrypt_sensitive_data déchiffre les données"""
        # Arrange
        sensitive_data = "credit_card_number_1234"
        encryption_key = "test_encryption_key"
        encrypted = encrypt_sensitive_data(sensitive_data, encryption_key)
        
        # Act
        decrypted = decrypt_sensitive_data(encrypted, encryption_key)
        
        # Assert
        assert decrypted == sensitive_data

    def test_encrypt_decrypt_cycle(self):
        """Test du cycle complet de chiffrement/déchiffrement"""
        # Arrange
        test_data = [
            "credit_card_1234",
            "ssn_567890",
            "password_hash_abc123",
            "api_key_xyz789"
        ]
        encryption_key = "test_encryption_key"
        
        # Act & Assert
        for data in test_data:
            encrypted = encrypt_sensitive_data(data, encryption_key)
            decrypted = decrypt_sensitive_data(encrypted, encryption_key)
            assert decrypted == data

    def test_encrypt_sensitive_data_different_keys(self):
        """Test que des clés différentes produisent des résultats différents"""
        # Arrange
        sensitive_data = "test_data"
        key1 = "key1"
        key2 = "key2"
        
        # Act
        encrypted1 = encrypt_sensitive_data(sensitive_data, key1)
        encrypted2 = encrypt_sensitive_data(sensitive_data, key2)
        
        # Assert
        assert encrypted1 != encrypted2


class TestCSRFTokenValidation:
    """Tests pour la validation des tokens CSRF"""

    def test_generate_csrf_token_creates_token(self):
        """Test que generate_csrf_token crée un token"""
        # Act
        token = generate_csrf_token()
        
        # Assert
        assert isinstance(token, str)
        assert len(token) >= 32

    def test_validate_csrf_token_valid_token(self):
        """Test de validation d'un token CSRF valide"""
        # Arrange
        token = generate_csrf_token()
        
        # Act
        result = validate_csrf_token(token)
        
        # Assert
        assert result is True

    def test_validate_csrf_token_invalid_token(self):
        """Test de validation d'un token CSRF invalide"""
        # Arrange
        invalid_token = "invalid_csrf_token"
        
        # Act
        result = validate_csrf_token(invalid_token)
        
        # Assert
        assert result is False

    def test_validate_csrf_token_expired_token(self):
        """Test de validation d'un token CSRF expiré"""
        # Arrange
        # Simuler un token expiré
        with patch('app.core.security.get_csrf_token_info') as mock_get_info:
            mock_get_info.return_value = {
                "expires_at": datetime.now() - timedelta(hours=1)
            }
            
            result = validate_csrf_token("expired_token")
        
        # Assert
        assert result is False


class TestFileValidation:
    """Tests pour la validation des fichiers"""

    def test_validate_file_type_valid_types(self):
        """Test de validation de types de fichiers valides"""
        # Arrange
        valid_files = [
            ("document.pdf", "application/pdf"),
            ("image.jpg", "image/jpeg"),
            ("data.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        ]
        
        # Act & Assert
        for filename, content_type in valid_files:
            result = validate_file_type(filename, content_type)
            assert result["is_valid"] is True

    def test_validate_file_type_invalid_types(self):
        """Test de validation de types de fichiers invalides"""
        # Arrange
        invalid_files = [
            ("script.exe", "application/x-msdownload"),
            ("malware.bat", "application/x-bat"),
            ("virus.com", "application/x-msdos-program")
        ]
        
        # Act & Assert
        for filename, content_type in invalid_files:
            result = validate_file_type(filename, content_type)
            assert result["is_valid"] is False

    def test_validate_file_size_valid_size(self):
        """Test de validation de taille de fichier valide"""
        # Arrange
        file_size = 1024 * 1024  # 1MB
        max_size = 10 * 1024 * 1024  # 10MB
        
        # Act
        result = validate_file_size(file_size, max_size)
        
        # Assert
        assert result["is_valid"] is True

    def test_validate_file_size_too_large(self):
        """Test de validation de taille de fichier trop grande"""
        # Arrange
        file_size = 20 * 1024 * 1024  # 20MB
        max_size = 10 * 1024 * 1024  # 10MB
        
        # Act
        result = validate_file_size(file_size, max_size)
        
        # Assert
        assert result["is_valid"] is False


class TestDataValidation:
    """Tests pour la validation des données"""

    def test_validate_url_valid_urls(self):
        """Test de validation d'URLs valides"""
        # Arrange
        valid_urls = [
            "https://www.example.com",
            "http://localhost:8000",
            "https://api.example.com/v1/users",
            "ftp://files.example.com"
        ]
        
        # Act & Assert
        for url in valid_urls:
            assert validate_url(url) is True

    def test_validate_url_invalid_urls(self):
        """Test de validation d'URLs invalides"""
        # Arrange
        invalid_urls = [
            "not_a_url",
            "http://",
            "https://",
            "ftp://",
            ""
        ]
        
        # Act & Assert
        for url in invalid_urls:
            assert validate_url(url) is False

    def test_validate_ip_address_valid_ips(self):
        """Test de validation d'adresses IP valides"""
        # Arrange
        valid_ips = [
            "192.168.1.1",
            "10.0.0.1",
            "172.16.0.1",
            "127.0.0.1",
            "8.8.8.8"
        ]
        
        # Act & Assert
        for ip in valid_ips:
            assert validate_ip_address(ip) is True

    def test_validate_ip_address_invalid_ips(self):
        """Test de validation d'adresses IP invalides"""
        # Arrange
        invalid_ips = [
            "256.1.2.3",
            "1.2.3.256",
            "192.168.1",
            "192.168.1.1.1",
            "not_an_ip"
        ]
        
        # Act & Assert
        for ip in invalid_ips:
            assert validate_ip_address(ip) is False

    def test_validate_phone_number_valid_numbers(self):
        """Test de validation de numéros de téléphone valides"""
        # Arrange
        valid_phones = [
            "+33123456789",
            "0123456789",
            "+44 20 7946 0958",
            "1-555-123-4567"
        ]
        
        # Act & Assert
        for phone in valid_phones:
            assert validate_phone_number(phone) is True

    def test_validate_phone_number_invalid_numbers(self):
        """Test de validation de numéros de téléphone invalides"""
        # Arrange
        invalid_phones = [
            "not_a_phone",
            "123",
            "abc123",
            ""
        ]
        
        # Act & Assert
        for phone in invalid_phones:
            assert validate_phone_number(phone) is False

    def test_validate_postal_code_valid_codes(self):
        """Test de validation de codes postaux valides"""
        # Arrange
        valid_codes = [
            "12345",      # Format US
            "12345-6789", # Format US étendu
            "A1B 2C3",    # Format canadien
            "12345 67"    # Format européen
        ]
        
        # Act & Assert
        for code in valid_codes:
            assert validate_postal_code(code) is True

    def test_validate_postal_code_invalid_codes(self):
        """Test de validation de codes postaux invalides"""
        # Arrange
        invalid_codes = [
            "123",        # Trop court
            "12345678901", # Trop long
            "ABCDE",      # Pas de chiffres
            ""            # Vide
        ]
        
        # Act & Assert
        for code in invalid_codes:
            assert validate_postal_code(code) is False

    def test_validate_credit_card_valid_cards(self):
        """Test de validation de cartes de crédit valides"""
        # Arrange
        valid_cards = [
            "4532015112830366",  # Visa
            "5425233430109903",  # Mastercard
            "378282246310005"    # American Express
        ]
        
        # Act & Assert
        for card in valid_cards:
            assert validate_credit_card(card) is True

    def test_validate_credit_card_invalid_cards(self):
        """Test de validation de cartes de crédit invalides"""
        # Arrange
        invalid_cards = [
            "1234567890123456",  # Numéro invalide
            "1234",              # Trop court
            "not_a_card",        # Pas de chiffres
            ""                   # Vide
        ]
        
        # Act & Assert
        for card in invalid_cards:
            assert validate_credit_card(card) is False

    def test_validate_iban_valid_ibans(self):
        """Test de validation d'IBANs valides"""
        # Arrange
        valid_ibans = [
            "FR1420041010050500013M02606",  # France
            "DE89370400440532013000",       # Allemagne
            "GB29NWBK60161331926819"        # Royaume-Uni
        ]
        
        # Act & Assert
        for iban in valid_ibans:
            assert validate_iban(iban) is True

    def test_validate_iban_invalid_ibans(self):
        """Test de validation d'IBANs invalides"""
        # Arrange
        invalid_ibans = [
            "FR1420041010050500013M0260",   # Trop court
            "FR1420041010050500013M026060", # Trop long
            "not_an_iban",                  # Pas un IBAN
            ""                              # Vide
        ]
        
        # Act & Assert
        for iban in invalid_ibans:
            assert validate_iban(iban) is False


class TestSecurityLevels:
    """Tests pour les niveaux de sécurité"""

    def test_security_levels_are_ordered(self):
        """Test que les niveaux de sécurité sont ordonnés"""
        # Assert
        assert SecurityLevel.LOW < SecurityLevel.MEDIUM
        assert SecurityLevel.MEDIUM < SecurityLevel.HIGH
        assert SecurityLevel.HIGH < SecurityLevel.CRITICAL

    def test_security_levels_have_descriptions(self):
        """Test que les niveaux de sécurité ont des descriptions"""
        # Act & Assert
        for level in SecurityLevel:
            assert hasattr(level, 'description')
            assert isinstance(level.description, str)
            assert len(level.description) > 0

    def test_security_levels_have_thresholds(self):
        """Test que les niveaux de sécurité ont des seuils"""
        # Act & Assert
        for level in SecurityLevel:
            assert hasattr(level, 'threshold')
            assert isinstance(level.threshold, int)
            assert level.threshold >= 0
