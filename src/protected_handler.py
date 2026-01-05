import json
from loguru import logger

def lambda_handler(event, context):
    logger.info("Protected endpoint accessed", request_id=context.request_id)
    
    claims = event.get("requestContext", {}).get("authorizer", {})
    logger.debug("JWT claims extracted", claims=claims)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Acesso autorizado",
            "claims": claims
        })
    }
