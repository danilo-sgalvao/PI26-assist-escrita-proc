CREATE TABLE IF NOT EXISTS revisoes (
    id uuid PRIMARY KEY,
    aluno_sub text NOT NULL,
    chave_s3 text NOT NULL UNIQUE,
    status text NOT NULL CHECK (status IN ('PROCESSANDO', 'CONCLUIDO')),
    criada_em timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS conexoes (
    connection_id text PRIMARY KEY,
    aluno_sub text NOT NULL,
    criada_em timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS conexoes_por_aluno ON conexoes (aluno_sub);
