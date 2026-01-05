import json

def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Acesso autorizado",
            "claims": event.get("requestContext", {}).get("authorizer", {})
        })
    }
