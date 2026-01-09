from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects import CPF
from src.application.use_cases.ports import ICustomerRepository, ITokenGenerator


@dataclass
class AuthenticationRequest:
    """Input data for authentication."""

    cpf: str


@dataclass
class AuthenticationResponse:
    """Output data for authentication."""

    success: bool
    token: Optional[str] = None
    message: Optional[str] = None
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None


class AuthenticateCustomerUseCase:
    """
    Use Case: Authenticate Customer

    Responsibilities:
    1. Validate CPF format
    2. Find customer in database
    3. Check customer status
    4. Generate JWT token

    This class contains the application business logic,
    independent of frameworks and external systems.
    """

    def __init__(
        self, customer_repository: ICustomerRepository, token_generator: ITokenGenerator
    ):
        self._customer_repository = customer_repository
        self._token_generator = token_generator

    def execute(self, request: AuthenticationRequest) -> AuthenticationResponse:
        """
        Execute authentication use case.

        Args:
            request: Authentication request with CPF

        Returns:
            AuthenticationResponse with token or error message
        """
        try:
            cpf = CPF(request.cpf)
        except ValueError:
            return AuthenticationResponse(success=False, message="CPF inválido")

        customer = self._customer_repository.find_by_cpf(cpf.clean())

        if not customer:
            return AuthenticationResponse(
                success=False, message="Cliente não encontrado"
            )

        token = self._token_generator.generate(
            customer_id=customer.id, cpf=customer.cpf
        )

        return AuthenticationResponse(
            success=True,
            token=token,
            message="Autenticação realizada com sucesso",
            customer_id=customer.id,
            customer_name=customer.nome,
        )
