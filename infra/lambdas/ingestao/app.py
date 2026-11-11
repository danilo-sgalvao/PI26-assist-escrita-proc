"""Validação da entrada da API de submissão."""
import base64
import binascii
import json

MAX_BYTES = 100_000


def resposta(status, mensagem):
    return {"statusCode": status, "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"mensagem": mensagem}, ensure_ascii=False)}


def lambda_handler(event, context):
    claims = (event.get("requestContext", {}).get("authorizer") or {}).get("claims") or {}
    if not claims.get("sub"):
        return resposta(401, "Autenticação necessária.")
    body = event.get("body") or ""
    if not isinstance(body, str):
        return resposta(400, "Requisição inválida.")
    try:
        raw = base64.b64decode(body, validate=True) if event.get("isBase64Encoded") else body.encode("utf-8")
        if len(raw) > MAX_BYTES:
            return resposta(413, "Redação excede o limite permitido.")
        dados = json.loads(raw)
    except (ValueError, UnicodeError, binascii.Error):
        return resposta(400, "Requisição inválida.")
    if not isinstance(dados, dict) or not isinstance(dados.get("texto"), str) or not dados["texto"].strip():
        return resposta(400, "Informe o texto da redação.")
    # A persistência ainda não está conectada: nunca confirmar uma submissão não salva.
    return resposta(503, "Submissão temporariamente indisponível.")
