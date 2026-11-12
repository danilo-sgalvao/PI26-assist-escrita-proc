"""Configuração e acesso PostgreSQL autenticado por IAM."""
import json
import os

import boto3
import psycopg


def banco():
    host = os.environ["DB_HOST"]
    port = int(os.environ.get("DB_PORT", "5432"))
    user = os.environ["DB_USER"]
    token = boto3.client("rds").generate_db_auth_token(DBHostname=host, Port=port, DBUsername=user)
    return psycopg.connect(host=host, port=port, dbname=os.environ["DB_NAME"], user=user,
                           password=token, sslmode="verify-full",
                           sslrootcert=os.environ["DB_CA_PATH"], connect_timeout=5)


def resposta(status, data):
    headers = {"Content-Type": "application/json"}
    origin = os.environ.get("FRONTEND_ORIGIN")
    if origin:
        headers.update({"Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Headers": "Content-Type,Authorization",
                        "Access-Control-Allow-Methods": "GET,POST,OPTIONS"})
    return {"statusCode": status, "headers": headers,
            "body": json.dumps(data, ensure_ascii=False)}
