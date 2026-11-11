"""Validação inicial dos eventos do WebSocket."""


def lambda_handler(event, context):
    request = event.get("requestContext") or {}
    route = request.get("routeKey")
    connection_id = request.get("connectionId")
    if route not in ("$connect", "$disconnect") or not isinstance(connection_id, str) or not connection_id:
        return {"statusCode": 400, "body": "Evento inválido."}
    if route == "$connect":
        authorizer = request.get("authorizer") or {}
        if not authorizer.get("principalId"):
            return {"statusCode": 401, "body": "Autenticação necessária."}
    # A conexão não é aceita enquanto o repositório de conexões não estiver disponível.
    return {"statusCode": 503, "body": "Serviço temporariamente indisponível."}
