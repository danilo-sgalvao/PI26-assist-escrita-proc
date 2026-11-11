import base64
import importlib
import io
import json
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lambdas"))
ingestao = importlib.import_module("ingestao.app")
ws = importlib.import_module("conexao_websocket.app")
auth = importlib.import_module("autorizador.app")
consulta = importlib.import_module("consulta.app")
processador = importlib.import_module("processador_bedrock.app")
ID = "e4a6d9f5-2069-4097-8faf-402e10fa08cc"


def evento_s3(version="v1"):
    return {"Records": [{"eventSource": "aws:s3", "eventName": "ObjectCreated:Put",
            "s3": {"bucket": {"name": "bucket"}, "object": {
                "key": f"redacoes%2F{ID}.txt", "versionId": version}}}]}


def conexao(linhas=None):
    conn = MagicMock()
    conn.__enter__.return_value = conn
    if linhas is not None:
        conn.execute.return_value.fetchone.return_value = linhas
    return conn


class TestLambdas(unittest.TestCase):
    def test_ingestao_exige_identidade_consentimento_e_persiste(self):
        self.assertEqual(ingestao.lambda_handler({}, None)["statusCode"], 401)
        event = {"requestContext": {"authorizer": {"claims": {"sub": "aluno"}}},
                 "body": json.dumps({"texto": "Texto do aluno."})}
        self.assertEqual(ingestao.lambda_handler(event, None)["statusCode"], 400)
        event["body"] = json.dumps({"texto": "Texto do aluno.", "consentimento": True})
        conn, s3 = conexao(), MagicMock()
        with patch.object(ingestao, "banco", return_value=conn), patch.object(ingestao.boto3, "client", return_value=s3), patch.dict(os.environ, {"BUCKET_REDACOES": "bucket"}):
            result = ingestao.lambda_handler(event, None)
        self.assertEqual(result["statusCode"], 202)
        self.assertEqual(json.loads(result["body"])["status"], "PROCESSANDO")
        s3.put_object.assert_called_once()
        self.assertEqual(s3.put_object.call_args.kwargs["Body"], b"Texto do aluno.")
        conn.execute.assert_called_once()

    def test_ingestao_nao_confirma_se_s3_falhar(self):
        event = {"requestContext": {"authorizer": {"claims": {"sub": "aluno"}}},
                 "body": json.dumps({"texto": "texto", "consentimento": True})}
        s3 = MagicMock(); s3.put_object.side_effect = RuntimeError()
        with patch.object(ingestao, "banco", return_value=conexao()), patch.object(ingestao.boto3, "client", return_value=s3), patch.dict(os.environ, {"BUCKET_REDACOES": "bucket"}):
            self.assertEqual(ingestao.lambda_handler(event, None)["statusCode"], 503)

    def test_websocket_exige_identidade_e_registra_ou_remove(self):
        event = {"requestContext": {"routeKey": "$connect", "connectionId": "abc"}}
        self.assertEqual(ws.lambda_handler(event, None)["statusCode"], 401)
        event["requestContext"]["authorizer"] = {"principalId": "aluno"}
        conn = conexao()
        with patch.object(ws, "banco", return_value=conn):
            self.assertEqual(ws.lambda_handler(event, None)["statusCode"], 200)
            event["requestContext"]["routeKey"] = "$disconnect"
            self.assertEqual(ws.lambda_handler(event, None)["statusCode"], 200)
        self.assertEqual(conn.execute.call_count, 2)

    def test_autorizador_valida_pool_cliente_e_token_no_cognito(self):
        claims = {"iss": "pool", "client_id": "cliente", "token_use": "access", "sub": "aluno"}
        payload = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
        event = {"queryStringParameters": {"token": "x." + payload + ".x"}, "methodArn": "arn"}
        cognito = MagicMock(); cognito.get_user.return_value = {"UserAttributes": [{"Name": "sub", "Value": "aluno"}]}
        with patch.object(auth.boto3, "client", return_value=cognito), patch.dict(os.environ, {"COGNITO_ISSUER": "pool", "COGNITO_CLIENT_ID": "cliente"}):
            self.assertEqual(auth.lambda_handler(event, None)["principalId"], "aluno")
            cognito.get_user.side_effect = ValueError()
            with self.assertRaises(Exception): auth.lambda_handler(event, None)

    def test_analise_nao_envia_texto_ao_modelo_e_apenas_retorna_frases_fixas(self):
        bedrock = MagicMock()
        bedrock.converse.return_value = {"stopReason": "end_turn", "output": {"message": {"content": [{"text": '["REVISAO"]'}]}}}
        with patch.object(processador.boto3, "client", return_value=bedrock), patch.dict(os.environ, {"BEDROCK_MODEL_ID": "modelo"}):
            saida = processador.analisar("Nome Confidencial. Redação privada!")
        self.assertEqual(saida, [processador.ORIENTACOES["REVISAO"]])
        self.assertNotIn("Confidencial", str(bedrock.converse.call_args))
        bedrock.converse.return_value["output"]["message"]["content"][0]["text"] = '["texto inventado"]'
        with patch.object(processador.boto3, "client", return_value=bedrock), patch.dict(os.environ, {"BEDROCK_MODEL_ID": "modelo"}):
            with self.assertRaises(ValueError): processador.analisar("texto")

    def test_sqs_valida_origem_versao_e_relata_apenas_falha(self):
        mensagem = {"messageId": "a", "body": json.dumps(evento_s3())}
        invalida = {"messageId": "b", "body": "{}"}
        with patch.dict(os.environ, {"BUCKET_REDACOES": "bucket"}), patch.object(processador, "processar") as executar:
            result = processador.lambda_handler({"Records": [mensagem, invalida]}, None)
            self.assertEqual(result, {"batchItemFailures": [{"itemIdentifier": "b"}]})
            executar.assert_called_once_with("bucket", f"redacoes/{ID}.txt", "v1", ID)
            with self.assertRaises(ValueError): processador.ler_eventos_s3(json.dumps(evento_s3("null")))

    def test_processamento_salva_e_notifica_usuario(self):
        tabela = MagicMock(); tabela.get_item.return_value = {}
        dynamo = MagicMock(); dynamo.Table.return_value = tabela
        s3 = MagicMock(); s3.get_object.return_value = {"Body": io.BytesIO(b"uma redacao.")}
        gateway = MagicMock()
        conn = conexao(("aluno",)); conn.execute.return_value.fetchall.return_value = [("conexao",)]
        def cliente(service, **kwargs): return {"s3": s3, "apigatewaymanagementapi": gateway}[service]
        with patch.object(processador, "banco", return_value=conn), patch.object(processador.boto3, "resource", return_value=dynamo), patch.object(processador.boto3, "client", side_effect=cliente), patch.object(processador, "analisar", return_value=["orientacao"]), patch.dict(os.environ, {"TABELA_SUGESTOES": "tabela", "WEBSOCKET_ENDPOINT": "https://example.com"}):
            processador.processar("bucket", f"redacoes/{ID}.txt", "v1", ID)
        s3.get_object.assert_called_once_with(Bucket="bucket", Key=f"redacoes/{ID}.txt", VersionId="v1")
        tabela.put_item.assert_called_once()
        gateway.post_to_connection.assert_called_once()

    def test_consulta_nega_acesso_a_outro_aluno(self):
        event = {"requestContext": {"authorizer": {"claims": {"sub": "outro"}}}, "pathParameters": {"id": ID}}
        conn = conexao(); conn.execute.return_value.fetchone.return_value = None
        with patch.object(consulta, "banco", return_value=conn):
            self.assertEqual(consulta.lambda_handler(event, None)["statusCode"], 404)
        self.assertEqual(conn.execute.call_args.args[1], (ID, "outro"))


if __name__ == "__main__":
    unittest.main()
