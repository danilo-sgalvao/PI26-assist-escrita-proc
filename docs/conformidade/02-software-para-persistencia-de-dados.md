# Conformidade do PI26 com Software para Persistência de Dados

Versão: 1.0 · Data: 25/11/2026 · Autor: Luiz Augusto Godinho (com apoio de IA) · Revisor: pendente · Estado: rascunho para a equipe

Projeto avaliado: **Assistente de Escrita Processual — Grupo 8** (POC 2.2), snapshot `PI26-assist-escrita-proc-main`.

## 1. Para que serve este documento

Diz o que a disciplina **Software para Persistência de Dados** (6º período, 64 h, 32 teóricas + 32 práticas, pré-requisito: Banco de Dados) espera ver no projeto interdisciplinar, onde o projeto já atende e o que falta fazer. Cada item cruza:

- **Ementa e competências mínimas** do PPC 2024 do BES;
- **SWEBOK v4**: 16.6 Database Management (foco principal), 3.3.3 Data Persistence (design), 2 Arquitetura e 7 Manutenção (migração e evolução de esquema), mais 6.3.3 Rollback and Data Migration;
- Bibliografia básica da disciplina: Ambler (*Agile Database Techniques*), McMurtry et al. (*Data Access for Highly-Scalable Solutions: SQL, NoSQL and Polyglot Persistence*) e Redmond & Wilson (*Seven Databases in Seven Weeks*).

Legenda de situação: ✅ atende · 🟡 parcial · ❌ não atende · ➖ não se aplica nesta entrega.

## 2. O que a disciplina pede

### 2.1 Ementa (resumo por bloco)

| Bloco | CH | Conteúdo | SWEBOK |
|---|---|---|---|
| Conceitos | 4 h | Dados, metadados e modelos de dados; transferência e armazenamento; sistemas de arquivos, bancos de dados e data warehouse | 16.6.1, 16.6.2, 16.6.6 |
| Tecnologias | 8 h | Arquivos texto e binário; serialização de objetos; JSON; XML; SQL e NoSQL; frameworks ETL | 16.6.2–16.6.5 |
| Arquitetura | 8 h | Padrões e estilos arquiteturais de persistência; arquitetura do componente de persistência | 3.3.3, 2 |
| Integração baseada em dados | 8 h | Integração por troca de arquivos; integração por dados compartilhados | 2, 16.6 |
| Evolução de bancos de dados | 8 h | Manutenção evolutiva, adaptativa e corretiva de esquema; extração, modificação e migração de dados; refatoração de bancos | 7, 6.3.3 |
| Prática | 28 h | Modelagem e implementação de aplicação com persistência em **sistema de arquivos** e em **banco de dados** | 16.6 |

### 2.2 Competências mínimas (todas "faz com orientação")

- **C1** Explicar a construção de software, a persistência e a relação delas com a engenharia de software e de sistemas.
- **C2** Identificar e usar a estratégia de persistência adequada para um problema.
- **C3** Usar ferramentas para definição e manipulação de bancos de dados.
- **C4** Criar código que cria, busca, atualiza e remove dados (CRUD).
- **C5** Refatorar bases de dados.

## 3. Como o projeto persiste dados hoje

O projeto já é um caso de **persistência poliglota**, que é tema central da bibliografia (McMurtry; Redmond & Wilson):

| Armazenamento | O que guarda | Onde está definido | Acesso |
|---|---|---|---|
| **PostgreSQL** (externo, RDS) | `revisoes` (id, dono, chave S3, status) e `conexoes` (WebSocket ativas) | `infra/migrations/001_inicial.sql` | `psycopg` 3 em Python, SQL parametrizado, autenticação IAM e TLS `verify-full` (`infra/lambdas/comum.py`) |
| **Amazon S3** (sistema de arquivos/objetos) | Texto da redação como `.txt` UTF-8, **com versionamento ativo**, criptografia SSE e acesso público bloqueado | `BucketRedacoes` em `infra/template.yaml` | `boto3` `put_object` / `get_object` com `VersionId` |
| **DynamoDB** (NoSQL chave-valor) | Sugestões geradas por produção (`id_producao`, `versao_s3`, `sugestoes`) | Tabela `Sugestoes` no template, com PITR e SSE | `put_item` com `ConditionExpression` (idempotência) e leitura consistente |
| **sessionStorage** do navegador | IDs e horários das revisões do usuário (sem texto nem token) | `frontend/src` | API Web Storage, JSON |

O plano mestre v1.2 (seção 6.4) previa outra coisa: modelo lógico relacional completo (USUARIO, TURMA, MATRICULA, ATIVIDADE, PRODUCAO, VERSAO, TRANSICAO_ETAPA, EVENTO_COLAGEM, INTERACAO_APOIO, DEVOLUTIVA, ANALISE/RESULTADO_SIMILARIDADE), Spring Data JPA/Hibernate, Flyway e trigger que impede UPDATE/DELETE nas versões (ADR-004).

## 4. Matriz de conformidade

### 4.1 Conceitos, modelos e tecnologias

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| P01 | Modelo de dados conceitual e lógico documentado | Modelo ER completo no plano v1.2 (6.4, Figura 8), mas não corresponde ao que foi implementado. O modelo implementado (2 tabelas + S3 + DynamoDB) não está documentado como modelo | 🟡 |
| P02 | Metadados e dicionário de dados (tipos, restrições, significado de cada campo) | `CHECK (status IN ('PROCESSANDO','CONCLUIDO'))`, `UNIQUE` em `chave_s3`, PK UUID. Não há dicionário de dados | 🟡 |
| P03 | Uso de **SQL e NoSQL** com justificativa | Usa os dois (PostgreSQL + DynamoDB), além de armazenamento de objetos. A justificativa da escolha não está escrita | 🟡 |
| P04 | Persistência em **arquivo** (exigida na prática) | S3 guarda a redação como arquivo texto versionado | ✅ |
| P05 | Formatos de serialização (JSON, texto, binário, XML) | JSON nas APIs, nas mensagens SNS/SQS e no `sessionStorage`; texto UTF-8 no S3. XML não aparece | ✅ (XML ➖) |
| P06 | ETL ou data warehouse | Não há. As métricas da POC (autonomia progressiva, qualidade, originalidade) seriam um bom caso de extração para análise | ➖ / oportunidade |

### 4.2 Arquitetura do componente de persistência

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| P07 | Camada de persistência isolada (padrões Repository, DAO, Data Mapper ou portas e adaptadores) | SQL escrito direto nos *handlers* das Lambdas; `comum.banco()` só abre a conexão. Não há repositório nem separação entre regra e acesso a dados | ❌ |
| P08 | Padrão arquitetural de persistência identificado e justificado | Na prática o projeto usa **polyglot persistence** e **claim-check** (o texto vai ao S3 e só a referência circula na fila). Isso não está nomeado nem justificado | 🟡 |
| P09 | Gerência de transações e consistência | Escrita no PostgreSQL e no S3 sem transação distribuída. O `infra/README.md` reconhece que pode sobrar registro `PROCESSANDO` órfão e que falta reconciliação. Gravação no DynamoDB é condicional e idempotente | 🟡 |
| P10 | Imutabilidade do histórico de versões (RN04 do projeto; ADR-004) | Versionamento do S3 preserva todas as versões do objeto, mas cada submissão gera uma chave nova e não há tabela de versões nem bloqueio de UPDATE/DELETE no banco | 🟡 |
| P11 | Segurança no acesso a dados (SWEBOK 13; Banco de Dados Avançado: SQL injection) | Consultas parametrizadas (`%s`), token IAM no lugar de senha, TLS `verify-full`, filtro por dono (`aluno_sub`) em toda leitura, S3 privado e criptografado | ✅ |
| P12 | Backup e recuperação (SWEBOK 16.6.7) | DynamoDB com PITR; S3 versionado; `DeletionPolicy: Retain`. **Backup do PostgreSQL não é tratado** (o README avisa) | 🟡 |

### 4.3 Integração baseada em dados

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| P13 | Integração por **troca de arquivos** | Gravação no S3 dispara evento `ObjectCreated` → SNS → SQS → processador, que lê a versão exata do arquivo | ✅ |
| P14 | Integração por **dados compartilhados** | Ingestão, consulta e processador compartilham as tabelas `revisoes` e `conexoes` e a tabela DynamoDB | ✅ |
| P15 | Documento explicando os dois estilos e seus riscos (acoplamento ao esquema, ordem de eventos, duplicidade) | Parte disso está no `infra/README.md` (reentregas idempotentes, notificação duplicada) | 🟡 |

### 4.4 Evolução e refatoração de banco de dados

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| P16 | Esquema sob controle de versão com migrações numeradas | Existe `001_inicial.sql`, mas sem ferramenta de migração (Flyway, Alembic, yoyo, sqitch) e sem tabela de histórico. Execução manual | 🟡 |
| P17 | Pelo menos uma **migração evolutiva** além da inicial (nova tabela ou coluna) | Não há `002_...` | ❌ |
| P18 | Pelo menos uma **refatoração de banco** do catálogo de Ambler & Sadalage (ex.: *Introduce Column Constraint*, *Split Table*, *Rename Column* com período de transição) | Nenhuma | ❌ |
| P19 | Migração de **dados** (extrair, transformar, carregar dados existentes para o novo esquema) | Nenhuma | ❌ |
| P20 | Migração reversível ou plano de rollback de esquema (SWEBOK 6.3.3) | Não há *down migration* nem procedimento de restauração do PostgreSQL. O plano v1.2 previa `pg_dump` antes de cada atualização | ❌ |

### 4.5 Competências mínimas

| Competência | Situação | Evidência ou o que falta |
|---|---|---|
| C1 Explicar persistência e sua relação com ES | 🟡 | Falta um documento de arquitetura de dados explicando as escolhas (T-P01) |
| C2 Escolher a estratégia adequada | 🟡 | A escolha poliglota existe e é boa, mas não está justificada (T-P02) |
| C3 Ferramentas de definição e manipulação | 🟡 | DDL em SQL e IaC (CloudFormation/SAM) para S3 e DynamoDB. Falta ferramenta de migração (T-P05) |
| C4 CRUD | 🟡 | Há **C** (INSERT, `put_object`, `put_item`), **R** (SELECT, `get_object`, `get_item`), **U** (UPDATE de status) e **D** (DELETE de conexões). Mas não há CRUD de entidade de negócio completa (ex.: turmas e atividades; o README diz que não há CRUD de turmas) |
| C5 Refatorar bases de dados | ❌ | Nenhuma refatoração feita (T-P06) |

## 5. Ponto que precisa ser resolvido com o professor

A equipe registrou como fato confirmado: **"Persistência e acesso a dados em Java (exigência do enunciado)"**. O código atual faz todo o acesso a dados em **Python** dentro das Lambdas, e o `infra/README.md` registra que essa divergência "foi autorizada pelo usuário" e que "a equipe deve registrar a decisão".

Se a exigência de Java vem desta disciplina, este é o maior risco de reprovação do item. Há três caminhos:

1. **Pedir ao professor que aceite Python**, registrando a decisão em ADR (com justificativa: arquitetura serverless, `psycopg` 3, SQL explícito).
2. **Criar um serviço Java de persistência** (ex.: Lambda Java com JDBC/JPA, ou um módulo Spring Boot) que assuma pelo menos um agregado (ex.: turmas e atividades, que ainda não existem), mantendo o resto em Python.
3. **Migrar a camada de dados para Java**, opção mais cara e arriscada para o prazo.

Recomendo levar 1 e 2 ao professor. A opção 2 também resolve a lacuna de CRUD completo (C4).

## 6. TODO

Prioridade: **P1** necessário para a avaliação · **P2** recomendado · **P3** se sobrar tempo.

- [ ] **T-P00 (P1)** Confirmar com o professor a exigência de Java e registrar a decisão em ADR (ver seção 5).
- [ ] **T-P01 (P1)** Escrever `docs/dados/arquitetura-de-dados.md`: diagrama do que é guardado onde (PostgreSQL, S3, DynamoDB, sessionStorage), fluxo dos dados e relação com o modelo do plano v1.2.
- [ ] **T-P02 (P1)** ADR de **persistência poliglota**: por que relacional para posse e status, objetos versionados para o texto, chave-valor para sugestões. Citar o padrão claim-check e os trade-offs de consistência.
- [ ] **T-P03 (P1)** Modelo ER **do que está implementado** + dicionário de dados (tabela, coluna, tipo, restrição, significado, dado pessoal sim/não).
- [ ] **T-P04 (P1)** Extrair o acesso a dados para uma camada de repositórios (ex.: `repositorio_revisoes.py`, `repositorio_conexoes.py`, `repositorio_sugestoes.py`) e cobrir com testes. Resolve P07.
- [ ] **T-P05 (P1)** Adotar ferramenta de migração (Flyway se houver componente Java; senão Alembic, yoyo ou sqitch), com tabela de histórico e execução no pipeline de deploy.
- [ ] **T-P06 (P1)** Fazer e documentar **uma migração evolutiva com migração de dados**. Sugestão aderente à ERS: criar tabela `versoes` (id, producao_id, numero, chave_s3, versao_s3, etapa, criada_em) e popular a partir de `revisoes` existentes. Incluir **refatoração** do catálogo de Ambler (ex.: *Introduce Column Constraint* ou *Move Column*).
- [ ] **T-P07 (P1)** Implementar **imutabilidade** no banco (ADR-004/RN04): trigger ou `REVOKE UPDATE, DELETE` na tabela de versões, com teste que prova a rejeição.
- [ ] **T-P08 (P2)** CRUD completo de uma entidade de negócio (turmas ou atividades). É a chance de cumprir a exigência de Java (opção 2 da seção 5).
- [ ] **T-P09 (P2)** Rotina de **reconciliação** de revisões `PROCESSANDO` sem objeto no S3 ou sem resultado (consistência eventual).
- [ ] **T-P10 (P2)** Backup e restauração do PostgreSQL: snapshots automáticos do RDS ou `pg_dump` antes de cada migração, com **teste de restauração** documentado (SWEBOK 16.6.7 e 6.3.3).
- [ ] **T-P11 (P3)** Pequeno processo ETL que extrai métricas da POC (número de versões por produção, intervalo entre submissões, uso do assistente) para um esquema analítico ou CSV. Cobre o tópico de ETL e data warehouse.
- [ ] **T-P12 (P3)** Política de retenção e exclusão de dados pessoais (LGPD, RNF01): o que apagar, onde (todas as versões no S3, DynamoDB, PostgreSQL) e como.

## 7. Entregáveis sugeridos para a avaliação

| Entregável | Cobre |
|---|---|
| Arquitetura de dados + ADR de persistência poliglota | C1, C2, P03, P08 |
| Modelo ER implementado + dicionário de dados | P01, P02 |
| Camada de repositórios com testes | C4, P07 |
| Migrações versionadas (`001`, `002`, ...) com migração de dados e refatoração | C3, C5, P16–P19 |
| Trigger/permissão de imutabilidade com teste | P10 |
| Procedimento de backup e restauração testado | P12, P20 |

## 8. Uso de IA

Documento redigido com apoio de IA a partir da ementa do PPC 2024, do SWEBOK v4 e do snapshot do repositório. A equipe deve revisar as avaliações de situação antes de usar este material.
