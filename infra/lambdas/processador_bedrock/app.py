"""Processa eventos S3 recebidos via SNS/SQS e envia notificação."""
import json
import logging
import os
import re
import uuid
from urllib.parse import unquote_plus
import boto3
from comum import banco

log = logging.getLogger(__name__)
ORIENTACOES = {
    "ESTRUTURA": "Verifique se a introdução, o desenvolvimento e a conclusão estão claramente organizados.",
    "PARAGRAFOS": "Revise a divisão em parágrafos e confira se cada um desenvolve uma ideia.",
    "FRASES": "Revise o tamanho das frases e avalie se estão claras.",
    "REVISAO": "Releia a redação para verificar clareza, coerência e pontuação.",
}


def ler_eventos_s3(body):
    payload = json.loads(body)
    if not isinstance(payload, dict) or not isinstance(payload.get("Records"), list) or not payload["Records"]:
        raise ValueError("Evento S3 inválido")
    eventos = []
    for record in payload["Records"]:
        if not isinstance(record, dict) or record.get("eventSource") != "aws:s3" or not record.get("eventName", "").startswith("ObjectCreated:"):
            raise ValueError("Evento S3 inválido")
        obj = record["s3"]["object"]
        bucket = record["s3"]["bucket"]["name"]
        key, version = unquote_plus(obj["key"]), obj.get("versionId")
        if bucket != os.environ["BUCKET_REDACOES"] or not isinstance(version, str) or not version or version == "null":
            raise ValueError("Origem ou versão inválida")
        match = re.fullmatch(r"redacoes/([0-9a-f-]{36})\.txt", key)
        if not match or str(uuid.UUID(match.group(1))) != match.group(1):
            raise ValueError("Chave inválida")
        eventos.append((bucket, key, version, match.group(1)))
    return eventos


def analisar(texto):
    palavras = re.findall(r"\b\w+\b", texto, flags=re.UNICODE)
    frases = [x for x in re.split(r"[.!?]+", texto) if x.strip()]
    paragrafos = [x for x in re.split(r"\n\s*\n", texto) if x.strip()]
    # Nenhuma palavra ou identificador do texto é enviado ao modelo.
    metricas = {"palavras": len(palavras), "frases": len(frases), "paragrafos": len(paragrafos)}
    resposta = boto3.client("bedrock-runtime").converse(
        modelId=os.environ["BEDROCK_MODEL_ID"],
        system=[{"text": "Retorne somente um array JSON com até três códigos entre ESTRUTURA, PARAGRAFOS, FRASES e REVISAO. Não escreva texto."}],
        messages=[{"role": "user", "content": [{"text": json.dumps(metricas)}]}],
        inferenceConfig={"maxTokens": 100, "temperature": 0},
    )
    if resposta.get("stopReason") != "end_turn":
        raise ValueError("Resposta Bedrock não concluída")
    blocos = resposta["output"]["message"]["content"]
    if len(blocos) != 1 or set(blocos[0]) != {"text"}:
        raise ValueError("Resposta Bedrock inválida")
    codigos = json.loads(blocos[0]["text"])
    if not isinstance(codigos, list) or not 1 <= len(codigos) <= 3 or any(not isinstance(x, str) or x not in ORIENTACOES for x in codigos):
        raise ValueError("Categorias inválidas")
    return [ORIENTACOES[c] for c in dict.fromkeys(codigos)]


def processar(bucket, chave, versao, producao):
    with banco() as conn:
        linha = conn.execute("SELECT aluno_sub FROM revisoes WHERE id=%s AND chave_s3=%s", (producao, chave)).fetchone()
    if not linha:
        raise ValueError("Redação não registrada")
    aluno = linha[0]
    tabela = boto3.resource("dynamodb").Table(os.environ["TABELA_SUGESTOES"])
    existente = tabela.get_item(Key={"id_producao": producao}, ConsistentRead=True).get("Item")
    if existente and existente.get("versao_s3") != versao:
        raise ValueError("Versão divergente")
    if not existente:
        objeto = boto3.client("s3").get_object(Bucket=bucket, Key=chave, VersionId=versao)
        with objeto["Body"] as stream:
            dados = stream.read(100_001)
        if len(dados) > 100_000:
            raise ValueError("Redação excede limite")
        sugestoes = analisar(dados.decode("utf-8"))
        try:
            tabela.put_item(Item={"id_producao": producao, "versao_s3": versao, "sugestoes": sugestoes}, ConditionExpression="attribute_not_exists(id_producao)")
        except tabela.meta.client.exceptions.ConditionalCheckFailedException:
            existente = tabela.get_item(Key={"id_producao": producao}, ConsistentRead=True).get("Item")
            if not existente or existente.get("versao_s3") != versao:
                raise ValueError("Versão divergente")
    with banco() as conn:
        conn.execute("UPDATE revisoes SET status='CONCLUIDO' WHERE id=%s", (producao,))
        conexoes = conn.execute("SELECT connection_id FROM conexoes WHERE aluno_sub=%s", (aluno,)).fetchall()
    gateway = boto3.client("apigatewaymanagementapi", endpoint_url=os.environ["WEBSOCKET_ENDPOINT"])
    mensagem = json.dumps({"id_producao": producao, "tipo": "REVISAO_DISPONIVEL"}).encode("utf-8")
    for (connection_id,) in conexoes:
        try:
            gateway.post_to_connection(ConnectionId=connection_id, Data=mensagem)
        except gateway.exceptions.GoneException:
            with banco() as conn:
                conn.execute("DELETE FROM conexoes WHERE connection_id=%s", (connection_id,))


def lambda_handler(event, context):
    falhas = []
    for registro in event.get("Records", []):
        try:
            for dados in ler_eventos_s3(registro["body"]):
                processar(*dados)
        except Exception:
            log.error("Falha no processamento de mensagem", exc_info=False)
            falhas.append({"itemIdentifier": registro["messageId"]})
    return {"batchItemFailures": falhas}
