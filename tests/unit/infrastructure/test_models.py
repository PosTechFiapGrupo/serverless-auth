"""Unit tests for database models."""
import pytest
from datetime import datetime

from src.infrastructure.database.models import CustomerModel


class TestCustomerModel:
    """Test suite for CustomerModel."""
    
    def test_create_customer_model(self):
        """Test creating a customer model."""
        customer = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0)
        )
        
        assert customer.id == "550e8400-e29b-41d4-a716-446655440000"
        assert customer.cpf == "111.444.777-35"
        assert customer.nome == "João da Silva"
        assert customer.email == "joao@example.com"
        assert customer.telefone == "11987654321"
    
    def test_customer_model_table_name(self):
        """Test that table name is correct."""
        assert CustomerModel.__tablename__ == "clientes"
    
    def test_customer_model_repr(self):
        """Test customer model string representation."""
        customer = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva",
            email="joao@example.com",
            telefone="11987654321",
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0)
        )
        
        repr_str = repr(customer)
        assert "550e8400-e29b-41d4-a716-446655440000" in repr_str
        assert "111.444.777-35" in repr_str
        assert "João da Silva" in repr_str
    
    def test_customer_model_with_optional_fields_none(self):
        """Test customer model with optional fields as None."""
        customer = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf=None,
            nome="João da Silva",
            email=None,
            telefone=None,
            criado_em=datetime(2024, 1, 1, 10, 0, 0),
            atualizado_em=datetime(2024, 1, 1, 10, 0, 0)
        )
        
        assert customer.cpf is None
        assert customer.email is None
        assert customer.telefone is None
    
    def test_customer_model_default_timestamps(self):
        """Test that timestamps have defaults."""
        customer = CustomerModel(
            id="550e8400-e29b-41d4-a716-446655440000",
            cpf="111.444.777-35",
            nome="João da Silva"
        )
        
        # Timestamps should have default values (will be set by SQLAlchemy)
        assert customer.criado_em is None  # Not set until persisted
        assert customer.atualizado_em is None  # Not set until persisted
