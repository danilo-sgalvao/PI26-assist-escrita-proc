-- Usuário da aplicação autenticado por IAM (rds_iam). Específico do RDS: não é migração.
-- Rodar depois das migrações, com o usuário de migração. Uso: psql -v app=<usuario> -f usuario-aplicacao.sql
SELECT format('CREATE ROLE %I LOGIN', :'app')
WHERE NOT EXISTS (SELECT FROM pg_roles WHERE rolname = :'app') \gexec

SELECT format('GRANT rds_iam TO %I', :'app') \gexec
SELECT format('GRANT USAGE ON SCHEMA public TO %I', :'app') \gexec

-- RN04: o histórico nunca é apagado. DELETE só em conexoes (WebSocket encerrado).
SELECT format('GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO %I', :'app') \gexec
SELECT format('ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE ON TABLES TO %I', :'app') \gexec
SELECT format('GRANT DELETE ON conexoes TO %I', :'app') \gexec
