import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1] / "lambdas"


def carregar(nome):
    spec = importlib.util.spec_from_file_location(nome, ROOT / nome / "app.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


ingestao = carregar("ingestao")
ws = carregar("conexao_websocket")
processador = carregar("processador_bedrock")


class TestLambdas(unittest.TestCase):
    def test_ingestao_exige_identidade_e_nao_confirma_sem_persistir(self):
        self.assertEqual(ingestao.lambda_handler({}, None)["statusCode"], 401)
        event = {"requestContext": {"authorizer": {"claims": {"sub": "aluno"}}},
                 "body": json.dumps({"texto": "Um texto."})}
        self.assertEqual(ingestao.lambda_handler(event, None)["statusCode"], 503)
        event["body"] = "{}"
        self.assertEqual(ingestao.lambda_handler(event, None)["statusCode"], 400)

    def test_websocket_nao_aceita_conexao_sem_identidade_ou_persistencia(self):
        event = {"requestContext": {"routeKey": "$connect", "connectionId": "abc"}}
        self.assertEqual(ws.lambda_handler(event, None)["statusCode"], 401)
        event["requestContext"]["authorizer"] = {"principalId": "aluno"}
        self.assertEqual(ws.lambda_handler(event, None)["statusCode"], 503)

    def test_sqs_identifica_versao_e_retenta_mensagens_nao_processadas(self):
        s3 = {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put",
              "s3": {"bucket": {"name": "ensaios"},
                     "object": {"key": "redacoes%2Fum+texto", "versionId": "v1"}}}]}
        self.assertEqual(processador.ler_eventos_s3(json.dumps(s3)), [("ensaios", "redacoes/um texto", "v1")])
        result = processador.lambda_handler({"Records": [
            {"messageId": "a", "body": json.dumps(s3)}, {"messageId": "b", "body": "{}"}]}, None)
        self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "a"}, {"itemIdentifier": "b"}]})
        del s3["Records"][0]["s3"]["object"]["versionId"]
        with self.assertRaises(ValueError):
            processador.ler_eventos_s3(json.dumps(s3))


if __name__ == "__main__":
    unittest.main()
