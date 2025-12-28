"""Unit tests for Customer Entity."""

import pytest
from datetime import datetime
from src.domain.entities import Customer


class TestCustomer:
    """Test suite for Customer entity."""

    def test_create_customer(self):
        """Test creating a customer."""
        customer = Customer(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="11144477735",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        assert customer.id == "550e8400-e29b-41d4-a716-446655440000"
        assert customer.cpf == "11144477735"
        assert customer.nome == "João da Silva"
        assert customer.email == "joao@example.com"
        assert customer.telefone == "11987654321"

    def test_customer_is_active(self):
        """Test is_active method - all customers in database are active."""
        customer = Customer(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="11144477735",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        assert customer.is_active() is True

    def test_customer_can_authenticate(self):
        """Test can_authenticate returns True for all customers in database."""
        customer = Customer(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="11144477735",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        assert customer.can_authenticate() is True

    def test_customer_is_immutable(self):
        """Test that customer is immutable."""
        customer = Customer(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="11144477735",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
        )

        with pytest.raises(AttributeError):
            customer.nome = "Maria Santos"

    def test_customer_without_cpf_raises_error(self):
        """Test that customer without CPF raises ValueError."""
        with pytest.raises(ValueError, match="CPF cannot be empty"):
            Customer(
                id="550e8400-e29b-41d4-a716-446655440000",
                cpf="",
                nome="João da Silva",
                email="joao@example.com",
                telefone="11987654321",
                criado_em=datetime(2024, 1, 1, 10, 0, 0),
                atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
            )

    def test_customer_without_nome_raises_error(self):
        """Test that customer without nome raises ValueError."""
        with pytest.raises(ValueError, match="Nome cannot be empty"):
            Customer(
                id="550e8400-e29b-41d4-a716-446655440000",
                cpf="11144477735",
                nome="",
                email="joao@example.com",
                telefone="11987654321",
                criado_em=datetime(2024, 1, 1, 10, 0, 0),
                atualizado_em=datetime(2024, 1, 1, 10, 0, 0),
            )

    def test_customer_with_optional_fields_none(self):
        """Test customer with optional email and telefone as None."""
        customer = Customer(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="11144477735",
            nome="João da Silva",
            email=None,
            telefone=None,
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 2, 1, 15, 30, 0),
        )

        assert customer.email is None
        assert customer.telefone is None
        assert customer.atualizado_em == datetime(2024, 2, 1, 15, 30, 0)
