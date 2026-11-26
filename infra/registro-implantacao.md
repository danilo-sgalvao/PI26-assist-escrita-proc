# Registro de implantação na AWS

Versão: 0.2 · Data: 26/11/2026 · Autor: Danilo Galvão, com apoio de IA · Revisor: pendente · Estado: primeiro deploy feito e recursos removidos; teste ponta a ponta pendente

Este arquivo registra cada implantação e cada teste feitos na conta AWS do projeto: o que foi feito, como, com que resultado e com que evidência. O passo a passo para repetir está no [README](README.md). Cada nova sessão entra como uma seção nova no fim, e as anteriores não são alteradas.

O repositório é público. Por isso, este registro não traz o número da conta, o endereço do banco nem os IDs e URLs dos recursos. Consulte esses valores nas saídas das stacks:

```powershell
aws cloudformation describe-stacks --stack-name entrelinhas-base --query "Stacks[0].Outputs"
aws cloudformation describe-stacks --stack-name entrelinhas --query "Stacks[0].Outputs"
```

## 26/11/2026: primeiro deploy

**Objetivo:** implantar a stack atual e testá-la com dados sintéticos antes da fatia 1. Até aqui, o código só tinha sido testado com dublês. Os riscos estavam na infraestrutura: autenticação IAM no RDS, Lambdas dentro da VPC e chamada ao Bedrock.

### Resumo

| Etapa | Resultado |
|---|---|
| 1. Stack de pré-requisitos (`entrelinhas-base`) | Criada |
| 2. Banco preparado pelo CloudShell | Tabelas e usuário da aplicação criados |
| 3. Chamada real ao Bedrock | **Defeito 1** achado e corrigido no PR #70 |
| 4. Stack da aplicação (`entrelinhas`) | Criada. **Defeito 2** achado, corrigido no PR #70 e reimplantado |
| 5. Site publicado no CloudFront | Abre a tela de entrada |
| 6. Teste ponta a ponta com dados sintéticos | **Não feito**: ficou para a próxima sessão |
| 7. Desligamento do NAT e do banco | Feito |

**Ainda não verificado na AWS:**
- as Lambdas conectando ao PostgreSQL real por IAM;
- a cadeia S3 → SNS → SQS → processador;
- o Bedrock chamado de dentro da VPC;
- a gravação no DynamoDB;
- o aviso pelo WebSocket;
- o `GET` restrito ao dono.

São justamente os riscos que motivaram o deploy, e o teste ponta a ponta existe para cobri-los.

### Ambiente

- **Conta:** projeto AWS na nova experiência (plano gratuito com créditos), com uma única região, **us-east-2**. Todos os recursos regionais ficam nela; o CloudFront é global.
- **Ferramentas:**
  - AWS CLI 2.42.4 e SAM CLI 1.174.1;
  - Docker Desktop, para o `sam build --use-container` e para os testes;
  - na máquina, Node 22.14. Ele não basta para os testes do frontend (ver "Problemas e observações").
- **Código implantado:**
  - pré-requisitos: branch `feat/infra-pre-requisitos-aws` (commit `84dba1f`);
  - aplicação: branch `fix/processador-tool-use` (PR #70, commits `ac18aab` e `e9ec777`), ainda fora da `main`.

### 1. Pré-requisitos (stack `entrelinhas-base`)

- **O que é:** o `infra/pre-requisitos.yaml` cria a rede, o NAT (que liga e desliga), os endpoints de S3 e DynamoDB e o PostgreSQL.
- **Parâmetros:** `NatLigado=sim`; o resto ficou no padrão (PostgreSQL 17, `db.t4g.micro`, banco `entrelinhas`, usuário `entrelinhas_app`).
- **Como:**
  - `sam validate --lint` sem erros;
  - change set gerado e revisado antes de criar: 22 recursos a adicionar.
- **Resultado:** `CREATE_COMPLETE`, com o PostgreSQL na versão 17.9.
- **Lacuna:** a verificação de segurança com `cfn-guard` não foi rodada, porque a ferramenta não estava instalada. No lugar dela, foi feita uma revisão manual.

### 2. Banco (CloudShell em VPC)

- **Por que o CloudShell:** o banco não tem acesso público. Por isso, a migração roda num ambiente CloudShell em VPC:
  - fica numa sub-rede privada, com o security group `GrupoAdministracao`;
  - a saída para a internet passa pelo NAT, para clonar o repositório e instalar o `psql`.
- **Comandos:**

  ```bash
  aws cloudformation wait stack-create-complete --stack-name entrelinhas-base
  git clone -q -b feat/infra-pre-requisitos-aws https://github.com/danilo-sgalvao/PI26-assist-escrita-proc.git
  bash PI26-assist-escrita-proc/infra/scripts/preparar-banco.sh entrelinhas-base
  ```

- **Resultado:**

  ```text
  Aplicando 001_inicial.sql
  Configurando o usuário da aplicação entrelinhas_app
   Schema |   Name   | Type  |          Access privileges
  --------+----------+-------+--------------------------------------
   public | conexoes | table | administrador=arwdDxtm/administrador+
          |          |       | entrelinhas_app=arwd/administrador
   public | revisoes | table | administrador=arwdDxtm/administrador+
          |          |       | entrelinhas_app=arw/administrador
  ```

- **Leitura:**
  - em `conexoes`, o usuário da aplicação lê, grava, altera e apaga (`arwd`). Precisa apagar porque a conexão do WebSocket é removida quando o aluno sai;
  - em `revisoes`, não pode apagar (`arw`): a RN04 é garantida pelo próprio banco.

### 3. Chamada real ao Bedrock (antes do deploy da aplicação)

- **Por que:** o processador só tinha sido testado com dublês.
- **Modelo:** `amazon.nova-lite-v1:0`. É o único modelo de texto da Amazon com chamada direta (*on-demand*) em us-east-2.
- **Como:** chamadas à API Converse com o mesmo prompt do código, enviando só as contagens de palavras, frases e parágrafos.
- **Defeito 1, achado:** 3 respostas inválidas em 3. O modelo devolvia as contagens num bloco de código JSON, nunca os códigos do catálogo. Com o código de então, **todas** as mensagens iriam para a DLQ.
- **Correção (PR #70, `ac18aab`):**
  - a chamada passou a usar *tool use* forçado: uma única ferramenta, cujo esquema só aceita de 1 a 3 códigos de `ESTRUTURA | PARAGRAFOS | FRASES | REVISAO`;
  - a validação no código continua sendo a garantia.
- **Mesmo teste com a correção:** 4 respostas válidas em 4, com cerca de 620 tokens de entrada por chamada.
- **Testes:** 11 de 11 no container `public.ecr.aws/sam/build-python3.12`, inclusive o integrado contra um PostgreSQL 17 descartável.

### 4. Aplicação (stack `entrelinhas`)

- **Como:**
  - `sam build --template-file infra/template.yaml --use-container`;
  - em seguida, `sam deploy` com `--resolve-s3 --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --tags projeto=entrelinhas`.
- **Parâmetros:**
  - `DatabaseHost`, `DatabaseName`, `DatabaseUser`, `DatabaseUserArn`, `PrivateSubnets` e `LambdaSecurityGroups` vêm das saídas da `entrelinhas-base`, que têm os mesmos nomes;
  - `BedrockModelArn` = `arn:aws:bedrock:us-east-2::foundation-model/amazon.nova-lite-v1:0`.
- **Resultado:** `CREATE_COMPLETE`, com 39 recursos. As quatro Lambdas na VPC (`ingestao`, `consulta`, `conexao_websocket` e `processador_bedrock`) ficaram nas duas sub-redes privadas, com o security group `GrupoLambdas`.
- **Defeito 2, achado com `curl` depois do deploy:** a API REST só tinha `/saude`.
  - `GET /v1/saude` → 401;
  - `POST /v1/producoes` → 403 `MissingAuthenticationTokenException` (a rota não existia).
- **Causa:**
  - com `DefinitionBody` na `ApiRest`, o SAM só junta os eventos `Api` das funções se `MergeDefinitions` for `true`, e o padrão é `false`;
  - o `DefaultAuthorizer: Cognito` anulava o `security: []` da `/saude`, que o frontend chama sem token.
- **Correção (PR #70, `e9ec777`):**
  - `MergeDefinitions: true`;
  - nenhum autorizador padrão;
  - `Auth: {Authorizer: Cognito}` nos eventos `Submissao` e `Consulta`.

  Antes de aplicar, o template foi traduzido na máquina pelo `samtranslator`, que mostrou as rotas e a autenticação esperadas.
- **Reimplantação:**
  - `sam deploy --no-execute-changeset` gerou a lista de mudanças;
  - a lista só alterava a `ApiRest` (sem substituição) e o estágio `v1`, e trocava o `Deployment`;
  - depois da revisão, ela foi executada: `UPDATE_COMPLETE`.
- **Depois da correção:**

  | Chamada | Resposta |
  |---|---|
  | `GET /v1/saude` | 200, com `Access-Control-Allow-Origin` do CloudFront |
  | `POST /v1/producoes` sem token ou com token falso | 401 |
  | `GET /v1/producoes/{id}` sem token | 401 |
  | `OPTIONS /v1/producoes` (pré-voo CORS) | 200, com os cabeçalhos CORS |

### 5. Site (SPA)

- **Build:** `npm ci` e `npm run build` em `frontend/`, com os valores das saídas da `entrelinhas`:

  | Variável | Saída |
  |---|---|
  | `VITE_API_URL` | `UrlRest` |
  | `VITE_WEBSOCKET_URL` | `UrlWebSocket` |
  | `VITE_COGNITO_CLIENT_ID` | `CognitoClientId` |
  | `VITE_COGNITO_REGION` | `us-east-2` |

  Os valores foram passados como variáveis de ambiente, sem criar arquivo `.env` no repositório. Eles são públicos dentro do site.
- **Testes:** 7 de 7 no container `node:22` (Node 22.23.5).
- **Envio:** 4 arquivos para o bucket `BucketFrontend`, cada um com o tipo do arquivo e uma regra de cache:
  - `index.html` com `no-cache`, para que uma publicação nova apareça na hora;
  - `assets/*` com `max-age=31536000, immutable`, porque o nome muda a cada build;
  - `favicon.svg` com cache de 1 dia.

  O envio usou URLs pré-assinadas geradas pelo AWS MCP. O equivalente em AWS CLI está no README.
- **Cache:** invalidação `/*` no CloudFront, concluída.
- **Verificação:** pelo CloudFront, `/`, `/termo-de-ciencia` e os arquivos de `assets/` respondem 200 com o tipo certo, e o título é "Entrelinhas — Assistente de Escrita".

### 6. Desligamento ao fim da sessão

- **NAT:**
  - change set da `entrelinhas-base` só com `NatLigado=nao`, que remove 3 recursos: o NAT, o IP público e a rota de saída;
  - executado: `UPDATE_COMPLETE`, com o NAT apagado e o IP liberado.
- **Banco:** `stop-db-instance`. Um RDS parado volta a ligar sozinho depois de 7 dias.
- **O que continua cobrando com tudo desligado:**
  - o disco e os backups do RDS;
  - o segredo do Secrets Manager;
  - os logs.

  Lambdas, API Gateway, SQS, SNS e DynamoDB cobram por uso e ficam praticamente em zero parados. As estimativas de custo estão no README.

### Problemas e observações

- **Node da máquina abaixo do exigido:** o projeto pede Node 22.22.2 ou mais novo, e o jsdom 31 não sobe abaixo disso. Com o 22.14, o Vitest falha ao iniciar (`Failed to start forks worker`). O build funciona. Para testar sem atualizar o Node:

  ```powershell
  # na raiz do repositório; o volume /app/node_modules isola as dependências do Linux
  docker run --rm -v "${PWD}\frontend:/app" -v /app/node_modules -w /app node:22 sh -c "npm ci && npx vitest run"
  ```

- **Lint do frontend:** 1 erro antigo, só em teste (`_url` sem uso em `src/api/revisoes.test.ts:30`). Não foi corrigido.
- **Rotas inexistentes:** endereços que não existem no site devolvem um 403 em XML do S3 em vez de uma página "não encontrada". A função `RotasFrontend` só redireciona `/termo-de-ciencia` para o `index.html`; é o comportamento atual do template.
- **Testes da infra sem `boto3` e `psycopg` na máquina:** rode-os no container do SAM:

  ```powershell
  docker run --rm -v "${PWD}:/repo:ro" -w /repo public.ecr.aws/sam/build-python3.12:latest-x86_64 bash -c "pip install -q -r infra/lambdas/requirements.txt && python -m unittest discover -s infra/tests -v"
  ```

- **Cognito:** o pool só aceita usuários criados pelo administrador. Até o fim da sessão, nenhum usuário tinha sido criado.

### Pendências para a próxima sessão

1. Religar o NAT (`NatLigado=sim`) e o banco (`start-db-instance`), o que leva cerca de 10 minutos.
2. Teste ponta a ponta com dados sintéticos:
   - criar dois alunos fictícios no Cognito, com e-mails `@example.com` e sem envio de e-mail;
   - com o aluno A: conectar ao WebSocket, enviar uma redação inventada e medir o tempo até o aviso (latência do evento do S3, decisão D2);
   - ainda com o aluno A, consultar o resultado;
   - confirmar que o aluno B recebe 404 ao tentar ler a redação de A.
3. Conferir que a DLQ está vazia e que os logs das Lambdas não têm erros.
4. Desligar o NAT e o banco de novo.
5. Integrar o PR #70 e o PR desta branch. Depois disso, implantar sempre a partir da `main`.

### Uso de IA

As implantações, os diagnósticos, as correções e este registro foram feitos com Claude Code (Claude Opus 5.5) a pedido de Danilo Galvão, que aprovou cada passo que criava ou alterava recursos na AWS. A revisão é da equipe.

## 26/11/2026: remoção de todos os recursos

**Decisão:** como não haveria teste na mesma noite, Danilo optou por apagar tudo em vez de deixar desligado. Recriar só custa tempo (cerca de 30 minutos) e a repetição do passo do CloudShell.

**Antes de apagar, foi confirmado que não havia dados:**
- o bucket das redações e a tabela de sugestões estavam vazios;
- não havia nenhum usuário no Cognito;
- não havia nenhum grupo de logs, porque as Lambdas nunca rodaram.

### Ordem e resultado

1. **Stack `entrelinhas`:** apagada (`DELETE_COMPLETE`), sem falhas. O mais demorado foi o CloudFront, que precisa ser desativado antes de sair.
2. **Recursos guardados pelo template (`DeletionPolicy: Retain`):** apagados à mão:
   - o bucket do site, com os 4 arquivos publicados;
   - o bucket das redações, vazio;
   - a tabela de sugestões, vazia.
3. **Stack `aws-sam-cli-managed-default`:** o bucket só tinha o pacote do código e duas versões do template enviadas nos deploys. Foi esvaziado e apagado junto com a stack.
4. **Stack `entrelinhas-base`:**
   - as interfaces de rede das Lambdas já tinham sido liberadas, então não foi preciso esperar;
   - o RDS foi apagado mesmo parado, e o segredo da senha saiu junto;
   - o template gerou o snapshot final (`DeletionPolicy: Snapshot`). Como o banco não tinha dados, o snapshot foi apagado.
5. **Inventário final, em us-east-2 e em us-east-1:** não sobrou nenhum destes recursos:
   - stack, Lambda, API REST ou WebSocket;
   - fila, tópico, pool do Cognito ou tabela;
   - bucket do projeto, instância ou snapshot manual do RDS;
   - segredo, VPC fora da padrão ou IP público;
   - distribuição, função ou controle de acesso do CloudFront;
   - Web ACL ou grupo de logs.

### Para recriar

- **Passo a passo:** siga o README desde "Criar os pré-requisitos em uma conta nova".
- **Endereços e IDs:** todos mudam. Refaça o build do site com as saídas novas.
- **Pendências:** as da seção anterior continuam valendo, mas o item 1 passa a ser **recriar as duas stacks e repetir o passo do CloudShell**, em vez de religar o NAT e o banco.
- **CloudShell:** o ambiente em VPC usado no preparo do banco já não ocupava a rede. Se ainda aparecer no console, pode ser apagado, porque a VPC dele não existe mais.
