"""Unit tests for CustomerRepository."""

import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.adapters.gateways.customer_repository import CustomerRepository
from src.infrastructure.database.models import CustomerModel
from src.domain.entities import Customer


class TestCustomerRepository:
    """Test suite for CustomerRepository."""

    def test_find_by_cpf_found(self):
        """Test finding a customer by CPF when customer exists."""
        # Arrange
        mock_session = Mock()

        customer_model = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        mock_query = Mock()
        mock_query.all.return_value = [customer_model]
        mock_session.query.return_value = mock_query

        repository = CustomerRepository(mock_session)

        # Act
        customer = repository.find_by_cpf("11144477735")

        # Assert
        assert customer is not None
        assert isinstance(customer, Customer)
        assert customer.id == "550e8400-e29b-41d4-a716-446655440000"
        assert customer.cpf == "11144477735"
        assert customer.nome == "João da Silva"
        assert customer.email == "joao@example.com"
        assert customer.telefone == "11987654321"

        mock_session.query.assert_called_once_with(CustomerModel)

    def test_find_by_cpf_not_found(self):
        """Test finding a customer by CPF when customer doesn't exist."""
        # Arrange
        mock_session = Mock()

        mock_query = Mock()
        mock_query.all.return_value = []
        mock_session.query.return_value = mock_query

        repository = CustomerRepository(mock_session)

        # Act
        customer = repository.find_by_cpf("11144477735")

        # Assert
        assert customer is None
        mock_session.query.assert_called_once_with(CustomerModel)

    def test_find_by_cpf_handles_formatted_cpf(self):
        """Test that repository can handle CPF with formatting."""
        # Arrange
        mock_session = Mock()

        customer_model = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        mock_query = Mock()
        mock_query.all.return_value = [customer_model]
        mock_session.query.return_value = mock_query

        repository = CustomerRepository(mock_session)

        # Act
        customer = repository.find_by_cpf("111.444.777-35")

        # Assert
        assert customer is not None
        assert customer.cpf == "11144477735"

    def test_to_entity_conversion(self):
        """Test conversion from database model to domain entity."""
        # Arrange
        mock_session = Mock()
        repository = CustomerRepository(mock_session)

        customer_model = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        # Act
        customer = repository._to_entity(customer_model)

        # Assert
        assert isinstance(customer, Customer)
        assert customer.id == "550e8400-e29b-41d4-a716-446655440000"
        assert customer.cpf == "11144477735"
        assert customer.nome == "João da Silva"
        assert customer.email == "joao@example.com"
        assert customer.telefone == "11987654321"
