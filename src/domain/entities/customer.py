from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Customer:
    """
    Customer entity representing a client in the system.

    This is an immutable entity following Clean Architecture principles.
    All business rules related to a customer should be here.

    Note: Production database doesn't have status field, so all customers
    with valid CPF in the database are considered active.
    """

    id: str
    cpf: str
    nome: str
    email: Optional[str]
    telefone: Optional[str]
    criado_em: datetime
    atualizado_em: datetime

    def is_active(self) -> bool:
        """
        Check if customer is active.

        Since production database doesn't have status field,
        all customers in the database are considered active.
        """
        return True

    def can_authenticate(self) -> bool:
        """Business rule: only active customers can authenticate."""
        return self.is_active()

    def __post_init__(self):
        """Validate customer data."""
        if not self.cpf:
            raise ValueError("CPF cannot be empty")
        if not self.nome:
            raise ValueError("Nome cannot be empty")
