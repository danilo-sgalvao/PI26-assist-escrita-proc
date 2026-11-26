# Backlog do que falta — Assistente de Escrita Processual

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data | 25/11/2026 |
| Autor | Equipe do Grupo 8, redação com apoio de IA (Claude Code, Claude Opus 5.5) |
| Revisor | Pendente |
| Estado | Proposta para a equipe |

## 1. Para que serve

Lista as tarefas que faltam para entregar a POC. Cada tarefa cita os requisitos que atende e os itens de conformidade das três disciplinas que cobre. A seção 9 faz o caminho inverso: para cada item de conformidade, mostra a tarefa que o fecha.

Base usada:

- o que está implementado na `main` (commits de 11/11/2026: AWS SAM, cinco Lambdas em Python, telas de escrita e de termo);
- as decisões de 16/11 e 19/11/2026 (arquitetura serverless definitiva, persistência em Python, decisões D1 a D5 e fatias 1 a 5), registradas em [DES];
- os documentos de conformidade locais [CF-MS], [CF-PD] e [CF-IE].

As tarefas continuam a numeração do plano mestre (T01–T65) a partir de **T66**. As tarefas do plano v1.2 que ainda fazem sentido foram absorvidas por estas; a seção 10 mostra a correspondência.

## 2. Documentos de referência

| Sigla | Documento |
|---|---|
| [ERS] | [ERS v2](../ers/v2/ERS-Grupo8-v2.md): requisitos RF, RN e RNF |
| [PM] | [Plano mestre v1.2](../plano/v1.2/plano-mestre-v1.2.md): processo, qualidade, riscos e modelos (apêndices) |
| [DEC] | [Decisões B1–B12](../plano/v1.2/decisoes-plano-v1.2.md) |
| [DES] | [Design: modelo de dados e contrato da API](../arquitetura/modelo-de-dados-e-api.md): decisões D1–D5 e fatias |
| [INF] | [README da infra](../../infra/README.md): fluxo atual e limitações operacionais |
| [CF-MS] | [Conformidade com Manutenção de Software](../conformidade/01-manutencao-de-software.md): itens M01–M20, tarefas T-M01–T-M11 |
| [CF-PD] | [Conformidade com Software para Persistência de Dados](../conformidade/02-software-para-persistencia-de-dados.md): itens P01–P20, tarefas T-P00–T-P12 |
| [CF-IE] | [Conformidade com Implantação e Entrega de Software](../conformidade/03-implantacao-e-entrega-de-software.md): itens I01–I31, tarefas T-I01–T-I19 |

**Áreas** (plano mestre, seção 7): A = Requisitos/Produto/Qualidade · B = Frontend · C = Backend/API/Assistente · D = Persistência/Dados/Infra. Quem fica em cada área ainda não foi definido (T70).

**Prioridade:** para requisitos de produto vale o MoSCoW da ERS (*Must*, *Should*, *Could*). Para os itens só de conformidade vale a escala dos documentos de conformidade: **P1** necessário para a avaliação · **P2** recomendado · **P3** se sobrar tempo.

## 3. Ordem sugerida

1. **Fase 0** (seção 4) antes de qualquer fatia. Sem o ADR-010 e sem CI, o resto não conta como evidência de manutenção nem de entrega.
2. **Fatias 1 → 3** (seções 5.1 a 5.3). Com o contrato da API fixado em [DES], frontend e backend de uma mesma fatia podem andar em paralelo.
3. **Operação e entrega** (seção 6) a partir da fatia 1, porque ambientes, deploy e alarmes valem para todas as fatias.
4. **Fatias 4 e 5** (seções 5.4 e 5.5) conforme a capacidade, respeitando a ordem de corte: RF19 → RF20 → RF11/RF12 → RF15.
5. **Encerramento** (seção 8) na última semana.

## 4. Fase 0 — Regularização

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T66 | **ADR-010 — Reengenharia de Java/Spring para AWS Lambda/Python**, registrada também como **MUD-001 (adaptativa)**. Levar ao professor a exigência de persistência em Java e registrar a resposta. Os três caminhos estão em [CF-PD] seção 5; a opção 2 (agregado em Java) mudaria T76–T79 | C (revisão B e D) | P1 | [PM] seção 6.8 e Apêndice A; [INF]; [CF-MS] M10, M16, T-M03; [CF-PD] seção 5, T-P00 | ADR com contexto, alternativas, decisão e consequências; resposta do professor registrada; MUD-001 classificada como adaptativa |
| T67 | Integrar à `main` o que já está pronto: decisões de 19/11 (PR #67, issue #13), protótipo T05 e ADR-006 do Bedrock (PR #2, ajustado à API Converse). Fechar com comentário os PRs superados (backend Spring e base RAG), ou reaproveitá-los se T66 escolher a opção 2 | A | P1 | [PM] seção 10.4; [CF-MS] M12, M13 | `main` contém [DES], o protótipo e o ADR-006; nenhum PR aberto sem decisão |
| T68 | **Processo de manutenção**: `docs/manutencao/processo-de-manutencao.md` (pedido → impacto → aprovação → implementação → regressão → implantação → fechamento, com o anel A→B→C→D). Templates `.github/ISSUE_TEMPLATE/defeito.yml` e `mudanca.yml` (categoria ISO 14764, motivo, RF/RN afetado, impacto, estimativa, decisão, responsável), modelo de PR, CODEOWNERS e proteção da `main` | A | P1 | [PM] seções 9.6, 10.4 e 12.3, Apêndice C; [CF-MS] M01, M08, M09, M18, C3, T-M01, T-M02 | Templates em uso; push direto na `main` bloqueado; PR exige revisão de outra área |
| T69 | **CI** em `.github/workflows/ci.yml`, em PR e push na `main`: frontend (`npm ci`, lint, `npm test -- --coverage`, build); Python (`ruff check`, `bandit`, `unittest`, `coverage report`); infra (`sam validate --lint`). Falha bloqueia o merge | D (revisão C) | P1 | [PM] seção 10.5; [CF-IE] I04, I19, I21, C3, C4, T-I01, T-I12; [CF-MS] M11 | Pipeline verde na `main`; um PR com teste quebrado é bloqueado; relatório de cobertura publicado |
| T70 | **Replanejamento**: definir quem fica em cada área (antiga T01) e a data D0; reestimar as tarefas deste backlog dentro da capacidade fixa (B12); montar o quadro Kanban com elas. Publicar o **plano v1.3** com a arquitetura implementada, registrado como MUD perfectiva (sem apagar a v1.2) | A | P1 | [PM] seções 4.8, 7 e 8; [DEC] B12; [CF-MS] M15, M18, T-M08 | Áreas atribuídas; quadro com estimativas; plano v1.3 aprovado pela equipe |
| T71 | **Pendências com o professor e o stakeholder**: perguntas Q-xx ainda abertas, B5 (agora aplicado à redação do catálogo, [DES] seção 7.1), B10 (tempo de resposta), faixa etária, prazo de retenção, critério de sucesso do piloto | A | P1 | [ERS] seção 10; [PM] seção 5.8; [DEC] B5, B10 | Cada pendência com resposta ou hipótese aceita e registrada |
| T72 | **HU, CA e rastreabilidade**: HU e CA de cada fatia, uma fatia à frente; matriz bidirecional `docs/manutencao/rastreabilidade.md` (RF/RN → arquivo → teste e o inverso); testes renomeados para citar o CA | A (revisão D) | P1 | [PM] seções 5.4 e 11.3; [CF-MS] M14, T-M05 | Todo RF *Must* com CA; matriz cobre o código existente; nomes de teste citam o CA |
| T73 | **Ferramenta de migração e backup do PostgreSQL**: adotar yoyo, Alembic ou sqitch (Flyway se T66 escolher Java), com tabela de histórico e execução no deploy; `001` passa a ser controlada por ela. Backup (snapshot do RDS ou `pg_dump`) antes de cada migração, com teste de restauração e migração reversível | D (revisão C) | P1 | [PM] seção 10.8; [CF-PD] P12, P16, P20, C3, T-P05, T-P10; [CF-IE] I17 | Migrações aplicadas pela ferramenta; restauração ensaiada e registrada |

## 5. Produto, por fatia ([DES] seção 9)

### 5.1 Fatia 1 — Identidade e atividades

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T74 | **Migração 002** com todo o modelo de [DES] seção 4 (usuários, turmas, matrículas, atividades, produções, versões, transições, colagens, interações). Permissões de imutabilidade (só `INSERT`/`SELECT` em `versoes`, `transicoes_etapa` e `colagens`). Documentar uma **refatoração de banco** do catálogo de Ambler (por exemplo *Introduce Column Constraint*) e uma **migração de dados** (registros de `revisoes` de demonstração para o novo esquema, ou justificar se não houver dados) | D (revisão C) | *Must* / P1 | RN03, RN04, RNF09; [DES] seções 3 e 4; [CF-PD] P01, P10, P17, P18, P19, C5, T-P06, T-P07 | Migração roda em banco vazio e sobre a `001`; teste prova que `UPDATE` e `DELETE` em versões são negados |
| T75 | **Documentação de dados**: `docs/dados/arquitetura-de-dados.md` (o que fica em PostgreSQL, S3 e DynamoDB, persistência poliglota, padrão *claim-check*, consistência eventual); **ADR-011 — Persistência poliglota**; modelo ER implementado e dicionário de dados (tipo, restrição, significado, se é dado pessoal) | D (revisão A) | P1 | [DES] seção 3; [CF-PD] P02, P03, P08, P15, C1, C2, T-P01, T-P02, T-P03 | Documento e ADR revisados; dicionário cobre todas as colunas da `002` |
| T76 | **Camada de repositórios** em `infra/lambdas/` (SQL fora dos *handlers*) e roteador interno por rota em `ingestao` (escritas) e `consulta` (leituras), com testes | C (revisão D) | P1 | [DES] seção 2; [CF-PD] P07, C4, T-P04 | Nenhum SQL nos *handlers*; testes dos repositórios no CI |
| T77 | **Perfis e autorização**: grupos `estudantes` e `professores` no Cognito (template SAM), leitura de `cognito:groups`, `404` para recurso de outra pessoa, `403 TERMO_PENDENTE` | C (revisão B) | *Must* | RF22, RNF03; [DES] seção 5 | Testes de acesso cruzado entre estudantes e entre turmas negado |
| T78 | **API de identidade e turmas**: `GET /eu` (cria o usuário e vincula matrículas pelo e-mail), `POST /eu/termo`, `POST/GET /turmas`, `POST/GET /turmas/{id}/estudantes` com `consentimento_responsavel` | C (revisão B) | *Must* | RF16, RF21, RF22, RNF02; [DES] seção 6; [CF-PD] C4, T-P08 (CRUD de entidade de negócio) | Testes de API verdes; contrato revisado por B |
| T79 | **API de atividades**: `POST /atividades`, `GET /atividades`, `GET /atividades/{id}`, com gênero em lista fechada, prazo e `aceita_apos_prazo` | C (revisão B) | *Must* | RF01, RF16; [DEC] B4; [DES] seção 6 | Estudante só vê as atividades das suas turmas, verificado em teste |
| T80 | **Telas da fatia 1**: login Cognito com perfil; aceite do termo gravado no servidor (o texto informa o processamento pelo Amazon Bedrock, sem uso para treinamento); lista de atividades do estudante; turmas, matrículas e cadastro de atividade do professor | B (revisão A) | *Must* | RF01, RF16, RF21, RF22, RNF10, RN10; [DES] seção 9 | CA verificados por A; testes de componente |
| T81 | **Testes de aceitação da fatia 1** | A (revisão D) | *Must* | RF01, RF16, RF21, RF22; [PM] seção 9 | Todos os CA executados; defeitos registrados como DEF |

### 5.2 Fatia 2 — Produção e versões

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T82 | **API de produção**: `POST /atividades/{id}/producoes` (inicia na etapa Planejar ou devolve a existente), `GET /producoes/{id}` | C (revisão B) | *Must* | RF02, RF03; [DES] seção 6 | Uma produção por estudante e atividade, verificado em teste |
| T83 | **Versões**: `POST/GET /producoes/{id}/versoes` com filtro por etapa e tipo; não grava versão sem mudança (`sha256`); grava primeiro no S3, depois no PostgreSQL; calcula `palavras_alteradas`. Registrar como a **manutenção aditiva** da T112 | C e D (revisão B) | *Must* | RF04, RF05, RF11, RN04, RNF07, RNF09; [DES] seção 4; [CF-PD] P09, P10; [CF-MS] T-M04 (aditiva) | Histórico lido do servidor; teste de versão sem mudança; nenhum registro preso por falha do S3 |
| T84 | **Comparação de versões no servidor** (`difflib`, por palavras e pontuação), em função compartilhada; `GET /producoes/{id}/comparacao` | C (revisão D) | *Must* | RF06; [DES] decisão D5 | Casos de inserção, remoção e alteração corretos em teste |
| T85 | **Etapas**: `POST /producoes/{id}/etapa` (avançar e voltar), transição registrada e versão marcada | C (revisão B) | *Must* | RF17; [DES] seção 6 | Transições e voltas verificadas; troca de etapa após a submissão rejeitada |
| T86 | **Submissão**: versão final marcada, política de prazo (padrão: aceita e marca atrasada), `409` após submissão; deixa pronto o evento que dispara a similaridade (T102) | C (revisão B) | *Must* | RF14; [DEC] B4 | Edição após a submissão rejeitada em teste |
| T87 | **Editor da fatia 2**: etapas com espaço do Planejar, salvamento automático a cada minuto com indicador de estado, histórico do servidor (sai o `sessionStorage`), comparação lado a lado, submissão. Antes de mexer, **refatorar `Escrita.tsx`** em componentes, com os testes atuais como proteção, e registrar o antes e depois | B (revisão A) | *Must* / P1 | RF03–RF06, RF14, RF17, RNF07, RNF10; [CF-IE] I23, C6, T-I13; [CF-MS] M17 | CA verificados por A; refatoração registrada com métricas |
| T88 | **Testes de aceitação da fatia 2** | A (revisão D) | *Must* | RF02–RF06, RF14, RF17 | Todos os CA executados; defeitos registrados |

### 5.3 Fatia 3 — Assistente

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T89 | **Catálogo de orientações** versionado (algumas dezenas de itens *(sugerido)*, texto fixo de recusa e orientação de reserva), com revisão pelas regras de redação; os limites da B5 valem para os textos do catálogo | A e C | *Must* | RF08, RF09, RN07, RN08, RN09; [DES] seção 7.1; [DEC] B5 | Todo item revisado por alguém que não o escreveu; nenhum texto aproveitável numa redação |
| T90 | **Infra do assistente**: tabela `Interacoes` no DynamoDB (decisão D4), filtro de evento do S3 trocado para `pedidos/` (decisão D2); apagar à mão a tabela `Sugestoes` retida | D (revisão C) | *Must* | RF10; [DES] seção 8 (D2, D4) | Stack implantada com a tabela nova; evento só dispara em `pedidos/` |
| T91 | **API de apoio**: `POST /producoes/{id}/apoios` (`202`), `GET` da lista e do detalhe | C (revisão B) | *Must* | RF07, RF10, RF20; [DES] seção 6 | Testes de API verdes |
| T92 | **Novo processador**: lê pedido, versão e contexto, numera parágrafos e frases, chama o Bedrock, faz a **conferência determinística**, converte posições, grava, conclui e notifica; `INDISPONIVEL` quando o Bedrock falha. Interface `Analisador` com implementação Bedrock e implementação falsa para CI (polimorfismo). Teste do montador garante que nenhum `sub`, nome ou e-mail vai ao modelo | C (revisão D) | *Must* / P2 | RF07, RF08, RF09, RF12, RNF04, RNF05, RNF08; FA01, FA02, FA04; [DES] seção 7; [CF-IE] I29, T-I16 | Resposta inválida cai na orientação de reserva; pedido de escrita recebe recusa; CI roda sem chamar o Bedrock |
| T93 | **Painel de apoio no editor**: pedido com trecho selecionado, orientação identificada como gerada por IA, destaque do trecho apontado, aviso de indisponibilidade, WebSocket `APOIO_DISPONIVEL` e consulta a cada 10 s sem WebSocket | B (revisão A) | *Must* | RF07, RF10, RNF08, RNF11; [DES] seções 6 e 7 | CA verificados por A |
| T94 | **Avaliação do assistente**: no mínimo 30 pedidos de escrita ou reescrita, diretos e disfarçados, mais casos legítimos por categoria, variação linguística e pedido de nota, com 2 avaliadores e rubrica. Medir também a latência do gatilho do S3 contra o RNF06 (decisão D2) | A (revisão D) | *Must* | RF08, RF09, RF12, RNF06, RN07, RN08; [PM] seção 9.4; [DEC] B10; [DES] seção 7 | Relatório com resultados; nenhum texto aproveitável; latência medida e decisão sobre D2 registrada |
| T95 | **Testes de aceitação da fatia 3** | A (revisão D) | *Must* | RF07–RF10, RF12 | Todos os CA executados; defeitos registrados |

### 5.4 Fatia 4 — Acompanhamento

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T96 | **Colagens**: `POST/GET /producoes/{id}/colagens` e captura no editor | C e B | *Should* | RF18, RN03, RN06; [DES] seção 6 | Colagem registrada com trecho, tamanho, etapa e horário |
| T97 | **Indicadores**: `GET /producoes/{id}/indicadores` (tempo por etapa, versões, alterações, colagens, apoio por categoria e etapa), calculados por consulta, sem tabela própria | C e D | *Should* | RF11, RF12; [DES] seção 4 | Valores conferidos com dados de teste |
| T98 | **Painel do professor**: `GET /atividades/{id}/acompanhamento` e tela, em ordem alfabética, sem ranking | C e B | *Must* | RF13, RN05, RNF03 | Professor sem vínculo recebe `404`; nenhuma ordenação por indicador |
| T99 | **Meus registros** do estudante, reaproveitando as rotas de leitura | B | *Should* | RF20, RN10 | Estudante só vê os próprios registros |
| T100 | **Testes de aceitação da fatia 4** | A (revisão D) | *Must* | RF11–RF13, RF18, RF20, RN05 | Todos os CA executados |

### 5.5 Fatia 5 — Similaridade e devolutiva

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T101 | **Design da similaridade** na arquitetura atual (consumidor do tópico SNS acionado pela submissão; onde guardar o resultado) e ADR. Atenção: com a decisão D1, as "respostas do assistente" são textos do catálogo, o que muda o que comparar | C (revisão A) | *Should* | RF15, RN06; [DEC] B2; [DES] seção 9 | ADR aceito com fontes, gatilho e armazenamento |
| T102 | **Similaridade**: contenção de n-gramas (n = 5) contra as produções da atividade, relatório na interface por fonte, com trechos e resumo de colagens, **sem veredito** | C e B | *Should* | RF15, RN06 | Cópia literal detectada; sem falso positivo nos casos de controle; nenhuma tela emite veredito |
| T103 | **Devolutiva do professor**, só se sobrar capacidade depois da fatia 4 | B e C | *Could* | RF19 | CA de RF19 verificados |

## 6. Operação e entrega

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T104 | **Ambientes separados**: `samconfig.toml` com `dev` e `hml` (ou `prod`), stacks e parâmetros próprios | D | P1 | [CF-IE] I06, T-I03 | Duas stacks implantadas sem conflito de nomes |
| T105 | **Deploy contínuo**: `.github/workflows/deploy.yml` em tag `v*`, com `sam build` e `sam deploy`, publicação do `dist/` da SPA, invalidação do CloudFront e **smoke test** automático (usuário sintético, POST, espera, GET, recusa a outro usuário). Credenciais por OIDC, sem chave longa no repositório | D (revisão C) | P1 | [CF-IE] I03, I05, I12, T-I02, T-I07; [PM] seção 10.7 | Uma tag implanta em `hml` sem passo manual e o smoke test passa |
| T106 | **Observabilidade**: X-Ray, logs em JSON com retenção, alarmes de erro das Lambdas, 5xx da API e mensagens na DLQ, com aviso por SNS; logging estruturado com ID de correlação, sem texto do aluno nem token; dashboard *(P3)* | D e C | P1 | RNF01, RNF04; [CF-IE] I13, I14, I28, T-I08, T-I11, T-I17 | Alarme dispara num teste provocado; logs sem dado do aluno |
| T107 | **Reconciliação e runbook** (**manutenção preventiva** da T112): rotina que resolve revisões e interações presas em `PROCESSANDO`; procedimento de reprocessamento da DLQ; `docs/operacao/runbook.md` (DLQ, reconciliação, falha do Bedrock, severidades) | C e D | P1 | [INF] limitações operacionais; [CF-PD] P09, T-P09; [CF-IE] I14, I15, T-I09; [CF-MS] T-M04 (preventiva) | Rotina testada; runbook revisado |
| T108 | **Custo e capacidade**: AWS Budgets com alerta, concorrência reservada no processador, limite de chamadas ao Bedrock | D | P2 | RNF06; [CF-IE] I16, T-I10 | Alerta de orçamento configurado; limites no template |
| T109 | **Release e rollback**: SemVer com tags por marco, `CHANGELOG.md` (Keep a Changelog), GitHub Release; Lambdas com `AutoPublishAlias`; rollback **ensaiado** das Lambdas, do frontend e do banco (com T73); implantação gradual com `DeploymentPreference` e alarme *(P2)* | D (revisão C) | P1 | [PM] seção 10.8; [CF-IE] I09, I10, I11, T-I04, T-I05, T-I06; [CF-MS] M12 | Ensaio de rollback registrado (data, passos, tempo) |
| T110 | **Demonstração reprodutível**: dados sintéticos (turma, atividades, produções em várias etapas) e instalação limpa feita por outro integrante a partir do README | D (revisão C) | *Must* | [ERS] seção 9 (fase 1); [PM] antigas T29 e T49 | Instalação limpa em até 30 min *(sugerido)* por quem não implantou antes |

## 7. Qualidade, defeitos e manutenção registrada

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T111 | **Manutenção corretiva registrada (DEF-001)**: sem a variável da API configurada, `frontend/src/api/http.ts` recorre a `/api/health`, rota que não existe na API SAM (que expõe `GET /saude`), e o teste do `TermoDeCiencia` confirma justamente esse caminho. Registrar relato, reprodução, causa, correção e teste de regressão | B (revisão A) | P1 | [CF-MS] T-M04 (corretiva), lacuna 5; [CF-IE] I24, C6, T-I14 | Ciclo completo registrado na issue e no PR |
| T112 | **Quatro manutenções registradas, uma de cada categoria**, cada uma com issue, PR, teste e nota no `CHANGELOG`: corretiva (T111), adaptativa (T66), preventiva (T107), aditiva (T83). Esta tarefa acompanha as quatro e reúne as evidências | A | P1 | [CF-MS] M01, M02, C4, T-M04 | Quatro registros fechados e ligados entre si |
| T113 | **Métricas antes e depois**: cobertura (`coverage.py`, `vitest --coverage`), complexidade (`radon`, regra `complexity` do ESLint), duplicação, avisos de lint, defeitos por módulo e tempo de abertura a fechamento de cada DEF e MUD | A (revisão D) | P2 | [CF-MS] M06, T-M06; [CF-IE] I21, C5, T-I15 | Relatório com as duas medições |
| T114 | **Dívida técnica**: `docs/manutencao/divida-tecnica.md` a partir das limitações do [INF], com custo estimado e prioridade | A e D | P2 | [CF-MS] M07, T-M07; [CF-IE] I22 | Cada item com custo, prioridade e responsável |
| T115 | **Segurança e privacidade**: itens selecionados do ASVS, LGPD, permissões IAM mínimas, inspeção do que vai ao Bedrock, confirmação de que o modelo não treina com os dados; varredura de dependências (Dependabot, `pip-audit`, `npm audit`) e checklist de segurança no PR | A (revisão D) | *Must* / P1 | RNF01–RNF04; [PM] antiga T32; [CF-MS] M19 | Nenhum item crítico aberto sem plano; varredura no CI |
| T116 | **Usabilidade e acessibilidade**: WCAG 2.1 AA (axe e verificação manual), linguagem simples, Chrome, Firefox e Edge; textos da interface em arquivo de mensagens `pt-BR.json` *(P3)* | B (revisão A) | *Must* | RNF10–RNF13; [CF-IE] I31, T-I18 | Nenhuma falha A/AA nas telas principais |
| T117 | **Sustentação e descarte**: plano de sustentação (suporte, canais, SLA por severidade, dados operacionais, critério de descontinuação); política de retenção e procedimento de exclusão de dados do aluno em todas as versões do S3, no DynamoDB e no PostgreSQL; remoção da stack | A e D | P2 | RNF01; [CF-MS] C1, M20, T-M09, T-M11; [CF-PD] T-P12 | Documento revisado; exclusão testada com dados sintéticos |
| T118 | **ETL das métricas da POC**: extrair versões por produção, uso do assistente e colagens para CSV ou esquema analítico, alimentando a ficha de indicadores da T121 | D | P3 | [ERS] seção 8; [CF-PD] P06, T-P11 | Extração roda sobre os dados de demonstração |
| T119 | **Leis de Lehman aplicadas ao projeto**: crescimento de escopo da ERS v1 para a v2 e aumento de complexidade com a arquitetura assíncrona | A | P3 | [CF-MS] M03, T-M10 | Parágrafo no plano v1.3 ou no relatório final |
| T120 | **Reflexão**, só se houver uso justificado (por exemplo, escolher a implementação do `Analisador` por nome configurado) | C | P3 | [CF-IE] I30, T-I19 | Uso documentado, ou decisão registrada de não usar |

## 8. Encerramento

| ID | Tarefa | Área | Prio | Requisitos e conformidade | Pronto quando |
|---|---|---|---|---|---|
| T121 | **Ficha de indicadores e protocolo do piloto**: fórmula e fonte de cada métrica da ERS; protocolo com uma turma e pelo menos 3 atividades *(sugerido)*, termo, consentimento, retenção e pseudonimização | A (revisão D) | *Must* | [ERS] seções 8 e 9; RNF01, RNF02; [PM] antigas T30 e T41; [DEC] B11 | Protocolo aprovado pelo professor |
| T122 | **Regressão, correções e liberação**: regressão completa, correção de defeitos por área, teste de aceitação final ponta a ponta e parecer de liberação | Todos | *Must* | [PM] seções 9.6 e 13; antigas T40, T50, T53, T55, T57 | Nenhum defeito bloqueante ou alto aberto; parecer assinado |
| T123 | **Documentação final**: arquitetura como implementada (diagrama atualizado, ADRs, contrato da API), manual do estudante e do professor, relatório final de qualidade e rastreabilidade, declaração de uso de IA | A, B e C | *Must* | [PM] seção 11 e Apêndice D; antigas T51, T52, T54, T56; [CF-MS] M15 | Coerência entre código e documentos conferida por outra área |
| T124 | **Release v1.0.0 e ensaio da demonstração** | Todos | *Must* | [PM] antigas T58 e T59; [CF-IE] I09 | Tag, notas e backup publicados; roteiro executado sem falhas |

## 9. Índice reverso: conformidade → tarefa

**Manutenção de Software** ([CF-MS])

| Item | Tarefa | Item | Tarefa |
|---|---|---|---|
| T-M01 | T68 | T-M07 | T114 |
| T-M02 | T68 | T-M08 | T70 |
| T-M03 | T66 | T-M09 | T117 |
| T-M04 | T112 (T111, T66, T107, T83) | T-M10 | T119 |
| T-M05 | T72 | T-M11 | T117 |
| T-M06 | T113 | | |

**Software para Persistência de Dados** ([CF-PD])

| Item | Tarefa | Item | Tarefa |
|---|---|---|---|
| T-P00 | T66 | T-P07 | T74 |
| T-P01 | T75 | T-P08 | T78, T79 |
| T-P02 | T75 | T-P09 | T107 |
| T-P03 | T75 | T-P10 | T73 |
| T-P04 | T76 | T-P11 | T118 |
| T-P05 | T73 | T-P12 | T117 |
| T-P06 | T74 | | |

**Implantação e Entrega de Software** ([CF-IE])

| Item | Tarefa | Item | Tarefa |
|---|---|---|---|
| T-I01 | T69 | T-I11 | T106 |
| T-I02 | T105 | T-I12 | T69 |
| T-I03 | T104 | T-I13 | T87 |
| T-I04 | T109 | T-I14 | T111 |
| T-I05 | T109 | T-I15 | T113 |
| T-I06 | T109 | T-I16 | T92 |
| T-I07 | T105 | T-I17 | T106 |
| T-I08 | T106 | T-I18 | T116 |
| T-I09 | T107 | T-I19 | T120 |
| T-I10 | T108 | | |

## 10. Tarefas do plano v1.2

| Situação | Tarefas |
|---|---|
| Concluídas | T05 (protótipo, a integrar em T67), T06 (esqueleto do frontend) |
| Concluídas em parte | T07 (Bedrock escolhido sem a comparação entre provedores; ADR-006 em T67), T08 (diagrama AWS; ADRs em T66 e T75), T09 (modelo e contrato em [DES]; migração em T74), T10 (repositório sem CI; resto em T68 e T69) |
| Absorvidas por este backlog | T01 → T70 · T02 → T71 · T03, T11, T13, T22 → T72 · T04 → T69 e T72 · T12, T21, T31, T39 → T81, T88, T95, T100 · T14–T19 → T77–T87 · T20 → T94 · T23–T28 → T89–T93 e T84 · T29, T49 → T110 · T30, T41 → T121 · T32 → T115 · T33–T37 → T86, T96–T99 · T42, T45, T47 → T101–T102 · T43 → T116 · T46 → T108 e T94 · T48 → T69 · T40, T50, T53, T55, T57 → T122 · T51, T52, T54, T56 → T123 · T58, T59 → T124 · T60, T61, T63 → T85, T87, T96 · T64 → T103 · T65 → T99 |
| Superadas pela arquitetura | Partes Java/Spring (JPA, Flyway, Spring Security, Spring AI, Docker Compose, ArchUnit) das tarefas acima, a menos que T66 escolha a opção 2 |

## 11. Uso de IA

Backlog redigido com apoio de IA (Claude Code, Claude Opus 5.5) a partir do repositório, da ERS v2, do plano mestre v1.2, do design de 19/11/2026 e dos três documentos de conformidade. Áreas, prioridades e critérios de pronto são proposta e devem ser revisados pela equipe antes de virar issues.
