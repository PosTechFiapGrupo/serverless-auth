"""Unit tests for AuthenticateCustomerUseCase."""

import pytest
from unittest.mock import Mock

from src.application.use_cases.authenticate_customer import (
    AuthenticateCustomerUseCase,
    AuthenticationRequest,
    AuthenticationResponse,
)


class TestAuthenticateCustomerUseCase:
    """Test suite for authenticate customer use case."""

    def test_successful_authentication(
        self, mock_customer_repository, mock_token_generator, sample_customer
    ):
        """Test successful authentication flow."""
        # Arrange
        mock_customer_repository.find_by_cpf.return_value = sample_customer
        mock_token_generator.generate.return_value = "fake-jwt-token"

        use_case = AuthenticateCustomerUseCase(
            customer_repository=mock_customer_repository,
            token_generator=mock_token_generator,
        )

        request = AuthenticationRequest(cpf="11144477735")

        # Act
        response = use_case.execute(request)

        # Assert
        assert response.success is True
        assert response.token == "fake-jwt-token"
        assert response.customer_id == "550e8400-e29b-41d4-a716-446655440000"
        assert response.customer_name == "João da Silva"
        assert "sucesso" in response.message.lower()

        mock_customer_repository.find_by_cpf.assert_called_once_with("11144477735")
        mock_token_generator.generate.assert_called_once_with(
            customer_id="550e8400-e29b-41d4-a716-446655440000", cpf="11144477735"
        )

    def test_authentication_with_invalid_cpf(
        self, mock_customer_repository, mock_token_generator
    ):
        """Test authentication with invalid CPF format."""
        # Arrange
        use_case = AuthenticateCustomerUseCase(
            customer_repository=mock_customer_repository,
            token_generator=mock_token_generator,
        )

        request = AuthenticationRequest(cpf="00000000000")

        # Act
        response = use_case.execute(request)

        # Assert
        assert response.success is False
        assert response.token is None
        assert "CPF inválido" in response.message

        # Repository should not be called for invalid CPF
        mock_customer_repository.find_by_cpf.assert_not_called()
        mock_token_generator.generate.assert_not_called()

    def test_authentication_customer_not_found(
        self, mock_customer_repository, mock_token_generator
    ):
        """Test authentication when customer not found."""
        # Arrange
        mock_customer_repository.find_by_cpf.return_value = None

        use_case = AuthenticateCustomerUseCase(
            customer_repository=mock_customer_repository,
            token_generator=mock_token_generator,
        )

        request = AuthenticationRequest(cpf="52998224725")

        # Act
        response = use_case.execute(request)

        # Assert
        assert response.success is False
        assert response.token is None
        assert "não encontrado" in response.message.lower()

        mock_customer_repository.find_by_cpf.assert_called_once_with("52998224725")
        mock_token_generator.generate.assert_not_called()

    def test_authentication_with_formatted_cpf(
        self, mock_customer_repository, mock_token_generator, sample_customer
    ):
        """Test authentication with formatted CPF."""
        # Arrange
        mock_customer_repository.find_by_cpf.return_value = sample_customer
        mock_token_generator.generate.return_value = "fake-jwt-token"

        use_case = AuthenticateCustomerUseCase(
            customer_repository=mock_customer_repository,
            token_generator=mock_token_generator,
        )

        request = AuthenticationRequest(cpf="111.444.777-35")

        # Act
        response = use_case.execute(request)

        # Assert
        assert response.success is True
        # CPF should be cleaned before searching
        mock_customer_repository.find_by_cpf.assert_called_once_with("11144477735")

    def test_authentication_request_dto(self):
        """Test AuthenticationRequest DTO."""
        request = AuthenticationRequest(cpf="11144477735")
        assert request.cpf == "11144477735"

    def test_authentication_response_dto_success(self):
        """Test AuthenticationResponse DTO for success."""
        response = AuthenticationResponse(
            success=True,
            token="fake-token",
            message="Success",
            customer_id=1,
            customer_name="João",
        )

        assert response.success is True
        assert response.token == "fake-token"
        assert response.message == "Success"
        assert response.customer_id == 1
        assert response.customer_name == "João"

    def test_authentication_response_dto_failure(self):
        """Test AuthenticationResponse DTO for failure."""
        response = AuthenticationResponse(success=False, message="Error")

        assert response.success is False
        assert response.token is None
        assert response.message == "Error"
        assert response.customer_id is None
        assert response.customer_name is None
