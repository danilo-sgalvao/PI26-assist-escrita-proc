"""Executa teste integrado num container PostgreSQL criado para o teste."""
import os
from pathlib import Path
import subprocess
import sys
import time
import uuid
import psycopg

raiz = Path(__file__).resolve().parents[2]
nome = "assistente-teste-" + uuid.uuid4().hex[:12]
env = os.environ.copy()
container = None
try:
    container = subprocess.check_output(["docker", "run", "--rm", "-d", "--name", nome,
        "-e", "POSTGRES_PASSWORD=senha-de-teste", "-p", "127.0.0.1::5432", "postgres:16-alpine"], text=True).strip()
    porta = subprocess.check_output(["docker", "port", container, "5432/tcp"], text=True).strip().rsplit(":", 1)[-1]
    dsn = f"host=127.0.0.1 port={porta} dbname=postgres user=postgres password=senha-de-teste connect_timeout=2"
    for tentativa in range(30):
        try:
            with psycopg.connect(dsn): pass
            break
        except psycopg.OperationalError:
            time.sleep(1)
    else: raise RuntimeError("PostgreSQL de teste indisponível")
    env["TEST_POSTGRES_DSN"] = dsn
    resultado = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "infra/tests", "-v"], cwd=raiz, env=env)
    if resultado.returncode: raise SystemExit(resultado.returncode)
finally:
    if container: subprocess.run(["docker", "stop", "-t", "0", container], check=False, stdout=subprocess.DEVNULL)
