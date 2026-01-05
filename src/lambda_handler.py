from typing import Dict, Any
from loguru import logger

from src.adapters.controllers.authentication_controller import AuthenticationController
from src.adapters.gateways.customer_repository import CustomerRepository
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.security.jwt_service import JWTTokenGenerator
from src.application.use_cases.authenticate_customer import AuthenticateCustomerUseCase


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler for authentication.

    This is the entry point for AWS Lambda.
    Implements Dependency Injection manually (composition root).

    Args:
        event: API Gateway event
        context: Lambda context

    Returns:
        API Gateway response
    """
    logger.info("Authentication Lambda invoked", request_id=context.request_id)

    DatabaseConnection.initialize()
    logger.debug("Database connection initialized")

    with DatabaseConnection.get_session() as session:
        customer_repository = CustomerRepository(session)
        token_generator = JWTTokenGenerator()

        use_case = AuthenticateCustomerUseCase(
            customer_repository=customer_repository, token_generator=token_generator
        )

        controller = AuthenticationController(use_case)

        response = controller.handle(event)
        logger.info("Authentication request completed", status_code=response.get('statusCode'))
        return response
