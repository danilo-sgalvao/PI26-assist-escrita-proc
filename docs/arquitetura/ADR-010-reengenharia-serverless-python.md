# ADR-010 — Reengenharia do backend: de monólito Java/Spring para AWS SAM com Lambdas em Python

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data | 26/11/2026 |
| Autor | Luiz Augusto Godinho, área C (redação com apoio de IA; ver "Uso de IA") |
| Revisores | Danilo Galvão, Felipe Nunes, Enzo Machado (pendente) |
| Estado | **Proposto**: aguarda a resposta do professor sobre a exigência de persistência em Java |
| Substitui | ADR-001, ADR-002, ADR-003 e ADR-005 do plano v1.2 (seção 6.8), quando aceito |
| Registro de mudança | [MUD-001 — Reengenharia para serverless (adaptativa)](../manutencao/MUD-001-reengenharia-serverless.md) |
| Tarefa | T66 (issue #72) |

Modelo do Apêndice A do plano mestre v1.2: contexto, alternativas consideradas, decisão, consequências, conformidade e notas.

## Contexto

**O que o plano previa.** O plano mestre v1.2 (seções 1.3 e 6) definia um cliente-servidor com SPA React e **monólito modular em Java 25 + Spring Boot 4**, com Spring Data JPA/Hibernate sobre PostgreSQL, migrações Flyway, sessão com cookie HttpOnly (Spring Security), Spring AI para o LLM e Docker Compose para a implantação (ADR-001 a ADR-005). A restrição **RT-01 (Fato)** dizia: "persistência e acesso a dados em Java", vinda do enunciado.

**O que foi feito.** Em 11/11/2026 entraram na `main`, sem PR, os commits que trocaram essa arquitetura por uma **serverless, assíncrona e orientada a eventos na AWS**, definida em AWS SAM (`infra/template.yaml`):

- Cognito com JWT (autorizador Cognito na API REST, autorizador Lambda no WebSocket);
- API Gateway REST e WebSocket, estágio `v1`;
- cinco Lambdas em **Python 3.12** (`ingestao`, `consulta`, `conexao_websocket`, `autorizador`, `processador_bedrock`), com `comum.py` concentrando a conexão ao PostgreSQL (`psycopg` 3, autenticação IAM, TLS `verify-full`);
- S3 versionado para o texto (`redacoes/<id>.txt`), RDS PostgreSQL para metadados (`revisoes`, `conexoes`), DynamoDB para as sugestões;
- S3 → SNS → SQS (com DLQ) → processador → Bedrock (API Converse);
- SPA em S3 privado entregue pelo CloudFront.

O commit `8c57bf3` (`refactor(apoio): substitui gateway Java por processador Lambda`) apagou o último código Java (gateway do Bedrock e seu teste, 260 linhas).

**Decisões já tomadas pela equipe, sem ADR:**

- **16/11/2026 (Danilo):** a arquitetura e o design já iniciados no repositório são os permanentes, mesmo onde diferem do plano v1.2.
- **19/11/2026 (Danilo):** persistência e acesso a dados em **Python**, nas Lambdas (`psycopg` e `boto3`), **sem Java**. Substitui a RT-01.
- **19/11/2026 (equipe):** decisões D1–D5 e fatias 1–5 de `docs/arquitetura/modelo-de-dados-e-api.md`, todas escritas sobre a arquitetura serverless em Python (por exemplo, D5: comparação de versões no servidor com `difflib`).

**Forças e riscos.**

- O `infra/README.md` avisa que o acesso ao PostgreSQL em Python "diverge da exigência Java dos documentos anteriores" e que "a equipe deve registrar a decisão". Este ADR é esse registro.
- A exigência de Java vem do enunciado. Se for critério da disciplina **Software para Persistência de Dados**, é o maior risco de reprovação do item (`docs/conformidade/02-software-para-persistencia-de-dados.md`, seção 5, T-P00).
- Para **Manutenção de Software**, a troca é a evidência mais forte de manutenção **adaptativa** e de reengenharia (`docs/conformidade/01-manutencao-de-software.md`, M02, M10, M16, T-M03), mas só conta se registrada.
- **Cronograma fixo (B12):** 6 semanas, 10 h por pessoa por semana, 5 h de reserva no total. Qualquer opção que reescreva código precisa caber aí.
- Requisitos ligados: RF16, RF21 e RF22 (turmas, termo e perfis, que dependem da camada de dados), RN04 (histórico imutável), RNF03 e RNF04 (acesso e privacidade), RNF16 (manutenibilidade, acrescentado pelo plano). A ERS v2 **não** fixa linguagem: a exigência de Java só aparece no enunciado e no plano.

## Alternativas consideradas

As três opções são as da seção 5 de `docs/conformidade/02-software-para-persistencia-de-dados.md`. Esforços *(sugeridos)*, estimados sobre o código atual (cinco Lambdas, uma migração, quatro arquivos de teste) e sobre as tarefas T73–T79 do backlog (`docs/gestao/backlog-pendente.md`, PR #69).

| # | Opção | Vantagens | Desvantagens e riscos | Custo *(sugerido)* | Risco |
|---|---|---|---|---|---|
| 1 | **Pedir ao professor que aceite Python** e manter toda a persistência nas Lambdas Python (`psycopg` 3, SQL explícito e parametrizado, `boto3`) | Nenhuma reescrita; mantém D1–D5 e as fatias; uma linguagem só no backend, um só pipeline de teste (T69) e um só *runtime* no SAM; SQL explícito facilita mostrar migração e refatoração de banco (T73, T74) | Depende da aceitação do professor; perde Flyway e JPA como evidência; se o professor recusar, o problema volta com menos prazo | ≈ 1 h (pergunta, ata e atualização deste ADR) | **Alto se recusado**, baixo se aceito |
| 2 | **Um agregado em Java**: uma ou mais Lambdas Java (Java 21 no SAM, JDBC com token IAM do RDS, Flyway) assumem **turmas e atividades**, que ainda não existem; o resto fica em Python | Cumpre a exigência de Java em código novo, sem reescrever o que funciona; dá um CRUD completo de entidade de negócio (competência C4, T-P08); Flyway pode ser a ferramenta de migração (T73) | Duas linguagens, dois *builds* e duas suítes no CI; regra de autorização (`cognito:groups`, `404`, `TERMO_PENDENTE`) duplicada em Java e Python; *cold start* maior (mitigável com SnapStart); a área C passa de 6,5 h/semana; o código Java do PR #1 é Spring e não serve direto numa Lambda | ≈ 10–14 h a mais que T78 e T79 em Python, mais ≈ 2 h no CI | Médio: estoura a reserva de 5 h; precisa cortar *Should* ou *Could* |
| 3 | **Migrar toda a camada de dados para Java**: reescrever `ingestao`, `consulta`, `conexao_websocket` e o acesso a dados do processador, com testes, ou voltar ao monólito Spring | Cumpre a exigência sem discussão; alinha com o plano v1.2 | Reescreve código que funciona e foi testado; invalida a D5 (`difflib`) e parte de D1–D4; perde semanas sem entregar requisito novo; repete a reengenharia no sentido contrário | ≈ 30–40 h | **Alto**: não cabe nas 5 h de reserva e ameaça os *Must* |

## Decisão

**Proposta: opção 1**, com a **opção 2 como plano B** caso o professor mantenha a exigência de Java. A opção 3 fica descartada.

Por quê:

- a reengenharia já aconteceu (11/11/2026) e foi confirmada pela equipe em 16/11 e 19/11/2026; o design de 19/11 (D1–D5, fatias 1–5) foi todo escrito sobre ela;
- a ERS v2 não exige Java; a exigência está no enunciado e na RT-01 do plano, e só o professor pode dizer se ela é critério de avaliação;
- com o cronograma fixo (B12) e 5 h de reserva, só a opção 1 não exige cortar escopo; a opção 2 é viável se cortarmos itens *Should*/*Could* pela ordem de corte do `CLAUDE.md`; a opção 3 não é viável;
- turmas e atividades ainda não existem no código, então, se a opção 2 for necessária, ela cai sobre código novo e não sobre o que funciona.

O estado fica **Proposto** até a resposta do professor. Com a resposta:

- **"Python é aceito"** → estado **Aceito**; a RT-01 passa a ser "persistência em Python nas Lambdas", registrada no plano v1.3 (T70);
- **"Java é obrigatório, mas basta parte"** → este ADR é **substituído** por um ADR-012 que registra a opção 2, com o agregado escolhido;
- **"Java é obrigatório em toda a persistência"** → a equipe se reúne para replanejar; a opção 3 só volta a ser considerada com mudança de escopo aprovada pelo professor (seção 12.3 do plano).

### Pergunta ao professor (texto pronto para o grupo enviar)

> Professor, boa tarde. Somos o Grupo 8 (Assistente de Escrita Processual, POC 2.2).
>
> O enunciado pede persistência e acesso a dados em Java. No começo do projeto planejamos um backend Java com Spring Boot, mas, durante o desenvolvimento, migramos para uma arquitetura serverless na AWS: Lambdas em Python que acessam o PostgreSQL (RDS) com SQL explícito e parametrizado (biblioteca `psycopg`), com o texto das redações versionado no S3 e as orientações da IA no DynamoDB. A troca e os motivos estão registrados em um ADR no repositório.
>
> Gostaríamos de saber qual destes caminhos o senhor aceita:
>
> 1. manter toda a persistência em Python, como está hoje;
> 2. manter o que existe em Python e implementar em Java uma parte nova do sistema, com acesso ao banco (o cadastro de turmas e atividades, por exemplo);
> 3. reescrever toda a camada de dados em Java.
>
> Pelo nosso cronograma, a opção 1 não exige reescrita, a 2 cabe se cortarmos itens de menor prioridade e a 3 compromete a entrega dos requisitos principais. Se a exigência de Java vier de uma disciplina específica, poderia nos dizer qual, para ajustarmos o que entregamos para ela?
>
> Obrigado.

A resposta, com data e meio (e-mail, aula, mensagem), entra na seção "Notas" e na MUD-001.

## Consequências

### Positivas

- Fica registrada a mudança mais relevante do projeto, como pede o `infra/README.md`, e ela passa a contar como manutenção adaptativa (MUD-001; [CF-MS] M02, M16).
- O backlog T66–T124 pode seguir na arquitetura implementada sem ambiguidade sobre a linguagem.
- Uma linguagem no backend: menos ferramentas no CI (T69), um *runtime* no SAM, uma suíte de testes (`unittest`).

### Negativas e *trade-offs* aceitos

- Escalabilidade e implantação gerenciadas pela AWS, ao custo de dependência do provedor, deploy cobrado e teste integrado só na conta (os testes locais usam dublês).
- Sem transação entre S3 e PostgreSQL: pode sobrar registro em `PROCESSANDO`; a DLQ precisa de monitoramento; a notificação por WebSocket pode se repetir ou se perder (`infra/README.md`).
- Perdem-se ferramentas do plano: JPA, Flyway, ArchUnit, Spring Security e Spring AI. A ferramenta de migração passa a ser yoyo, Alembic ou sqitch (T73), e a separação entre regra e acesso a dados passa a depender da camada de repositórios (T76).
- Persiste o risco de o professor recusar a opção 1 depois que parte do backlog já foi feita em Python. Por isso a pergunta deve sair antes de T78 e T79 começarem.

### Impacto nos documentos

| Documento | Impacto | Como tratar |
|---|---|---|
| **ERS v2** | Nenhum requisito muda: a ERS não fixa linguagem. O RNF04 (dados enviados ao provedor) continua atendido pelo Bedrock e pela decisão D1 | Nada a editar. Se a resposta do professor mudar escopo, vira MUD de requisito (seção 12.3 do plano) |
| **Plano v1.2** | RT-01; seção 6 inteira (estilo, C4, stack, ADR-001 a 005 e ADR-007 "em Java"); seção 10 (Docker Compose, deploy); seção 13 (critério "três contêineres sobem com um comando", `/api/health` no Compose); riscos R06 e R09 (Spring) | O plano v1.2 **não é editado**. A v1.3 (T70) incorpora este ADR, registrada como MUD perfectiva |
| **`CLAUDE.md`** | Já descreve a arquitetura vigente e aponta a falta deste ADR | Atualizar quando o ADR for aceito (fora desta tarefa) |
| **Backlog** | T73 (Flyway só se houver Java), T76–T79, T67 (PRs #1–#3 do Spring) | Ver tabela abaixo |

### Impacto em T76–T79 se a opção 2 for escolhida

| Tarefa | Com a opção 1 (Python) | Com a opção 2 (turmas e atividades em Java) |
|---|---|---|
| **T76** Camada de repositórios | Repositórios Python para revisões, conexões, sugestões e as tabelas novas | Repositórios divididos: Python para produção, versões e interações; Java (JDBC ou Spring Data JDBC) para `turmas`, `matriculas` e `atividades`. O esquema continua único e as migrações ficam em uma só ferramenta (Flyway, por T73) |
| **T77** Perfis e autorização | Leitura de `cognito:groups` e regras de `404`/`TERMO_PENDENTE` num módulo Python | A mesma regra também em Java, com testes de acesso cruzado nas duas linguagens; risco de divergência entre elas |
| **T78** Identidade e turmas | `GET /eu`, `/eu/termo`, `/turmas` em Python | `/turmas` e `/turmas/{id}/estudantes` em Lambda Java; `GET /eu` e `/eu/termo` podem ficar em Python (dependem só do usuário), ou ir juntos para Java, para que o agregado fique inteiro |
| **T79** Atividades | `/atividades` em Python | `/atividades` em Lambda Java; a validação do gênero em lista fechada e do prazo passa a ser feita em Java |

Na opção 2 também mudam: T69 (CI com JDK e Maven/Gradle), T73 (Flyway), T67 (aproveitar ou não o código do PR #1, que é Spring e não roda como Lambda sem adaptação) e a estimativa da área C, que passa do limite de 6,5 h por semana.

## Conformidade

- **Revisão:** o PR deste ADR é revisado por duas áreas além do autor (seção 12.3 do plano, mudança de arquitetura).
- **Resposta do professor:** registrada em "Notas", com data e meio; o estado muda para Aceito ou Substituído no mesmo dia.
- **Código:** enquanto valer a opção 1, nenhuma Lambda de dados em outra linguagem entra sem novo ADR. Se valer a opção 2, o CI (T69) roda as duas suítes, e um teste de contrato garante que Java e Python aplicam a mesma regra de autorização (T77).
- **Rastreabilidade:** MUD-001 aponta para este ADR; o plano v1.3 (T70) e a documentação final (T123) citam os dois.

## Notas

- **Aprovado por:** pendente.
- **Resposta do professor:** pendente (pergunta ainda não enviada em 26/11/2026).
- **Substituições:** quando aceito, substitui ADR-001 (monólito modular), ADR-002 (portas e adaptadores dentro do monólito), ADR-003 (persistência Java/JPA/Flyway) e ADR-005 (sessão com cookie) do plano v1.2. Os ADR-004 (imutabilidade) e ADR-009 (versões) continuam válidos como princípio; o mecanismo deles passa a ser o versionamento do S3 e as migrações de T74.
- **Numeração:** ADR-006 (Bedrock) está no PR #2; ADR-007 a 009 são do plano; ADR-011 (persistência poliglota) é previsto em T75.

## Uso de IA

Redigido com apoio do Claude Code (Anthropic, modelo Claude Opus 5.5) em 26/11/2026, a partir do `CLAUDE.md`, do `infra/README.md`, de `docs/arquitetura/modelo-de-dados-e-api.md`, do plano v1.2, dos documentos de conformidade (PR #68) e do backlog (PR #69). As estimativas de esforço são sugestões e devem ser revisadas pela equipe. A decisão é da equipe e do professor.
