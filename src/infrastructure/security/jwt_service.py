from datetime import datetime, timedelta
from typing import Dict
import uuid

import jwt

from src.application.use_cases.ports import ITokenGenerator
from src.infrastructure.config.settings import get_settings


class JWTTokenGenerator(ITokenGenerator):
    """
    JWT Token Generator implementation.

    Uses PyJWT library to generate and validate JWT tokens.
    """

    def __init__(self):
        self._settings = get_settings()

    def generate(self, customer_id: int, cpf: str, expiration_minutes: int = 60) -> str:
        """
        Generate JWT token.

        Args:
            customer_id: Customer ID
            cpf: Customer CPF
            expiration_minutes: Token expiration time in minutes

        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        expiration = now + timedelta(minutes=expiration_minutes)
        trace_id = str(uuid.uuid4())

        payload = {
            "sub": str(customer_id),
            "cpf": cpf,
            "role": "client",
            "aud": "api-client",
            "trace_id": trace_id,
            "iat": now,
            "exp": expiration,
            "iss": self._settings.jwt_issuer,
        }

        token = jwt.encode(
            payload, self._settings.jwt_secret, algorithm=self._settings.jwt_algorithm
        )

        return token

    def validate(self, token: str) -> Dict:
        """
        Validate and decode JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded payload

        Raises:
            jwt.InvalidTokenError: If token is invalid or expired
        """
        try:
            payload = jwt.decode(
            token,
            self._settings.jwt_secret,
            algorithms=[self._settings.jwt_algorithm],
            issuer=self._settings.jwt_issuer,
            audience="api-client",
        )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Token inválido: {str(e)}")
