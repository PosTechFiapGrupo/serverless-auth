import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Settings:
    """
    Application settings.
    
    Loads configuration from environment variables.
    Uses dataclass for immutability and type safety.
    """
    
    database_url: str
    jwt_secret: str
    
    database_echo: bool = False
    jwt_algorithm: str = "HS256"
    jwt_issuer: str = "serverless-auth"
    jwt_expiration_minutes: int = 60
    
    environment: str = "production"
    
    @classmethod
    def from_env(cls) -> "Settings":
        """Create settings from environment variables."""

        db_host = os.getenv("DB_HOST")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        
        if not all([db_host, db_name, db_user, db_password]):
            raise ValueError(
                "Missing required database environment variables: "
                "DB_HOST, DB_NAME, DB_USER, DB_PASSWORD"
            )
        
        database_url = (
            f"mysql+pymysql://{db_user}:{db_password}"
            f"@{db_host}:{db_port}/{db_name}"
        )
        
        jwt_secret = os.getenv("JWT_SECRET")
        if not jwt_secret:
            raise ValueError("Missing required environment variable: JWT_SECRET")
        
        return cls(
            database_url=database_url,
            database_echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
            jwt_secret=jwt_secret,
            jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
            jwt_issuer=os.getenv("JWT_ISSUER", "serverless-auth"),
            jwt_expiration_minutes=int(os.getenv("JWT_EXPIRATION_MINUTES", "60")),
            environment=os.getenv("ENVIRONMENT", "production")
        )


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings.from_env()
