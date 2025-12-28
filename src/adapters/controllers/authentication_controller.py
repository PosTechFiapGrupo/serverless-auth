import json
from typing import Dict, Any

from src.application.use_cases.authenticate_customer import (
    AuthenticateCustomerUseCase,
    AuthenticationRequest
)


class AuthenticationController:
    """
    Controller for authentication endpoint.
    
    Responsibilities:
    - Parse HTTP request
    - Validate input
    - Call use case
    - Format HTTP response
    """
    
    def __init__(self, use_case: AuthenticateCustomerUseCase):
        self._use_case = use_case
    
    def handle(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle authentication request.
        
        Args:
            event: AWS Lambda event (API Gateway format)
            
        Returns:
            HTTP response in API Gateway format
        """
        try:
            body = self._parse_body(event)
            
            if "cpf" not in body:
                return self._bad_request("Campo 'cpf' é obrigatório")
            
            request = AuthenticationRequest(cpf=body["cpf"])
            
            response = self._use_case.execute(request)
            
            if response.success:
                return self._ok({
                    "token": response.token,
                    "message": response.message,
                    "customer": {
                        "id": response.customer_id,
                        "name": response.customer_name
                    }
                })
            else:
                return self._unauthorized(response.message)
                
        except json.JSONDecodeError:
            return self._bad_request("JSON inválido")
        except Exception as e:
            return self._internal_error(str(e))
    
    @staticmethod
    def _parse_body(event: Dict[str, Any]) -> Dict[str, Any]:
        """Parse request body."""
        body = event.get("body", "{}")
        if isinstance(body, str):
            return json.loads(body)
        return body
    
    @staticmethod
    def _ok(data: Dict[str, Any]) -> Dict[str, Any]:
        """Return 200 OK response."""
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps(data, ensure_ascii=False)
        }
    
    @staticmethod
    def _bad_request(message: str) -> Dict[str, Any]:
        """Return 400 Bad Request response."""
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": message}, ensure_ascii=False)
        }
    
    @staticmethod
    def _unauthorized(message: str) -> Dict[str, Any]:
        """Return 401 Unauthorized response."""
        return {
            "statusCode": 401,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": message}, ensure_ascii=False)
        }
    
    @staticmethod
    def _internal_error(message: str) -> Dict[str, Any]:
        """Return 500 Internal Server Error response."""
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": "Erro interno do servidor"}, ensure_ascii=False)
        }
