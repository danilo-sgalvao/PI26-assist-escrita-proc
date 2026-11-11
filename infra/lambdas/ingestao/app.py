"""Recebe uma redação autenticada e registra uma versão imutável."""
import base64
import binascii
import json
import logging
import os
import uuid
import boto3
from comum import banco, resposta

log = logging.getLogger(__name__)
MAX_BYTES = 100_000


def lambda_handler(event, context):
    claims = (event.get("requestContext", {}).get("authorizer") or {}).get("claims") or {}
    aluno = claims.get("sub")
    if not isinstance(aluno, str) or not aluno:
        return resposta(401, {"mensagem": "Autenticação necessária."})
    body = event.get("body") or ""
    if not isinstance(body, str):
        return resposta(400, {"mensagem": "Requisição inválida."})
    try:
        raw = base64.b64decode(body, validate=True) if event.get("isBase64Encoded") else body.encode("utf-8")
        if len(raw) > MAX_BYTES:
            return resposta(413, {"mensagem": "Redação excede o limite permitido."})
        dados = json.loads(raw)
    except (ValueError, UnicodeError, binascii.Error):
        return resposta(400, {"mensagem": "Requisição inválida."})
    if not isinstance(dados, dict) or not isinstance(dados.get("texto"), str) or not dados["texto"].strip():
        return resposta(400, {"mensagem": "Informe o texto da redação."})
    if dados.get("consentimento") is not True:
        return resposta(400, {"mensagem": "Confirme o processamento da revisão."})
    producao = str(uuid.uuid4())
    chave = "redacoes/" + producao + ".txt"
    try:
        with banco() as conn:
            conn.execute("INSERT INTO revisoes (id, aluno_sub, chave_s3, status) VALUES (%s,%s,%s,%s)",
                         (producao, aluno, chave, "PROCESSANDO"))
        boto3.client("s3").put_object(Bucket=os.environ["BUCKET_REDACOES"], Key=chave,
                                      Body=dados["texto"].encode("utf-8"), ContentType="text/plain; charset=utf-8")
    except Exception:
        log.error("Falha ao registrar submissão", exc_info=False)
        return resposta(503, {"mensagem": "Não foi possível registrar a submissão."})
    return resposta(202, {"id_producao": producao, "status": "PROCESSANDO"})
