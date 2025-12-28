"""Unit tests for Settings configuration."""

import pytest
import os
from unittest.mock import patch

from src.infrastructure.config.settings import Settings, get_settings


class TestSettings:
    """Test suite for Settings configuration."""

    def test_settings_from_env_with_all_vars(self):
        """Test settings when all environment variables are set."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_PORT": "3306",
                "DB_USER": "root",
                "DB_PASSWORD": "password",
                "DB_NAME": "test_db",
                "JWT_SECRET": "test-secret-key",
                "JWT_ALGORITHM": "HS512",
                "JWT_EXPIRATION_MINUTES": "60",
            },
            clear=True,
        ):
            settings = Settings.from_env()

            assert "localhost" in settings.database_url
            assert "test_db" in settings.database_url
            assert settings.jwt_secret == "test-secret-key"
            assert settings.jwt_algorithm == "HS512"
            assert settings.jwt_expiration_minutes == 60

    def test_settings_from_env_defaults(self):
        """Test that settings use default values when optional vars not set."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            settings = Settings.from_env()

            assert settings.jwt_algorithm == "HS256"
            assert settings.jwt_expiration_minutes == 60
            assert settings.environment == "production"

    def test_database_url_construction(self):
        """Test database_url property construction."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "db.example.com",
                "DB_PORT": "3307",
                "DB_USER": "myuser",
                "DB_PASSWORD": "mypass",
                "DB_NAME": "mydb",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            settings = Settings.from_env()
            expected = "mysql+pymysql://myuser:mypass@db.example.com:3307/mydb"

            assert settings.database_url == expected

    def test_database_url_with_special_chars(self):
        """Test database_url handles special characters in password."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_PORT": "3306",
                "DB_USER": "user",
                "DB_PASSWORD": "p@ssw0rd!",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            settings = Settings.from_env()

            assert "p@ssw0rd!" in settings.database_url

    def test_get_settings_singleton(self):
        """Test that get_settings returns the same instance."""
        # Clear cache first
        get_settings.cache_clear()

        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            settings1 = get_settings()
            settings2 = get_settings()

            assert settings1 is settings2

    def test_missing_db_host_raises_error(self):
        """Test that missing DB_HOST raises ValueError."""
        with patch.dict(
            os.environ,
            {
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            with pytest.raises(ValueError, match="Missing required database"):
                Settings.from_env()

    def test_missing_jwt_secret_raises_error(self):
        """Test that missing JWT_SECRET raises ValueError."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
            },
            clear=True,
        ):
            with pytest.raises(
                ValueError, match="Missing required environment variable: JWT_SECRET"
            ):
                Settings.from_env()

    def test_custom_port(self):
        """Test settings with custom database port."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_PORT": "3308",
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
            },
            clear=True,
        ):
            settings = Settings.from_env()

            assert ":3308/" in settings.database_url

    def test_custom_expiration(self):
        """Test JWT expiration minutes customization."""
        with patch.dict(
            os.environ,
            {
                "DB_HOST": "localhost",
                "DB_USER": "root",
                "DB_PASSWORD": "pass",
                "DB_NAME": "db",
                "JWT_SECRET": "secret",
                "JWT_EXPIRATION_MINUTES": "45",
            },
            clear=True,
        ):
            settings = Settings.from_env()

            assert settings.jwt_expiration_minutes == 45
