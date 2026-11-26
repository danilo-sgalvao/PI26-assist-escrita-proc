#!/usr/bin/env bash
# Aplica as migrações e cria o usuário IAM da aplicação no PostgreSQL da stack de pré-requisitos.
# Executar no AWS CloudShell em ambiente VPC (VPC e sub-rede privada da stack, security group
# GrupoAdministracao), com NatLigado=sim. Uso: bash infra/scripts/preparar-banco.sh <pilha-de-pre-requisitos>
set -euo pipefail

PILHA="${1:?uso: preparar-banco.sh <pilha-de-pre-requisitos>}"
INFRA="$(cd "$(dirname "$0")/.." && pwd)"

saida() {
  aws cloudformation describe-stacks --stack-name "$PILHA" \
    --query "Stacks[0].Outputs[?OutputKey=='$1'].OutputValue" --output text
}

HOST="$(saida DatabaseHost)"
BANCO="$(saida DatabaseName)"
APP="$(saida DatabaseUser)"
SEGREDO="$(saida SegredoMestre)"

if ! command -v psql >/dev/null; then
  sudo dnf install -y -q postgresql17 || sudo dnf install -y -q postgresql16 || sudo dnf install -y -q postgresql15
fi

CREDENCIAIS="$(aws secretsmanager get-secret-value --secret-id "$SEGREDO" --query SecretString --output text)"
export PGUSER="$(printf '%s' "$CREDENCIAIS" | python3 -c 'import json,sys; print(json.load(sys.stdin)["username"])')"
export PGPASSWORD="$(printf '%s' "$CREDENCIAIS" | python3 -c 'import json,sys; print(json.load(sys.stdin)["password"])')"
export PGHOST="$HOST" PGDATABASE="$BANCO" PGSSLMODE=verify-full PGSSLROOTCERT="$INFRA/lambdas/rds-global-bundle.pem"

for migracao in "$INFRA"/migrations/*.sql; do
  echo "Aplicando $(basename "$migracao")"
  psql -v ON_ERROR_STOP=1 -q -f "$migracao"
done

echo "Configurando o usuário da aplicação $APP"
psql -v ON_ERROR_STOP=1 -q -v app="$APP" -f "$INFRA/scripts/usuario-aplicacao.sql"
psql -c '\dp'
