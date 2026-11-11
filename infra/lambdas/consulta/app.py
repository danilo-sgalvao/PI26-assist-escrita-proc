"""Recupera uma revisão apenas para seu proprietário autenticado."""
import os
import boto3
from comum import banco, resposta


def lambda_handler(event, context):
    aluno = ((event.get("requestContext", {}).get("authorizer") or {}).get("claims") or {}).get("sub")
    if not aluno:
        return resposta(401, {"mensagem": "Autenticação necessária."})
    identificador = (event.get("pathParameters") or {}).get("id", "")
    try:
        import uuid
        identificador = str(uuid.UUID(identificador))
    except (ValueError, TypeError):
        return resposta(404, {"mensagem": "Revisão não encontrada."})
    try:
        with banco() as conn:
            linha = conn.execute("SELECT status FROM revisoes WHERE id=%s AND aluno_sub=%s", (identificador, aluno)).fetchone()
        if not linha:
            return resposta(404, {"mensagem": "Revisão não encontrada."})
        item = boto3.resource("dynamodb").Table(os.environ["TABELA_SUGESTOES"]).get_item(Key={"id_producao": identificador}, ConsistentRead=True).get("Item")
        return resposta(200, {"id_producao": identificador, "status": linha[0], "sugestoes": item.get("sugestoes", []) if item else []})
    except Exception:
        return resposta(503, {"mensagem": "Consulta temporariamente indisponível."})
