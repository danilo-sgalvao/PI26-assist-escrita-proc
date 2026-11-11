"""Tratamento de lote SQS que preserva mensagens ainda não processadas."""
import json
from urllib.parse import unquote_plus


def ler_eventos_s3(body):
    payload = json.loads(body)
    if not isinstance(payload, dict) or not isinstance(payload.get("Records"), list) or not payload["Records"]:
        raise ValueError("Evento S3 inválido")
    eventos = []
    for record in payload["Records"]:
        if record.get("eventSource") != "aws:s3" or not record.get("eventName", "").startswith("ObjectCreated:"):
            raise ValueError("Evento S3 inválido")
        obj = record["s3"]["object"]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(obj["key"])
        version = obj.get("versionId")
        if not isinstance(bucket, str) or not bucket or not key.startswith("redacoes/") or not isinstance(version, str) or not version or version == "null":
            raise ValueError("Versão ou objeto inválido")
        eventos.append((bucket, key, version))
    return eventos


def lambda_handler(event, context):
    falhas = []
    for registro in event.get("Records", []):
        try:
            ler_eventos_s3(registro["body"])
            # Sem persistência e validação de autoria, a mensagem deve ser reprocessada.
            raise RuntimeError("Processamento de IA ainda não configurado")
        except (ValueError, KeyError, TypeError, RuntimeError):
            falhas.append({"itemIdentifier": registro["messageId"]})
    return {"batchItemFailures": falhas}
