import pytest
from datetime import datetime
from unittest.mock import Mock

from src.domain.entities import Customer
from src.domain.value_objects import CPF


@pytest.fixture
def valid_cpf():
    """Valid CPF for testing."""
    return "11144477735"


@pytest.fixture
def invalid_cpf():
    """Invalid CPF for testing."""
    return "00000000000"


@pytest.fixture
def sample_customer():
    """Sample customer entity."""
    return Customer(
        id="550e8400-e29b-41d4-a716-446655440000",
        cpf="11144477735",
        nome="João da Silva",
        email="joao@example.com",
        telefone="11987654321",
        criado_em=datetime(2024, 1, 1, 10, 0, 0),
        atualizado_em=datetime(2024, 1, 1, 10, 0, 0)
    )


@pytest.fixture
def inactive_customer():
    """Inactive customer entity (for backwards compatibility with tests)."""
    return Customer(
        id="550e8400-e29b-41d4-a716-446655440001",
        cpf="39053344705",
        nome="Maria Santos",
        email="maria@example.com",
        telefone="11912345678",
        criado_em=datetime(2024, 1, 1, 10, 0, 0),
        atualizado_em=datetime(2024, 1, 1, 10, 0, 0)
    )


@pytest.fixture
def mock_customer_repository():
    """Mock customer repository."""
    from src.application.use_cases.ports import ICustomerRepository
    return Mock(spec=ICustomerRepository)


@pytest.fixture
def mock_token_generator():
    """Mock token generator."""
    from src.application.use_cases.ports import ITokenGenerator
    return Mock(spec=ITokenGenerator)
