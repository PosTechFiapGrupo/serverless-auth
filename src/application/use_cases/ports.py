from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities import Customer


class ICustomerRepository(ABC):
    """Interface for customer data access."""
    
    @abstractmethod
    def find_by_cpf(self, cpf: str) -> Optional[Customer]:
        """Find customer by CPF."""
        pass


class ITokenGenerator(ABC):
    """Interface for JWT token generation."""
    
    @abstractmethod
    def generate(self, customer_id: int, cpf: str, expiration_minutes: int = 60) -> str:
        """Generate JWT token."""
        pass
    
    @abstractmethod
    def validate(self, token: str) -> dict:
        """Validate and decode JWT token."""
        pass
