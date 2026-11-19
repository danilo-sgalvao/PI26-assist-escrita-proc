# Assistente de Escrita Processual — Grupo 8

Trabalho da disciplina **Manutenção de Software** (UFG, 6º semestre). Prova de conceito (POC 2.2) de uma plataforma em que o estudante escreve o próprio texto e uma IA **orienta sem escrever**, enquanto o professor acompanha o processo (versões, interações, evolução).

**Equipe:** Danilo Galvão, Enzo Machado, Felipe Nunes, Luiz Augusto Godinho.
**Idioma:** todo o conteúdo (documentos, código, commits, issues) é em português do Brasil.

## Estrutura do repositório

Monorepo com três pastas:
- `frontend/`: SPA em React + TypeScript (nome de produto na interface: "Entrelinhas");
- `infra/`: template AWS SAM, Lambdas em Python, migração SQL e testes;
- `docs/`: documentos do projeto.

Não existe pasta `backend/`: o backend Java/Spring Boot foi removido do `main` em 11/11/2026. Também não existe `.github/` (sem CI por enquanto).

Organização de `docs/`:
- `referencias/`: material externo ou apresentado, somente leitura;
- `ers/`: uma subpasta por versão da ERS;
- `plano/`: uma subpasta por versão do plano.

Versões antigas não são apagadas nem sobrescritas.

| Arquivo | O que é | Situação |
|---|---|---|
| `docs/arquitetura-aluno-processamento.png` | Diagrama da arquitetura AWS (fluxo do aluno e processamento assíncrono) | **Arquitetura vigente** |
| `infra/README.md` | Fluxo, contrato da API, pré-requisitos, deploy e limitações operacionais | Descreve a implementação atual |
| `infra/template.yaml` | Template AWS SAM com todos os recursos da stack | Fonte da infraestrutura |
| `frontend/README.md` | Execução do frontend, variáveis `VITE_*` e contrato utilizado | Descreve a implementação atual |
| `docs/arquitetura/modelo-de-dados-e-api.md` | Design: modelo de dados, contrato da API, fluxo do apoio e fatias de implementação | Aceito como base em 19/11/2026, aberto a mudanças; decisões D1–D5 tomadas em 19/11/2026 (seção 8): texto entra e saída fechada em catálogo, gatilho em `pedidos/` no S3, turmas na fatia 1, tabela `Interacoes` no DynamoDB, comparação no servidor |
| `docs/referencias/POC 2.2. Assistente de escrita processual.pdf` | Enunciado da POC: risco moderado, hipótese, salvaguardas, requisitos de dados e métricas de saída | Fonte externa (não editar) |
| `docs/referencias/AssistentedeEscritaProcessual_2.pdf` | Slides apresentados ao stakeholder (linguagem não técnica) | Referência |
| `docs/ers/v1.0/ESPECIFICAÇÃO DE REQUISITOS DE SOFTWARE – ERS GRUPO 8.pdf` | ERS v1.0 original: RF01–RF15, RN01–RN06 | Superada pela v2 |
| `docs/ers/v2/ERS-Grupo8-v2.md` | ERS v2.0 revisada; **o `.md` é a fonte** | Base de requisitos; em revisão pela equipe |
| `docs/ers/v2/ERS-Grupo8-v2.docx` | Versão Word gerada a partir do `.md` (capa, sumário, A4) | Regerar sempre que o `.md` mudar |
| `docs/plano/v1.1/PDS_Assistente_Escrita_Processual_v1.1.docx` | Plano mestre v1.1 editável (Word) | Base para a v1.2; não editar |
| `docs/plano/v1.1/Plano_Mestre_Assistente_Escrita_Processual_v1.1.pdf` | PDF do plano mestre v1.1 (processo, arquitetura, stack, cronograma, qualidade, riscos) | Superado pela v1.2 |
| `docs/plano/v1.2/decisoes-plano-v1.2.md` | Decisões B1–B12 e registro das mudanças aplicadas no plano v1.2 (seção E) | B5 e B10 pendentes |
| `docs/plano/v1.2/plano-mestre-v1.2.md` | Plano mestre v1.2, enriquecido com a ERS v2; **o `.md` é a fonte** (diagramas em Mermaid) | Vale para processo, cronograma e qualidade; **arquitetura e stack superadas** pela implementação |
| `docs/plano/v1.2/plano-mestre-v1.2.docx` | Versão Word gerada a partir do `.md` (diagramas renderizados, sumário, tabelas largas em paisagem) | Regerar sempre que o `.md` mudar |

O texto da POC é curto. O documento complementar dela é https://www.gov.br/mec/pt-br/escolas-conectadas/arquivos/ia-basica.pdf.

## Hipótese e regras centrais

- **Hipótese da POC:** acompanhar a escrita por etapas desenvolve autoria e autorregulação sem gerar dependência nem plágio assistido.
- **Métricas:** qualidade da produção final, autonomia progressiva (redução do apoio solicitado ao longo das atividades) e originalidade verificada.
- **Regras que não se negociam:** a IA não escreve, não reescreve, não completa nem parafraseia o texto do aluno (RN01/RN02); o histórico de versões nunca é apagado (RN04); indicadores não viram nota, ranking ou vigilância (RN05); a similaridade apenas apoia a avaliação, e quem decide sobre originalidade é o professor (RN06).

## Fatos confirmados pela equipe (não mudar sem aprovação)

- Prazo de **6 semanas** até a entrega final; quatro integrantes.
- Frontend em **React + TypeScript**.
- Assistente baseado em **LLM acessado por API externa** (decisão B1, 29/10/2026, que substitui o "LLM local" do plano v1.1). Na implementação, o provedor é o **AWS Bedrock** (API Converse; o modelo é informado no deploy pelo parâmetro `BedrockModelArn`). A comparação prevista no spike T07 não foi feita, e o ADR-006 está no PR #2, ainda aberto. Valem três cuidados:
  - nunca enviar nome ou outros identificadores do aluno à API;
  - usar provedor que não treine com os dados;
  - o termo de ciência (RF21) informa o processamento externo.
- Persistência e acesso a dados em **Python**, nas Lambdas (`psycopg` e `boto3`), **sem Java** (decisão de Danilo em 19/11/2026). Ela substitui a exigência de Java do enunciado e do plano; falta registrá-la em ADR, como pede o `infra/README.md`.
- Similaridade (RF15) compara a produção com **textos internos** (outras produções da atividade) e com as **respostas do assistente** (decisão B2). Base externa e serviço antiplágio ficam como evolução futura (*Won't* nesta entrega), mesmo os stakeholders tendo citado produção externa.

## Arquitetura vigente (implementada)

A arquitetura e o design já iniciados no repositório são os permanentes, mesmo onde diferem do plano v1.2 (decisão informada por Danilo em 16/11/2026; falta registrá-la em ADR/MUD). O diagrama `docs/arquitetura-aluno-processamento.png` é a referência. Ela substitui o "SPA + monólito modular Spring Boot" do plano.

- **Estilo:** serverless, assíncrono e orientado a eventos, na AWS, com a infraestrutura definida em AWS SAM (`infra/template.yaml`).
- **Frontend:** SPA React 18 + TypeScript, com Vite, Vitest, Testing Library, ESLint e `wouter` para rotas; Node.js 22.22.2 ou superior. É publicada em um bucket S3 privado e entregue pelo CloudFront.
- **Autenticação:** Amazon Cognito com JWT; os usuários são criados pelo administrador. A API REST usa o autorizador Cognito (ID token no cabeçalho `Authorization`). O WebSocket usa um autorizador Lambda (access token no parâmetro `token`).
- **API:** API Gateway REST (`POST /producoes`, `GET /producoes/{id}`, `GET /saude`) e API Gateway WebSocket (`$connect`, `$disconnect`), ambas no estágio `v1`.
- **Lambdas (Python 3.12, em `infra/lambdas/`):** `ingestao`, `consulta`, `conexao_websocket`, `autorizador` e `processador_bedrock`; `comum.py` concentra a conexão com o PostgreSQL (autenticação IAM e TLS).
- **Dados:**
  - S3 versionado guarda o texto das redações (`redacoes/<id>.txt`);
  - RDS PostgreSQL guarda os metadados (`revisoes`, `conexoes`); a migração `infra/migrations/001_inicial.sql` é aplicada manualmente;
  - DynamoDB guarda as sugestões, com chave `id_producao`.
- **Fluxo:**
  1. o aluno envia o texto e recebe `202` com `id_producao`;
  2. a ingestão grava a versão no S3 e os metadados no PostgreSQL;
  3. o S3 publica o evento no SNS, que entrega à fila SQS (com DLQ);
  4. o processador consulta o Bedrock e grava as sugestões no DynamoDB;
  5. o aluno é avisado pelo WebSocket e consulta o resultado pela API REST. Sem WebSocket, o frontend consulta a cada 10 segundos.
- **Defesa da RN01/RN02:** o texto do aluno **não** é enviado ao modelo. O processador calcula apenas as quantidades de palavras, frases e parágrafos; o Bedrock devolve códigos de uma lista fechada (`ESTRUTURA`, `PARAGRAFOS`, `FRASES`, `REVISAO`); a aplicação exibe somente orientações fixas, e qualquer saída fora da lista é rejeitada. Essa validação determinística é a garantia final, não o prompt. **Decisão D1 (19/11/2026), a implementar na fatia 3:** o texto e o pedido do aluno passam a ser enviados ao modelo, mas a saída continua fechada. O Bedrock devolve só códigos de um catálogo escrito pela equipe e a localização do trecho, e o aluno só lê textos do catálogo (ver `docs/arquitetura/modelo-de-dados-e-api.md`, seção 7).
- **Versões:** cada envio gera um identificador e um objeto próprios no S3 versionado. Ainda não há agrupamento das versões de uma mesma produção, e o histórico exibido ao aluno fica só no `sessionStorage` do navegador.
- **Diferenças entre o diagrama e o código:** Route 53 e domínio próprio não estão configurados; a API REST não é um CRUD completo; "Turmas" ainda não existe na migração.

## Propostas do plano mestre (valem até virar ADR ou mudança aprovada)

Continuam valendo as propostas de processo. As de arquitetura e stack do plano v1.2 (Spring Boot, JPA, Flyway, Spring Security com sessão, Spring AI, Docker Compose) foram superadas pela seção acima.

- **Processo:** iterativo, baseado em Scrum, com sprints de 1 semana e quadro Kanban (WIP ≤ 4 em desenvolvimento e ≤ 4 em revisão). Marcos M1–M6, um por semana. Cronograma relativo (Semana 1–6, dias D1–D5), porque D0 ainda não foi definido.
- **Áreas e revisão em anel:** A = Requisitos/Produto/Qualidade (Product Owner), B = Frontend, C = Backend/API/Assistente, D = Persistência/Dados/Infra. Anel de revisão A→B→C→D→A; o autor nunca aprova o próprio trabalho. Ainda falta definir quem fica em cada área (tarefa T01).
- **Similaridade:** contenção de n-gramas de palavras (n = 5), sem veredito de plágio. Ainda não implementada; falta definir onde ela entra na arquitetura vigente.
- **Versões:** o princípio continua sendo a imutabilidade (RN04), com o progresso calculado a partir das versões. O mecanismo do plano (append-only no banco, com UPDATE/DELETE bloqueados) deu lugar ao versionamento do S3.

## Comandos

```powershell
# infra (na raiz do repositório)
python -m unittest discover -s infra/tests -v
sam validate --lint --template-file infra/template.yaml --region <regiao>
sam build --template-file infra/template.yaml --use-container
sam deploy --guided

# frontend (em frontend/)
npm ci
npm run dev
npm test
npm run lint
npm run build
```

Os testes da infra usam dublês dos serviços AWS e não substituem o teste integrado na conta. O deploy cria recursos cobrados; o PostgreSQL, a rede e o modelo Bedrock são pré-requisitos externos à stack.

## Convenções

- **IDs:**
  - RF01–RF15 e RN01–RN06 mantêm a numeração da ERS original; itens novos são acrescentados ao final da sequência.
  - Demais prefixos: HU-nn / CA-nn.m, Q-xx / H-xx, ADR-nnn, Tnn, CT-nn.m, DEF-nnn, Rnn, MUD-nnn.
  - O nome do teste cita o CA (ex.: `deveRejeitarEdicaoAposSubmissao_CA14_2`).
- **Valores numéricos ainda não validados** aparecem marcados como *(sugerido)* ou "proposta".
- **Git:**
  - monorepo `frontend/`, `infra/`, `docs/` (e `.github/` quando houver CI);
  - GitHub Flow com branches `tipo/Txx-descricao` de no máximo 2 dias e squash merge;
  - Conventional Commits em português citando a issue (`feat(apoio): valida limite de palavras (#26)`);
  - PR segue o modelo do Apêndice C do plano, com a seção "Design do incremento".
- **Segredos:** nada de chaves, senhas ou tokens no repositório. As variáveis `VITE_*` do frontend são públicas no bundle.
- **Documentos:** em Markdown, com cabeçalho de título, versão, data, autor, revisor e estado. Uso de IA é sempre declarado (Apêndice D do plano).

## Hierarquia entre os documentos

1. **Fatos confirmados pela equipe** (seção acima) valem sobre tudo.
2. **ERS v2** (`docs/ers/v2/ERS-Grupo8-v2.md`, versão 2.0) é a base de requisitos. O plano mestre **não** está acima dela. Não editar a ERS sem pedido explícito: divergências com o plano, com a implementação ou com os fatos confirmados são levadas ao grupo, não corrigidas por conta própria. A divergência conhecida hoje: o RF15 da ERS cita base externa na similaridade, mas a decisão B2 limita a similaridade a textos internos.
3. **Arquitetura e stack:** vale a implementação (seção "Arquitetura vigente", o diagrama e os READMEs de `infra/` e `frontend/`), não o plano.
4. **Plano mestre** define processo, cronograma, qualidade e riscos. Versão vigente: **plano v1.2** (`docs/plano/v1.2/plano-mestre-v1.2.md`), já enriquecido com a ERS v2. O que mudou em relação à v1.1, e por quê, está em `docs/plano/v1.2/decisoes-plano-v1.2.md`. Não reescrever a arquitetura do plano sem pedido explícito.

## Pontos de atenção

- **Lacunas da implementação em relação à ERS v2:**
  - ainda não existem o papel do professor, atividades, etapas (RF17), turmas, acompanhamento e similaridade (RF15);
  - o assistente só dá orientação estrutural genérica, a partir de contagens. Não cobre as categorias de apoio da ERS nem orienta sobre o conteúdo;
  - falta agrupar as versões de uma mesma produção e ler o histórico pelo servidor.
- **Limitações operacionais** (detalhes no `infra/README.md`): S3 e PostgreSQL não formam transação, então pode sobrar registro em `PROCESSANDO`; a DLQ precisa de monitoramento; a notificação por WebSocket pode se repetir ou se perder.
- **Tarefas e issues:** T01–T65 foram escritas e estimadas para a arquitetura anterior e precisam de revisão. Os commits de 11/11/2026 entraram direto no `main`, sem PR e sem citar issue. Os PRs #1–#3, do backend Spring e da base RAG, continuam abertos.
- O **cronograma é fixo** (B12): 6 semanas, 10 h por pessoa por semana. A v1.2 tem 151 h de tarefas (a v1.1 tinha 144 h) e 5 h de reserva. A área B (frontend) só tem 0,5 h de reserva. Nenhuma área passa de 6,5 h de tarefas por semana. Essas horas foram estimadas para a arquitetura anterior.
- **Prioridades (MoSCoW):**
  - *Must*: RF01–RF10, RF13, RF14, RF16, RF17, RF21, RF22;
  - *Should*: RF11, RF12, RF15, RF18, RF20;
  - *Could*: RF19 (tarefa T64, fora da base).
- **Ordem de corte:** RF19 → RF20 → RF11/RF12 → RF15 → destaque do RF18.
- As etapas (RF17) só aparecem na interface na Semana 4 (M4).
- **Tarefas novas:** T60, T61, T63, T64, T65. **Tarefas removidas:** T38 e T44.
- **Regerar o `.docx` do plano:** usar o conversor do Markdown com Mermaid renderizado pelo mermaid-cli (Chrome local) e atualizar o sumário no Word. Os scripts ficam no scratchpad da sessão, não no repositório.
- Divergências entre ERS v2 e plano v1.1 já decididas a favor da ERS:
  - salvamento automático + versões marcadas por etapa;
  - prazo configurável pelo professor (padrão: aceita e marca atrasada);
  - categorias de apoio dos slides + "pedido de escrita";
  - similaridade automática após a submissão.

  A priorização segue MoSCoW (Alta → Must, Média → Should, Baixa → Could; RF06 é Must). Os RNF partem dos RNF01–13 da ERS, mais RNF14–17 vindos do plano.
- Pendentes: critério do RF09 (B5) e tempo de resposta da IA (B10).
- O piloto com turma fica para depois da entrega. Nas 6 semanas, o plano entrega a demo e o protocolo do piloto.
