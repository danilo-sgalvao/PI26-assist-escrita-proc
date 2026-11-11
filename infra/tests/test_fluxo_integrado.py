"""Teste integrado opcional com PostgreSQL descartável e AWS simulada."""
import importlib
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch
import psycopg

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lambdas"))
ingestao = importlib.import_module("ingestao.app")
processador = importlib.import_module("processador_bedrock.app")
consulta = importlib.import_module("consulta.app")
ws = importlib.import_module("conexao_websocket.app")


@unittest.skipUnless(os.getenv("TEST_POSTGRES_DSN"), "PostgreSQL de teste não configurado")
class FluxoIntegrado(unittest.TestCase):
    def test_submissao_processamento_consulta_e_notificacao(self):
        dsn = os.environ["TEST_POSTGRES_DSN"]
        def banco(): return psycopg.connect(dsn)
        with banco() as conn:
            sql = (Path(__file__).resolve().parents[1] / "migrations" / "001_inicial.sql").read_text(encoding="utf-8")
            conn.execute(sql)
        objetos, itens, notificacoes = {}, {}, []
        class S3:
            def put_object(self, **kw): objetos[kw["Key"]] = kw["Body"]
            def get_object(self, **kw): return {"Body": io.BytesIO(objetos[kw["Key"]])}
        class Tabela:
            def get_item(self, Key, **kw): return {"Item": itens.get(Key["id_producao"])}
            def put_item(self, Item, **kw): itens[Item["id_producao"]] = Item
        class Dynamo:
            def Table(self, name): return Tabela()
        class Bedrock:
            def converse(self, **kw):
                self.request = kw
                return {"stopReason": "end_turn", "output": {"message": {"content": [{"text": '["REVISAO"]'}]}}}
        class Gateway:
            def post_to_connection(self, **kw): notificacoes.append(kw)
        s3, bedrock, gateway = S3(), Bedrock(), Gateway()
        def cliente(service, **kwargs): return {"s3": s3, "bedrock-runtime": bedrock, "apigatewaymanagementapi": gateway}[service]
        env = {"BUCKET_REDACOES": "bucket", "TABELA_SUGESTOES": "tabela", "BEDROCK_MODEL_ID": "modelo", "WEBSOCKET_ENDPOINT": "https://example.com"}
        with patch.object(ingestao, "banco", banco), patch.object(processador, "banco", banco), patch.object(consulta, "banco", banco), patch.object(ws, "banco", banco), patch.object(ingestao.boto3, "client", side_effect=cliente), patch.object(processador.boto3, "resource", return_value=Dynamo()), patch.dict(os.environ, env):
            evento_ws = {"requestContext": {"routeKey": "$connect", "connectionId": "conexao-1", "authorizer": {"principalId": "aluno"}}}
            self.assertEqual(ws.lambda_handler(evento_ws, None)["statusCode"], 200)
            post = {"requestContext": {"authorizer": {"claims": {"sub": "aluno"}}}, "body": json.dumps({"texto": "Texto particular.", "consentimento": True})}
            resposta = ingestao.lambda_handler(post, None)
            self.assertEqual(resposta["statusCode"], 202)
            identificador = json.loads(resposta["body"])["id_producao"]
            chave = f"redacoes/{identificador}.txt"
            s3_event = {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put", "s3": {"bucket": {"name": "bucket"}, "object": {"key": chave, "versionId": "v1"}}}]}
            evento_sqs = {"Records": [{"messageId": "m1", "body": json.dumps(s3_event)}]}
            self.assertEqual(processador.lambda_handler(evento_sqs, None), {"batchItemFailures": []})
            self.assertEqual(processador.lambda_handler(evento_sqs, None), {"batchItemFailures": []})
            self.assertEqual(len(itens), 1)
            get = {"requestContext": {"authorizer": {"claims": {"sub": "aluno"}}}, "pathParameters": {"id": identificador}}
            resultado = consulta.lambda_handler(get, None)
            self.assertEqual(json.loads(resultado["body"])["status"], "CONCLUIDO")
            self.assertEqual(len(notificacoes), 2)
            self.assertNotIn("Texto particular", str(bedrock.request))
            get["requestContext"]["authorizer"]["claims"]["sub"] = "outro"
            self.assertEqual(consulta.lambda_handler(get, None)["statusCode"], 404)


if __name__ == "__main__": unittest.main()
