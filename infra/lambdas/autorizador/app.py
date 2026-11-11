"""Autoriza conexão usando token de acesso Cognito."""
import base64
import json
import os
import boto3


def lambda_handler(event, context):
    headers = {k.lower(): v for k, v in (event.get("headers") or {}).items()}
    token = headers.get("authorization", "")
    if token.lower().startswith("bearer "):
        token = token[7:]
    if not token and (event.get("queryStringParameters") or {}):
        token = event["queryStringParameters"].get("token", "")
    try:
        if not isinstance(token, str) or len(token) > 8192:
            raise ValueError("token inválido")
        resultado = boto3.client("cognito-idp").get_user(AccessToken=token)
        parte = token.split(".")[1]
        claims = json.loads(base64.urlsafe_b64decode(parte + "=" * (-len(parte) % 4)))
        atributos = {x["Name"]: x["Value"] for x in resultado["UserAttributes"]}
        if claims.get("iss") != os.environ["COGNITO_ISSUER"] or claims.get("client_id") != os.environ["COGNITO_CLIENT_ID"] or claims.get("token_use") != "access" or claims.get("sub") != atributos.get("sub"):
            raise ValueError("token inválido")
        principal = claims["sub"]
    except Exception:
        raise Exception("Unauthorized") from None
    return {"principalId": principal, "policyDocument": {"Version": "2012-10-17",
            "Statement": [{"Action": "execute-api:Invoke", "Effect": "Allow", "Resource": event["methodArn"]}]}}
