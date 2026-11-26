# Conformidade do PI26 com Implantação e Entrega de Software

Versão: 1.0 · Data: 25/11/2026 · Autor: Luiz Augusto Godinho (com apoio de IA) · Revisor: pendente · Estado: rascunho para a equipe

Projeto avaliado: **Assistente de Escrita Processual — Grupo 8** (POC 2.2), snapshot `PI26-assist-escrita-proc-main`.

## 1. Para que serve este documento

Diz o que a disciplina **Implantação e Entrega de Software** (6º período, 64 h, 32 teóricas + 32 práticas, pré-requisito: Implementação e Integração de Software) espera ver no projeto interdisciplinar, onde o projeto já atende e o que falta fazer. Cada item cruza:

- **Ementa e competências mínimas** do PPC 2024 do BES;
- **SWEBOK v4, capítulo 6 (Software Engineering Operations)** como foco principal, mais 8.6 (Release Management and Delivery), 4 (Construção) e 7.4.4 (CI/CD na manutenção);
- Bibliografia: Humble & Farley (*Entrega Contínua*), Kim et al. (*Manual de DevOps*), Duvall et al. (*Continuous Integration*), McConnell (*Code Complete*), Fowler (*Refatoração*), Martin (*Clean Code*).

A ementa desta disciplina vai além de deploy: inclui **detecção e remoção de defeitos** e **técnicas avançadas de implementação**. Os dois blocos estão na matriz.

Legenda de situação: ✅ atende · 🟡 parcial · ❌ não atende · ➖ não se aplica nesta entrega.

## 2. O que a disciplina pede

### 2.1 Ementa (resumo por bloco)

| Bloco | CH | Conteúdo | SWEBOK |
|---|---|---|---|
| Conceitos de DevOps | 4 h | Conceitos básicos e histórico | 6.1, 6.3.2 |
| Técnicas de integração de código | 16 h | Integração baseada no design; configuração em tempo de execução; build; entrega (delivery) e implantação (deploy); automação de integração, transição e entrega contínuas; monitoramento | 6.1.4, 6.2.2, 6.3.1–6.3.3, 6.4.2, 6.6, 8.6 |
| Detecção e remoção de defeitos | 16 h | Leitura e inspeção de código; depuração; refatoração; classificação e tratamento de defeitos e débitos técnicos | 4, 6.1.5, 7.2.3.1 |
| Técnicas avançadas de implementação | 28 h | Polimorfismo, reflexão, expressões regulares, generics, closures, logging, internacionalização e localização | 4.4 |

### 2.2 Competências mínimas (todas "faz com orientação")

- **C1** Construir código de forma colaborativa em equipe.
- **C2** Usar e configurar ferramentas de edição, documentação, compilação, testes de unidade e integração, e depuração.
- **C3** Usar e configurar ferramentas de controle de versão, coleta de medidas (desempenho, memória, análise estática, cobertura), build e transição.
- **C4** Usar processos e técnicas adequados de implementação e integração (codificação, versionamento, inspeção, teste, depuração).
- **C5** Avaliar medidas e atributos de qualidade de código.
- **C6** Ler código, localizar defeitos, depurar e refatorar.

## 3. Matriz de conformidade

### 3.1 DevOps, build e implantação

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| I01 | Infraestrutura como código (SWEBOK 6.1.4, 6.5.3) | `infra/template.yaml` (AWS SAM/CloudFormation) provisiona Cognito, API REST, WebSocket, S3, CloudFront, SNS, SQS + DLQ, DynamoDB e 5 Lambdas | ✅ |
| I02 | Build reproduzível | `sam build --use-container` (dependência nativa `psycopg[binary]` compilada para Linux); `npm ci` + `vite build` com `package-lock.json`; versão de `psycopg` fixada | ✅ |
| I03 | Procedimento de implantação documentado | `infra/README.md` (seção "Validar e implantar") e `frontend/README.md`. Publicação da SPA no bucket é manual | 🟡 |
| I04 | **Pipeline de CI** que roda testes, lint e build a cada PR | Não existe `.github/workflows`. O plano v1.2 (10.5, Tabela 89) descreve o pipeline, mas para a stack Java/Maven antiga | ❌ |
| I05 | **Entrega/implantação contínua** automatizada (deploy a partir da `main` ou de tag) | Deploy é manual (`sam deploy --guided`) | ❌ |
| I06 | Ambientes separados (dev, homologação/staging, produção) (SWEBOK 6.2.2 e 6.3.2) | Um único `sam deploy` sem parâmetros por ambiente nem `samconfig.toml` por estágio. Estágio da API fixo em `v1` | ❌ |
| I07 | Configuração em tempo de execução separada do código | Parâmetros do template (`DatabaseHost`, `BedrockModelArn`, ...) e variáveis de ambiente das Lambdas; `VITE_*` no frontend com `.env.example`; `.env` no `.gitignore` | ✅ |
| I08 | Segredos fora do repositório | Sem senhas no código: autenticação IAM no PostgreSQL; `.env` ignorado; README avisa que `VITE_*` é público | ✅ |
| I09 | **Estratégia de release e versionamento** (SWEBOK 8.6.2: SemVer, tags, notas de release) | Plano prevê v0.1.0 → v1.0.0 por marco (Tabela 90). Não há tag, `CHANGELOG` nem release publicada. `package.json` está em 0.1.0 | 🟡 |
| I10 | **Rollback** planejado e ensaiado (SWEBOK 6.3.3) | CloudFormation reverte stack com falha automaticamente, mas não há procedimento de rollback de versão das Lambdas (aliases/versões), do frontend (versão anterior no S3) nem do banco | ❌ |
| I11 | Estratégia de release com baixo risco (staging, canary, feature toggle) (SWEBOK 6.3.2) | Nenhuma. Lambdas sem `AutoPublishAlias`/`DeploymentPreference` | ❌ |
| I12 | Smoke test / teste operacional de aceitação após o deploy (SWEBOK 6.3.1) | `infra/tests/run_integracao.py` roda o fluxo com PostgreSQL em container e AWS simulada. O README pede um teste com dados sintéticos na conta AWS (POST, evento, GET, recusa a outro usuário), mas não há script contra o ambiente implantado | 🟡 |

### 3.2 Operação e monitoramento

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| I13 | **Monitoramento e telemetria** (SWEBOK 6.4.2, 6.6.4): métricas, logs, rastreamento | Logs padrão do CloudWatch via `logging`. Sem X-Ray (`Tracing`), sem alarmes, sem dashboard, sem retenção de logs definida | ❌ |
| I14 | Alarme da **DLQ** e procedimento de reprocessamento | DLQ `FilaFalhas` existe com `maxReceiveCount: 5`. README diz que "precisa de monitoramento e procedimento de reprocessamento" | 🟡 |
| I15 | Gestão de incidentes e problemas (SWEBOK 6.3.5, 6.4.1) | Plano tem severidades (Tabela 88). Não há runbook de incidente | 🟡 |
| I16 | Disponibilidade, capacidade e custo (SWEBOK 6.2.3, 6.2.4) | Serverless pay-per-request; DynamoDB sob demanda; README avisa que o deploy gera custo. Sem limites de concorrência, orçamento (AWS Budgets) ou metas de disponibilidade | 🟡 |
| I17 | Backup, recuperação de desastre e failover (SWEBOK 6.2.5) | PITR no DynamoDB; S3 versionado e retido. PostgreSQL fora da stack e sem backup tratado | 🟡 |

### 3.3 Detecção e remoção de defeitos

| # | O que se espera ver no projeto | Evidência hoje | Situação |
|---|---|---|---|
| I18 | Inspeção / revisão de código registrada | Anel de revisão e template de PR previstos no plano (seções 7 e 10.4). Sem PRs revisados no snapshot (sem `.git`) | 🟡 |
| I19 | Análise estática configurada | ESLint (`eslint.config.js`) e `tsc --strict` no frontend. **Nada no Python** (sem ruff, flake8, mypy, bandit) | 🟡 |
| I20 | Testes de unidade e integração | 9 testes unitários Python com dublês, 1 teste integrado opcional com PostgreSQL real, 7 testes Vitest + Testing Library | ✅ |
| I21 | Medida de cobertura | Não configurada (nem `coverage.py` nem `vitest --coverage`) | ❌ |
| I22 | Classificação e tratamento de defeitos e débitos técnicos | Tabela de severidade no plano (9.6). Débitos listados como "Limitações operacionais" no `infra/README.md`, sem registro formal | 🟡 |
| I23 | Refatoração com testes de proteção | `frontend/src/pages/Escrita.tsx` tem todo o JSX da tela em **uma única linha**, o que prejudica leitura, revisão e diff. Bom candidato. Nenhuma refatoração registrada | ❌ |
| I24 | Depuração documentada (um defeito encontrado, reproduzido, corrigido) | Nenhum registro. Candidato: o teste do `TermoDeCiencia` usa `/api/health`, rota que a API SAM não tem | ❌ |

### 3.4 Técnicas avançadas de implementação

| # | Técnica | Evidência hoje | Situação |
|---|---|---|---|
| I25 | Expressões regulares | `processador_bedrock/app.py`: validação da chave S3 (`re.fullmatch`), contagem de palavras, frases e parágrafos | ✅ |
| I26 | Generics (parametrização) | `getJson<T>` em `api/http.ts` e `request<T>` em `api/revisoes.ts` | ✅ |
| I27 | Closures | Handlers e hooks React no frontend (callbacks que capturam estado) | ✅ (implícito) |
| I28 | Logging | `logging` nas Lambdas, sem vazar texto (`exc_info=False`). Falta log estruturado (JSON), nível configurável e ID de correlação (`id_producao`, `requestId`) | 🟡 |
| I29 | Polimorfismo | Não há uso deliberado. Oportunidade: interface `Analisador` com implementação Bedrock e implementação falsa para testes/CI | ❌ |
| I30 | Reflexão | Não há uso deliberado (só `importlib` nos testes) | ❌ |
| I31 | Internacionalização e localização | Textos em pt-BR fixos no código; só datas usam `Intl.DateTimeFormat('pt-BR')` | 🟡 |

### 3.5 Competências mínimas

| Competência | Situação | Evidência ou o que falta |
|---|---|---|
| C1 Código colaborativo | 🟡 | GitHub Flow, Conventional Commits e anel de revisão definidos. Mostrar histórico de PRs revisados |
| C2 Ferramentas de edição, build, testes, depuração | ✅ | Vite, Vitest, ESLint, SAM CLI, `unittest`, Docker para build |
| C3 Controle de versão, medidas, build e transição | 🟡 | Falta coleta de medidas (cobertura, análise estática Python, desempenho) e pipeline de transição |
| C4 Processos de implementação e integração | 🟡 | Processo definido no plano, sem automação de CI |
| C5 Avaliar qualidade de código | ❌ | Nenhum relatório de métricas |
| C6 Ler, localizar defeitos, depurar, refatorar | ❌ | Fazer e registrar pelo menos um ciclo completo (I23, I24) |

## 4. Lacunas mais importantes

1. **Não há CI/CD.** É o centro da disciplina e hoje tudo é manual. O pipeline descrito no plano é para Maven/Java e precisa ser reescrito para Python + SAM + Node.
2. **Não há rollback nem estratégia de release.** SWEBOK 6.3.3 pede rollback planejado e ensaiado antes de ir a produção.
3. **Não há observabilidade.** Sem alarmes, a DLQ pode acumular falhas sem ninguém perceber.
4. **Um único ambiente.** Sem staging, não dá para mostrar promoção entre ambientes.
5. **Técnicas avançadas parciais.** Polimorfismo, reflexão e i18n não aparecem; é preciso uso deliberado e documentado.

## 5. TODO

Prioridade: **P1** necessário para a avaliação · **P2** recomendado · **P3** se sobrar tempo.

**CI/CD e release**

- [ ] **T-I01 (P1)** Criar `.github/workflows/ci.yml`, disparado em PR e push na `main`:
  - frontend: `npm ci`, `npm run lint`, `npm test -- --coverage`, `npm run build`;
  - backend: `ruff check`, `python -m unittest discover -s infra/tests`, `coverage report`;
  - infra: `sam validate --lint`.
  - Falha bloqueia merge (proteção de branch).
- [ ] **T-I02 (P1)** Criar `.github/workflows/deploy.yml`: em tag `v*`, `sam build` + `sam deploy` no ambiente de homologação, upload do `dist/` para o bucket do frontend, invalidação do CloudFront, smoke test. Credenciais via OIDC da AWS (sem chave longa no repositório).
- [ ] **T-I03 (P1)** Separar ambientes: `samconfig.toml` com `[dev]` e `[prod]` (ou `hml`), nomes de stack distintos, parâmetros por ambiente.
- [ ] **T-I04 (P1)** Versionamento de release: SemVer com tags (v0.x conforme Tabela 90 do plano), `CHANGELOG.md` no formato Keep a Changelog, GitHub Release com notas.
- [ ] **T-I05 (P1)** Rollback documentado e **ensaiado**: Lambdas com `AutoPublishAlias: vivo`, voltar o alias para a versão anterior; frontend mantendo o `dist` anterior no S3; banco com backup antes da migração. Registrar o ensaio (data, passos, tempo).
- [ ] **T-I06 (P2)** Implantação gradual: `DeploymentPreference` (ex.: `Canary10Percent5Minutes`) com alarme de erro que dispara rollback automático (SWEBOK 6.3.2 e 6.3.3).
- [ ] **T-I07 (P2)** Smoke test automatizado pós-deploy: script que cria usuário sintético, faz POST, espera o resultado, faz GET e confirma a recusa a outro usuário.

**Operação**

- [ ] **T-I08 (P1)** Observabilidade no template: `Tracing: Active` (X-Ray), `LoggingConfig` com formato JSON e retenção de logs, alarmes CloudWatch para erros das Lambdas, 5xx da API e **mensagens na DLQ**, com notificação por SNS/e-mail.
- [ ] **T-I09 (P2)** Runbook `docs/operacao/runbook.md`: como reprocessar a DLQ, como reconciliar revisões presas em `PROCESSANDO`, o que fazer quando o Bedrock falha, contatos e severidades.
- [ ] **T-I10 (P2)** Controle de custo: AWS Budgets com alerta, `ReservedConcurrentExecutions` no processador.
- [ ] **T-I11 (P3)** Dashboard CloudWatch com latência, erros, tamanho da fila e duração do processamento.

**Defeitos e qualidade de código**

- [ ] **T-I12 (P1)** Análise estática no Python (`ruff`, `mypy` opcional, `bandit` para segurança) e cobertura nos dois lados. Publicar relatório no CI.
- [ ] **T-I13 (P1)** Refatorar `Escrita.tsx` em componentes (`Sidebar`, `Editor`, `PainelRevisao`, `ListaVersoes`), com os testes atuais garantindo o comportamento. Registrar antes/depois (tamanho, complexidade).
- [ ] **T-I14 (P1)** Registrar um ciclo de depuração completo: o defeito do `/api/health` (relato → reprodução → causa → correção → teste de regressão).
- [ ] **T-I15 (P2)** Relatório de qualidade de código (C5): cobertura, complexidade (`radon`/ESLint `complexity`), duplicação, avisos de lint, antes e depois das refatorações.

**Técnicas avançadas**

- [ ] **T-I16 (P2)** Polimorfismo: interface `Analisador` (Protocol/ABC) com `AnalisadorBedrock` e `AnalisadorFalso`, escolhido por configuração. Também viabiliza a CI sem chamar o Bedrock (como o plano já previa com "adaptador falso").
- [ ] **T-I17 (P2)** Logging estruturado com ID de correlação (`id_producao`, `requestId`) e nível via variável de ambiente, nunca registrando texto do aluno nem token.
- [ ] **T-I18 (P3)** Internacionalização: extrair os textos da interface para um arquivo de mensagens (`pt-BR.json`) e usar `Intl` para números e datas.
- [ ] **T-I19 (P3)** Reflexão: uso justificado, por exemplo registro dinâmico de handlers ou carregamento do analisador por nome de classe configurado. Só se fizer sentido; não forçar.

## 6. Entregáveis sugeridos para a avaliação

| Entregável | Cobre |
|---|---|
| Workflows de CI e deploy rodando, com badge no README | I04, I05, C3, C4 |
| Dois ambientes com promoção dev → prod | I06 |
| Release v1.0.0 com `CHANGELOG` e notas | I09 |
| Registro do ensaio de rollback | I10 |
| Alarmes + runbook | I13–I15 |
| Relatório de qualidade antes/depois da refatoração | I21, I23, C5, C6 |
| Ciclo de depuração registrado | I24, C6 |

## 7. Uso de IA

Documento redigido com apoio de IA a partir da ementa do PPC 2024, do SWEBOK v4 e do snapshot do repositório. A equipe deve revisar as avaliações de situação antes de usar este material.
