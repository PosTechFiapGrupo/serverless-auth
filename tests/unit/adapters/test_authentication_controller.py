"""Unit tests for AuthenticationController."""

import json
import pytest
from unittest.mock import Mock

from src.adapters.controllers.authentication_controller import AuthenticationController
from src.application.use_cases.authenticate_customer import AuthenticationResponse


class TestAuthenticationController:
    """Test suite for authentication controller."""

    def test_successful_authentication(self):
        """Test successful authentication request."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute.return_value = AuthenticationResponse(
            success=True,
            token="fake-jwt-token",
            message="Autenticação realizada com sucesso",
            customer_id=1,
            customer_name="João da Silva",
        )

        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": json.dumps({"cpf": "11144477735"})}

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 200
        assert "Content-Type" in response["headers"]
        assert response["headers"]["Content-Type"] == "application/json"

        body = json.loads(response["body"])
        assert body["token"] == "fake-jwt-token"
        assert body["customer"]["id"] == 1
        assert body["customer"]["name"] == "João da Silva"

    def test_authentication_with_missing_cpf(self):
        """Test authentication with missing CPF field."""
        # Arrange
        mock_use_case = Mock()
        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": json.dumps({})}

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "obrigatório" in body["error"].lower()

        # Use case should not be called
        mock_use_case.execute.assert_not_called()

    def test_authentication_unauthorized(self):
        """Test authentication returning unauthorized."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute.return_value = AuthenticationResponse(
            success=False, message="CPF inválido"
        )

        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": json.dumps({"cpf": "00000000000"})}

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 401
        body = json.loads(response["body"])
        assert body["error"] == "CPF inválido"

    def test_authentication_with_invalid_json(self):
        """Test authentication with invalid JSON."""
        # Arrange
        mock_use_case = Mock()
        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": "invalid-json"}

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 400
        body = json.loads(response["body"])
        assert "JSON inválido" in body["error"]

    def test_authentication_with_exception(self):
        """Test authentication when exception occurs."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute.side_effect = Exception("Database error")

        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": json.dumps({"cpf": "12345678901"})}

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 500
        body = json.loads(response["body"])
        assert "Erro interno" in body["error"]

    def test_authentication_with_dict_body(self):
        """Test authentication when body is already a dict."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute.return_value = AuthenticationResponse(
            success=True,
            token="fake-jwt-token",
            message="Autenticação realizada com sucesso",
            customer_id=1,
            customer_name="João da Silva",
        )

        controller = AuthenticationController(use_case=mock_use_case)

        event = {
            "body": {"cpf": "11144477735"}  # Dict instead of string
        }

        # Act
        response = controller.handle(event)

        # Assert
        assert response["statusCode"] == 200

    def test_cors_headers_in_response(self):
        """Test that CORS headers are present in all responses."""
        # Arrange
        mock_use_case = Mock()
        mock_use_case.execute.return_value = AuthenticationResponse(
            success=True,
            token="fake-jwt-token",
            message="Success",
            customer_id=1,
            customer_name="João",
        )

        controller = AuthenticationController(use_case=mock_use_case)

        event = {"body": json.dumps({"cpf": "11144477735"})}

        # Act
        response = controller.handle(event)

        # Assert
        assert "Access-Control-Allow-Origin" in response["headers"]
        assert response["headers"]["Access-Control-Allow-Origin"] == "*"
