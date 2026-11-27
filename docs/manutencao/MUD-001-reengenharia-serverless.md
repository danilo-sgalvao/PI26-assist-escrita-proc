# MUD-001 — Reengenharia do backend para serverless (AWS SAM + Lambdas em Python)

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data do registro | 26/11/2026 |
| Autor | Luiz Augusto Godinho, área C (redação com apoio de IA) |
| Revisores | Danilo Galvão, Felipe Nunes, Enzo Machado (pendente) |
| Estado | **Proposta**: implementada em 11/11/2026, aguarda a resposta do professor sobre a exigência de Java |
| Decisão arquitetural | [ADR-010](../arquitetura/ADR-010-reengenharia-serverless-python.md) |
| Tarefa e issue | T66 (issue #72) |

Registro de mudança no sentido da ISO/IEC/IEEE 14764:2022 e do SWEBOK v4 (7.1.6 e 8.3.1.3). É o primeiro registro MUD do projeto e serve de exemplo para os próximos.

## Campos

| Campo | Conteúdo |
|---|---|
| **Descrição** | Troca do backend planejado no plano mestre v1.2 (monólito modular Java 25 + Spring Boot 4, JPA/Hibernate, Flyway, sessão com Spring Security, Spring AI, Docker Compose) por uma arquitetura serverless e orientada a eventos na AWS, definida em AWS SAM: Cognito, API Gateway REST e WebSocket, cinco Lambdas em Python 3.12, S3 versionado, RDS PostgreSQL, DynamoDB, SNS, SQS com DLQ e Bedrock (API Converse). Todo o acesso a dados passa a ser em Python (`psycopg` 3 e `boto3`) |
| **Motivo** | Adaptar o sistema a um novo ambiente de execução e implantação (nuvem AWS, serviços gerenciados), escolhido pela equipe durante o desenvolvimento. A arquitetura e o design iniciados no repositório foram confirmados como permanentes por Danilo em 16/11/2026, e a persistência em Python, sem Java, em 19/11/2026 |
| **Categoria** | **Adaptativa** (ISO/IEC/IEEE 14764): modifica o software para mantê-lo utilizável num ambiente diferente (plataforma, *runtime*, serviços de nuvem), sem mudar o que ele faz para o usuário. Por mudar a estrutura inteira do backend, é também uma **reengenharia** |
| **RF/RN afetados** | Nenhum RF ou RN muda de texto. Muda **como** são atendidos: RF01–RF05 e RF10 (envio e consulta de produção pela API assíncrona), RF16, RF21 e RF22 (perfis e termo, agora com Cognito), RN01/RN02 (defesa pela saída fechada do Bedrock, decisão D1), RN04 (imutabilidade pelo versionamento do S3, não mais por *trigger* no banco), RNF03/RNF04 (autorização por JWT; dados enviados ao Bedrock). Restrição afetada: **RT-01** do plano ("persistência em Java"), que deixa de ser cumprida |
| **Impacto — código** | Backend Java removido da `main` (último arquivo apagado no commit `8c57bf3`, 260 linhas). Criados `infra/template.yaml` e `infra/lambdas/` (`ingestao`, `consulta`, `conexao_websocket`, `autorizador`, `processador_bedrock`, `comum.py`). Frontend passou a usar Cognito e WebSocket. PRs #1–#3 (Spring e base RAG) ficaram superados, a decidir em T67 |
| **Impacto — dados** | Modelo relacional completo do plano (seção 6.4) trocado por persistência poliglota: `revisoes` e `conexoes` no PostgreSQL (`infra/migrations/001_inicial.sql`, aplicada à mão), texto no S3 versionado, sugestões no DynamoDB. Sem transação entre S3 e PostgreSQL. Turmas, atividades e versões entram na migração `002` (T74). A documentação desse modelo fica para T75 |
| **Impacto — docs** | `infra/README.md`, `frontend/README.md`, diagrama `docs/arquitetura-aluno-processamento.png`, `CLAUDE.md` e `docs/arquitetura/modelo-de-dados-e-api.md` já descrevem a arquitetura nova. A ERS v2 não muda (não fixa linguagem). O plano v1.2 fica superado em arquitetura, stack, seção 10 e parte da seção 13; não é editado, e o plano v1.3 (T70) incorpora a mudança |
| **Impacto — testes** | Testes JUnit e Testcontainers do plano dão lugar a `unittest` com dublês dos serviços AWS (`infra/tests/`) e Vitest no frontend. Os testes locais não substituem o teste integrado na conta AWS. Testes de arquitetura (ArchUnit) deixam de existir; a separação entre regra e dados passa a ser verificada pela camada de repositórios (T76) |
| **Esforço** | **Já gasto:** os commits de 11/11/2026 (sem registro de horas). **A gastar**, conforme a resposta do professor (ADR-010): opção 1 ≈ 1 h; opção 2 ≈ 12–16 h a mais; opção 3 ≈ 30–40 h *(estimativas sugeridas)* |
| **Decisão** | Implementada de fato em 11/11/2026 e confirmada pela equipe em 16/11 e 19/11/2026. Formalização **pendente**: o ADR-010 propõe manter Python (opção 1), com um agregado em Java (opção 2) como plano B, e aguarda a resposta do professor |
| **Responsável** | Execução: Felipe Nunes (commits de 11/11/2026). Decisão: Danilo Galvão (16/11 e 19/11/2026). Registro: Luiz Augusto Godinho (T66) |
| **Data** | Implementação: 11/11/2026. Decisão da equipe: 16/11 e 19/11/2026. Registro: 26/11/2026. Resposta do professor: pendente |

## Lições para os próximos registros

- A mudança entrou direto na `main`, sem PR, sem issue e sem ADR. O registro só veio 15 dias depois. A partir de T68, toda mudança deve abrir uma issue do tipo "mudança" antes do código.
- A mudança contrariou um "fato confirmado" (RT-01) sem consulta ao professor. Mudanças que tocam fatos confirmados precisam da aprovação dele antes de começar (seção 12.3 do plano).

## Uso de IA

Redigido com apoio do Claude Code (Anthropic, modelo Claude Opus 5.5) em 26/11/2026, a partir do histórico do Git, do `CLAUDE.md`, do `infra/README.md` e dos documentos de conformidade. A classificação e as estimativas devem ser revisadas pela equipe.
