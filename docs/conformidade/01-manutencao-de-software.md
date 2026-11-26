# Conformidade do PI26 com Manutenção de Software

Versão: 1.0 · Data: 25/11/2026 · Autor: Luiz Augusto Godinho (com apoio de IA) · Revisor: pendente · Estado: rascunho para a equipe

Projeto avaliado: **Assistente de Escrita Processual — Grupo 8** (POC 2.2), snapshot `PI26-assist-escrita-proc-main`.

## 1. Para que serve este documento

Diz o que a disciplina **Manutenção de Software** (6º período, 64 h, 32 teóricas + 32 práticas) espera ver no projeto interdisciplinar, onde o projeto já atende e o que falta fazer. Cada item cruza três fontes:

- **Ementa e competências mínimas** do PPC 2024 do BES;
- **SWEBOK v4, capítulo 7 (Software Maintenance)**, que a própria ementa cita como bibliografia básica, mais os secundários 8 (Gerência de Configuração), 5 (Teste) e 13 (Segurança);
- **ISO/IEC/IEEE 14764:2022**, a outra bibliografia básica.

Legenda de situação: ✅ atende · 🟡 parcial · ❌ não atende · ➖ não se aplica nesta entrega.

## 2. O que a disciplina pede

### 2.1 Ementa (resumo por bloco)

| Bloco | CH | Conteúdo | SWEBOK |
|---|---|---|---|
| Conceitos | 4 h | Manutenção como parte da sustentação; categorias (correção, prevenção, adaptação, adição, aperfeiçoamento); leis de Lehman | 7.1.1–7.1.6 |
| Manutenibilidade | 8 h | Modularidade, reuso, testabilidade, analisabilidade, modificabilidade; indicadores (manutenibilidade, densidade de falhas e defeitos) | 7.2.1.4, 7.2.4 |
| Processos e atividades | 12 h | Ciclo com CI/CD (DevOps) e com entrega discreta; fluxo por tipo de manutenção; interface com GCS e Garantia da Qualidade; manutenção corretiva (relato, confirmação, classificação e tratamento de anomalias) | 7.3, 7.4.4 |
| Gestão de mudanças | 8 h | Solicitação; análise de impacto e viabilidade; deliberação e planejamento; implementação; monitoramento e validação; regressão; implantação | 7.2.1.3, 8.3 |
| Técnicas | 12 h | Rastreabilidade bidirecional; compreensão de programas; estimativa de custo e prazo; reengenharia; engenharia reversa; depuração; refatoração; descarte; ameaças à segurança na manutenção | 7.2.3, 7.4.1–7.4.3, 7.5 |
| Prática | 20 h | Seleção e uso de ferramentas e técnicas para cada tipo de manutenção | 7.5 |

### 2.2 Competências mínimas (todas "faz com orientação")

- **C1** Planejar a sustentação de um software.
- **C2** Planejar, monitorar e executar a transição do software para produção.
- **C3** Planejar um sistema de suporte técnico e de registro de pedidos de mudança.
- **C4** Realizar manutenção corretiva, adaptativa, preventiva e aditiva.

## 3. Matriz de conformidade

### 3.1 Conceitos e categorias de manutenção

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| M01 | Cada mudança classificada numa das categorias da ISO 14764 / SWEBOK 7.1.6 (corretiva, preventiva, adaptativa, aditiva, perfectiva, emergencial) | O plano prevê MUD-nnn e DEF-nnn (plano v1.2, seções 9.6 e 12), mas não há nenhum registro criado e o modelo de MUD não tem campo de categoria | ❌ |
| M02 | Pelo menos um exemplo real de **cada** categoria exigida pela C4 (corretiva, adaptativa, preventiva, aditiva) executado e documentado | Há mudanças que já se encaixam, mas sem registro: troca de "LLM local" por API externa (B1, **adaptativa**); troca de Java/Spring por Lambdas Python + AWS SAM (**adaptativa**, sem ADR); ERS v1 → v2 (**aditiva** no nível de requisitos) | 🟡 |
| M03 | Discussão das leis de Lehman aplicada ao projeto (crescimento contínuo, complexidade crescente) | Nada | ❌ |

### 3.2 Manutenibilidade e métricas

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| M04 | Código modular e com baixo acoplamento | Lambdas pequenas e separadas por responsabilidade (`ingestao`, `consulta`, `processador_bedrock`, `autorizador`, `conexao_websocket`, código comum em `comum.py`); frontend com `api/` separado de `pages/` | ✅ |
| M05 | Testabilidade demonstrada | 9 testes unitários Python com dublês (`infra/tests/test_lambdas.py` e `test_cors.py`), teste integrado opcional com PostgreSQL descartável (`test_fluxo_integrado.py`), 7 testes Vitest no frontend | ✅ |
| M06 | Indicadores de manutenção medidos e acompanhados (SWEBOK 7.2.4): densidade de defeitos, tempo médio de correção, cobertura, complexidade, dívida técnica | Nenhuma medição. Não há cobertura configurada nem análise estática no backend Python | ❌ |
| M07 | Dívida técnica identificada e priorizada (SWEBOK 7.2.1.4 e 7.2.3.1) | O `infra/README.md` lista limitações (sem reconciliação de registros `PROCESSANDO`, DLQ sem monitoramento, migração manual, sem CRUD de turmas), mas não como backlog de dívida com custo e prioridade | 🟡 |

### 3.3 Processo de manutenção e gestão de mudanças

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| M08 | Processo de manutenção definido (como entra um pedido, quem analisa, quem aprova, como é validado) | Fluxo de defeitos descrito no plano v1.2, 9.6 (severidade, prazo, anel de revisão). Fluxo de mudança de escopo na seção 12. É plano, ainda não foi exercido | 🟡 |
| M09 | Formulário de solicitação de mudança (SWEBOK 8.3.1.3) com: descrição, motivo, categoria, impacto, esforço estimado, decisão, responsável | Não existe modelo de issue nem de MUD | ❌ |
| M10 | **Análise de impacto** documentada para mudanças relevantes (SWEBOK 7.2.1.3) | `decisoes-plano-v1.2.md` registra decisões B1–B12 e o que mudou no plano, que é uma forma de análise de impacto **documental**. Não há análise de impacto sobre o código | 🟡 |
| M11 | Testes de regressão automáticos executados a cada mudança | Os testes existem, mas não há CI (`.github/` ausente), então nada roda sozinho | 🟡 |
| M12 | Baselines identificadas e versões das entregas (interface com GCS) | Documentos versionados por pasta (`ers/v1.0`, `ers/v2`, `plano/v1.1`, `plano/v1.2`). Sem tags de release do código e sem `CHANGELOG` | 🟡 |
| M13 | Interface com Garantia da Qualidade: revisão antes de aceitar a mudança | Anel de revisão A→B→C→D→A e template de PR com "Design do incremento" previstos no plano. Não há evidência de PR revisado no snapshot | 🟡 |

### 3.4 Técnicas de manutenção

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| M14 | **Rastreabilidade bidirecional** requisito ↔ código ↔ teste | Convenção definida (o nome do teste cita o CA, ex.: `deveRejeitarEdicaoAposSubmissao_CA14_2`), mas os testes atuais não seguem a convenção e não há matriz RF → arquivo → teste | 🟡 |
| M15 | Compreensão de programa / engenharia reversa: documentar a arquitetura **como implementada** | `docs/arquitetura-aluno-processamento.png` e `infra/README.md` descrevem o fluxo real. O plano v1.2 ainda descreve outra arquitetura (monólito Spring) | 🟡 |
| M16 | **Reengenharia** registrada: decisão de sair de monólito Java para serverless Python | O `infra/README.md` diz que a divergência "deve ser registrada pela equipe". Não há ADR | ❌ |
| M17 | Refatoração com testes de proteção | Nenhuma refatoração registrada | ❌ |
| M18 | Estimativa de custo e prazo de mudança | O plano estima tarefas em horas (seção 8). Não há estimativa por pedido de mudança | 🟡 |
| M19 | Ameaças à segurança durante a manutenção (SWEBOK 7 e 13) | Pontos fortes no código: autenticação IAM no PostgreSQL com TLS `verify-full`, consultas parametrizadas, nenhum texto do aluno enviado ao modelo, controle de dono no GET. Falta varredura de dependências (Dependabot/pip-audit/npm audit) e checklist de segurança no PR | 🟡 |
| M20 | Plano de descarte / descontinuação (retenção de dados, remoção de recursos) | `DeletionPolicy: Retain` no S3 e DynamoDB. O README avisa que isso não é política de retenção. Não há procedimento de descarte nem de exclusão de dados do aluno | ❌ |

### 3.5 Competências mínimas

| Competência | Situação | O que falta para fechar |
|---|---|---|
| C1 Planejar a sustentação | 🟡 | Documento de sustentação: quem mantém, como, por quanto tempo, com quais SLAs e dados de operação (ver T-M04) |
| C2 Transição para produção | 🟡 | Existe roteiro `sam validate/build/deploy`. Falta checklist de transição, smoke test e rollback ensaiado (alinhar com o doc de Implantação) |
| C3 Suporte e registro de pedidos de mudança | ❌ | Templates de issue (defeito, mudança), rótulos por categoria e quadro de manutenção |
| C4 Manutenção corretiva, adaptativa, preventiva e aditiva | 🟡 | Executar e registrar **uma de cada**, com issue, PR, teste de regressão e nota de release |

## 4. Lacunas mais importantes

1. **Não há nenhum pedido de mudança registrado.** A disciplina avalia o *processo*. Sem MUD/DEF preenchidos, a manutenção feita fica invisível.
2. **A reengenharia Java → Python/serverless não tem ADR.** É a mudança mais relevante do projeto e a melhor evidência de manutenção adaptativa, mas hoje aparece só como aviso no README. Além disso, contraria um "fato confirmado pela equipe" ("persistência em Java, exigência do enunciado"). Isso precisa ser resolvido com o professor.
3. **Sem CI, não há regressão automática.** Os testes existem e são bons, mas não protegem as mudanças.
4. **Documentação desatualizada em relação ao código.** O plano v1.2 descreve Spring Boot, Flyway e Docker Compose. O código usa Lambdas, SAM e migração SQL manual. Alinhar isso é, em si, uma manutenção perfectiva de documentação.
5. **Defeito latente conhecido:** o teste `TermoDeCiencia.test.tsx` confirma conexão com `/api/health`, rota que não existe na API SAM. Bom candidato para a manutenção **corretiva** registrada.

## 5. TODO

Prioridade: **P1** necessário para a avaliação · **P2** recomendado · **P3** se sobrar tempo.

- [ ] **T-M01 (P1)** Criar `docs/manutencao/processo-de-manutencao.md`: fluxo pedido → análise de impacto → aprovação → implementação → regressão → implantação → fechamento, com papéis do anel A→B→C→D.
- [ ] **T-M02 (P1)** Criar templates `.github/ISSUE_TEMPLATE/defeito.yml` e `mudanca.yml` com campos: categoria ISO 14764, motivo, RF/RN afetado, impacto (código, dados, docs, testes), estimativa, decisão, responsável.
- [ ] **T-M03 (P1)** Escrever **ADR-010 — Migração do backend de Spring/Java para AWS Lambda/Python**: contexto, alternativas, decisão, consequências, impacto na ERS e no plano. Levar ao professor a questão da exigência de Java.
- [ ] **T-M04 (P1)** Executar e registrar uma manutenção de cada tipo, cada uma com issue + PR + teste + nota no `CHANGELOG.md`:
  - [ ] **Corretiva:** ajustar o health check do `TermoDeCiencia` (rota `/api/health` inexistente) ou criar a rota.
  - [ ] **Adaptativa:** registrar formalmente a troca para serverless (MUD ligada ao ADR-010) ou outra adaptação de ambiente (ex.: versão de runtime).
  - [ ] **Preventiva:** rotina de reconciliação de revisões presas em `PROCESSANDO` e alarme da DLQ (limitações já listadas no `infra/README.md`).
  - [ ] **Aditiva:** uma funcionalidade nova da ERS, ex.: listagem de versões da produção (hoje a API não oferece).
- [ ] **T-M05 (P1)** Matriz de rastreabilidade `docs/manutencao/rastreabilidade.md`: RF/RN → arquivo(s) → teste(s), nos dois sentidos. Renomear testes para citar o CA conforme a convenção.
- [ ] **T-M06 (P2)** Medir e registrar indicadores antes e depois das manutenções: cobertura (`coverage.py`, `vitest --coverage`), complexidade ciclomática (`radon`), número de defeitos por módulo, tempo entre abertura e fechamento de cada DEF/MUD.
- [ ] **T-M07 (P2)** Backlog de dívida técnica (`docs/manutencao/divida-tecnica.md`) a partir das limitações do `infra/README.md`, com custo estimado e prioridade (SWEBOK 7.2.3.1).
- [ ] **T-M08 (P2)** Atualizar o plano mestre (v1.3) para refletir a arquitetura implementada; registrar a mudança documental como MUD perfectiva.
- [ ] **T-M09 (P2)** Plano de sustentação (C1): janela de suporte, canais, SLA por severidade (reaproveitar a tabela 88 do plano), dados operacionais coletados, critério de descontinuação.
- [ ] **T-M10 (P3)** Parágrafo sobre leis de Lehman aplicadas ao projeto (crescimento de escopo ERS v1 → v2, aumento de complexidade com a arquitetura assíncrona).
- [ ] **T-M11 (P3)** Procedimento de descarte: exclusão de dados do aluno no S3 (todas as versões), DynamoDB e PostgreSQL; remoção da stack.

## 6. Entregáveis sugeridos para a avaliação

| Entregável | Cobre |
|---|---|
| `processo-de-manutencao.md` + templates de issue | C3, M08, M09 |
| 4 MUD/DEF fechados (uma de cada categoria), com PR e teste | C4, M01, M02, M11 |
| ADR-010 (reengenharia) | M10, M16, C4 adaptativa |
| Matriz de rastreabilidade | M14 |
| Relatório de métricas antes/depois | M06 |
| Plano de sustentação | C1 |

## 7. Uso de IA

Documento redigido com apoio de IA a partir da ementa do PPC 2024, do SWEBOK v4 e do snapshot do repositório. A equipe deve revisar as avaliações de situação antes de usar este material.
