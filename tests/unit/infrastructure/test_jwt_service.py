"""Unit tests for JWT Token Generator."""

import pytest
import jwt
from datetime import datetime, timedelta
from unittest.mock import patch, Mock

from src.infrastructure.security.jwt_service import JWTTokenGenerator


class TestJWTTokenGenerator:
    """Test suite for JWT token generator."""

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_generate_token(self, mock_get_settings):
        """Test generating a JWT token."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        token_generator = JWTTokenGenerator()

        # Act
        token = token_generator.generate(
            customer_id=1, cpf="12345678901", expiration_minutes=60
        )

        # Assert
        assert token is not None
        assert isinstance(token, str)

        # Decode to verify
        payload = jwt.decode(
            token, "test-secret", algorithms=["HS256"], issuer="test-issuer", audience="api-client"
        )

        assert payload["sub"] == "1"
        assert payload["cpf"] == "12345678901"
        assert payload["iss"] == "test-issuer"
        assert "iat" in payload
        assert "exp" in payload

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_validate_valid_token(self, mock_get_settings):
        """Test validating a valid JWT token."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        token_generator = JWTTokenGenerator()

        # Generate a token
        token = token_generator.generate(
            customer_id=1, cpf="12345678901", expiration_minutes=60
        )

        # Act
        payload = token_generator.validate(token)

        # Assert
        assert payload["sub"] == "1"
        assert payload["cpf"] == "12345678901"

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_validate_expired_token(self, mock_get_settings):
        """Test validating an expired JWT token."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        # Create an expired token manually
        now = datetime.utcnow()
        expired_time = now - timedelta(hours=2)

        payload = {
            "sub": "1",
            "cpf": "12345678901",
            "iat": expired_time,
            "exp": expired_time + timedelta(minutes=60),
            "iss": "test-issuer",
        }

        token = jwt.encode(payload, "test-secret", algorithm="HS256")

        token_generator = JWTTokenGenerator()

        # Act & Assert
        with pytest.raises(ValueError, match="Token expirado"):
            token_generator.validate(token)

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_validate_invalid_token(self, mock_get_settings):
        """Test validating an invalid JWT token."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        token_generator = JWTTokenGenerator()

        # Act & Assert
        with pytest.raises(ValueError, match="Token inválido"):
            token_generator.validate("invalid-token")

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_validate_token_wrong_secret(self, mock_get_settings):
        """Test validating a token with wrong secret."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        # Create token with different secret
        payload = {
            "sub": "1",
            "cpf": "12345678901",
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iss": "test-issuer",
        }

        token = jwt.encode(payload, "wrong-secret", algorithm="HS256")

        token_generator = JWTTokenGenerator()

        # Act & Assert
        with pytest.raises(ValueError, match="Token inválido"):
            token_generator.validate(token)

    @patch("src.infrastructure.security.jwt_service.get_settings")
    def test_generate_token_custom_expiration(self, mock_get_settings):
        """Test generating token with custom expiration."""
        # Arrange
        mock_settings = Mock()
        mock_settings.jwt_secret = "test-secret"
        mock_settings.jwt_algorithm = "HS256"
        mock_settings.jwt_issuer = "test-issuer"
        mock_get_settings.return_value = mock_settings

        token_generator = JWTTokenGenerator()

        # Act
        token = token_generator.generate(
            customer_id=1,
            cpf="12345678901",
            expiration_minutes=120,  # Custom expiration
        )

        # Assert
        payload = jwt.decode(
            token, "test-secret", algorithms=["HS256"], issuer="test-issuer", audience="api-client"
        )

        iat = datetime.fromtimestamp(payload["iat"])
        exp = datetime.fromtimestamp(payload["exp"])

        # Should be approximately 120 minutes
        delta = exp - iat
        assert 119 <= delta.total_seconds() / 60 <= 121
