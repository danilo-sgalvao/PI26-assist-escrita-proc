"""Registra conexões autenticadas e remove conexões encerradas."""
import logging
from comum import banco

log = logging.getLogger(__name__)


def lambda_handler(event, context):
    request = event.get("requestContext") or {}
    route, connection_id = request.get("routeKey"), request.get("connectionId")
    if route not in ("$connect", "$disconnect") or not isinstance(connection_id, str) or not connection_id:
        return {"statusCode": 400}
    aluno = (request.get("authorizer") or {}).get("principalId")
    if route == "$connect" and not aluno:
        return {"statusCode": 401}
    try:
        with banco() as conn:
            if route == "$connect":
                conn.execute("INSERT INTO conexoes (connection_id, aluno_sub) VALUES (%s,%s) ON CONFLICT (connection_id) DO UPDATE SET aluno_sub=EXCLUDED.aluno_sub", (connection_id, aluno))
            else:
                conn.execute("DELETE FROM conexoes WHERE connection_id=%s", (connection_id,))
    except Exception:
        log.error("Falha no gerenciamento da conexão", exc_info=False)
        return {"statusCode": 503}
    return {"statusCode": 200}
