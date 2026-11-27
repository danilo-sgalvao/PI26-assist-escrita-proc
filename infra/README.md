# Arquitetura assíncrona AWS SAM

Versão: 0.3 · Data: 26/11/2026 · Autor: equipe com apoio de IA · Revisor: pendente · Estado: implementação para avaliação

O template provisiona Cognito, REST API, WebSocket, S3 privado e versionado, CloudFront, SNS, SQS e DLQ, DynamoDB e cinco Lambdas Python. O PostgreSQL, sua rede e o modelo Bedrock são **pré-requisitos externos**; não são criados pela stack. O acesso direto ao PostgreSQL em Python foi autorizado pelo usuário e diverge da exigência Java dos documentos anteriores: a equipe deve registrar a decisão.

## Fluxo e contrato

1. `POST /v1/producoes`, protegido pelo Cognito, recebe JSON `{"texto":"...", "consentimento":true}` e retorna `202` com `id_producao` e `status`. Cada submissão cria um identificador e uma chave S3 próprios. O limite é 100.000 bytes no corpo.
2. S3 publica o evento `ObjectCreated` no SNS e o SQS entrega ao processador. Ele valida bucket, chave e versão, consulta o proprietário no PostgreSQL e lê a **versão exata** no S3.
3. Para evitar enviar a redação ou identificadores ao modelo, a função calcula somente quantidades de palavras, frases e parágrafos. O Bedrock recebe essas métricas e retorna códigos de uma lista fechada, preenchendo uma ferramenta obrigatória (*tool use*) cujo esquema só aceita esses códigos; a aplicação valida a resposta e só exibe orientações fixas. O mecanismo oferece orientação estrutural genérica, não revisão semântica nem diagnóstico ortográfico.
4. O processador grava o resultado condicionalmente no DynamoDB, marca a revisão como concluída e notifica as conexões do aluno. Reentregas são idempotentes quanto ao resultado; a notificação pode ser duplicada, e clientes devem tolerá-la.
5. O cliente consulta `GET /v1/producoes/{id}` com token Cognito. A consulta só retorna a revisão ao dono; o resultado inclui status e sugestões.

O WebSocket usa `wss://.../v1?token=<access-token>`. O autorizador valida o access token pelo Cognito, seu pool e cliente; `$connect` registra a identidade e `$disconnect` remove o ID. Evite registrar URLs ou tokens em logs; faça reconexão após expiração ou desconexão. Conexões antigas também são removidas ao receber `GoneException`.

## Pré-requisitos

- SAM CLI e Docker para construir a dependência nativa `psycopg[binary]` para Linux; AWS CLI autenticada e permissões CloudFormation/IAM.
- Instância ou cluster PostgreSQL privado existente, com TLS, autenticação IAM habilitada, usuário de banco com `rds_iam` e permissões para ler/escrever nas tabelas. Consulte o [procedimento de autenticação IAM do RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html).
- Execute `infra/migrations/001_inicial.sql` uma vez usando um usuário de migração autorizado. A migração cria `revisoes` e `conexoes`; conceda ao usuário IAM da aplicação os privilégios SQL necessários.
- Sub-redes e security groups que alcancem o PostgreSQL e os serviços S3, SQS, DynamoDB, Bedrock Runtime, Cognito e API Gateway Management por endpoints VPC ou NAT. Verifique DNS, rotas e regras de saída.
- ARN `rds-db:connect` do usuário, obtido com o **resource ID** do banco/cluster e o nome do usuário, e ARN de modelo Bedrock com Converse disponível e autorizado na região. Para perfis de inferência podem ser necessárias permissões adicionais e verificação da residência dos dados.
- Confirme o termo de ciência e as salvaguardas do projeto antes de usar dados reais. A validação de catálogo impede exibir saída livre, mas ainda não substitui avaliação pedagógica adversarial.

O bundle público de certificados RDS foi obtido da [AWS](https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem); revise sua atualização conforme a rotação de certificados.

### Criar os pré-requisitos em uma conta nova

O `infra/pre-requisitos.yaml` cria:

- a VPC, com duas sub-redes privadas e uma pública;
- o NAT Gateway, controlado pelo parâmetro `NatLigado`;
- endpoints gratuitos de S3 e DynamoDB;
- um PostgreSQL `db.t4g.micro`, sem Multi-AZ e com autenticação IAM. A senha do usuário de migração fica no Secrets Manager, gerida pelo RDS.

As saídas têm o mesmo nome dos parâmetros do `template.yaml`.

```powershell
aws cloudformation deploy --stack-name entrelinhas-base --template-file infra/pre-requisitos.yaml
aws cloudformation describe-stacks --stack-name entrelinhas-base --query "Stacks[0].Outputs"
```

O banco é privado. A migração e o usuário da aplicação são aplicados pelo AWS CloudShell em ambiente VPC:

1. Crie o ambiente com a VPC `Rede`, uma das sub-redes privadas e o security group `GrupoAdministracao`.
2. Clone o repositório no CloudShell.
3. Rode `bash infra/scripts/preparar-banco.sh entrelinhas-base`.

O ambiente sai para a internet pelo NAT, para clonar o repositório e instalar o `psql`. Por isso, rode esse passo com `NatLigado=sim`.

O script aplica `infra/migrations/*.sql` em ordem. Elas precisam ser idempotentes, porque ainda não há registro de quais migrações já rodaram. Em seguida, cria o usuário IAM com `SELECT`, `INSERT` e `UPDATE`, e concede `DELETE` só em `conexoes` (RN04).

Os custos são aproximados, em us-east-2:

- NAT Gateway com IP público: cerca de US$ 1,20 por dia ligado, mais o tráfego;
- RDS: cerca de US$ 15 por mês, somando instância, 20 GB gp3 e o segredo.

Para economizar entre as sessões de teste:

```powershell
aws cloudformation deploy --stack-name entrelinhas-base --template-file infra/pre-requisitos.yaml --parameter-overrides NatLigado=nao
aws rds stop-db-instance --db-instance-identifier entrelinhas-base-postgres
```

Sem NAT, a ingestão e a consulta continuam funcionando. O processador, porém, não alcança o Bedrock nem o WebSocket, e as mensagens vão para a DLQ. Um RDS parado volta a ligar sozinho depois de 7 dias.

Para remover tudo:
1. **Stack da aplicação:** apague-a primeiro. Os dois buckets e a tabela ficam guardados (`DeletionPolicy: Retain`). Confira se há dados, esvazie os buckets, incluindo as versões antigas, e apague-os à mão junto com a tabela.
2. **Stack de pré-requisitos:** apague-a depois. As Lambdas mantêm interfaces de rede nas sub-redes por alguns minutos, e a remoção da rede espera por elas. O RDS deixa um snapshot final, que é cobrado até ser apagado.
3. **Stack `aws-sam-cli-managed-default`:** o `sam deploy --resolve-s3` a cria para guardar os pacotes do deploy. Ela pode ser apagada depois de esvaziar o bucket, e o próximo deploy a recria.

## Validar e implantar

O que já foi implantado e testado na conta do projeto, com os resultados, está no [registro de implantação](registro-implantacao.md).

```powershell
python -m unittest discover -s infra/tests -v
sam validate --lint --template-file infra/template.yaml --region <regiao>
sam build --template-file infra/template.yaml --use-container
sam deploy --guided
```

Informe no deploy `DatabaseHost`, `DatabaseName`, `DatabaseUser`, `DatabaseUserArn`, `PrivateSubnets`, `LambdaSecurityGroups` e `BedrockModelArn`. Use nome de stack curto em minúsculas: ele integra o nome global do bucket. O deploy cria recursos cobrados. As saídas apresentam URLs, pool e cliente Cognito e nomes dos recursos. Publique a SPA no bucket de frontend; CloudFront usa Origin Access Control. Route 53 e domínio próprio não estão configurados.

### Atualizar uma stack que já existe

Gere a lista de mudanças sem aplicar e confira:
- que nenhum recurso de dados aparece com substituição (`Replacement: True`). São recursos de dados os buckets, a tabela, o Cognito e o RDS;
- que nada é removido sem querer.

Só então execute a lista.

```powershell
sam deploy --no-execute-changeset <mesmas opções do deploy anterior>
aws cloudformation execute-change-set --change-set-name <ARN mostrado pelo sam deploy>
```

### Publicar o site

Em `frontend/`, preencha o `.env.local` com as saídas da stack (ver `frontend/README.md`) e rode `npm ci` e `npm run build`. Depois, envie os arquivos.

```powershell
$bucket = aws cloudformation describe-stacks --stack-name entrelinhas --query "Stacks[0].Outputs[?OutputKey=='BucketFrontend'].OutputValue" --output text
$distribuicao = aws cloudformation describe-stack-resource --stack-name entrelinhas --logical-resource-id DistribuicaoFrontend --query "StackResourceDetail.PhysicalResourceId" --output text
aws s3 cp frontend/dist/assets "s3://$bucket/assets" --recursive --exclude "*" --include "*.js" --content-type "text/javascript; charset=utf-8" --cache-control "public, max-age=31536000, immutable"
aws s3 cp frontend/dist/assets "s3://$bucket/assets" --recursive --exclude "*" --include "*.css" --content-type "text/css; charset=utf-8" --cache-control "public, max-age=31536000, immutable"
aws s3 cp frontend/dist/favicon.svg "s3://$bucket/favicon.svg" --content-type "image/svg+xml" --cache-control "public, max-age=86400"
aws s3 cp frontend/dist/index.html "s3://$bucket/index.html" --content-type "text/html; charset=utf-8" --cache-control "no-cache"
aws cloudfront create-invalidation --distribution-id $distribuicao --paths "/*"
```

- **Tipo de cada arquivo:** é informado explicitamente porque, no Windows, a CLI pode adivinhar um tipo errado para `.js`. O navegador recusa um script de módulo com tipo errado.
- **Ordem:** o `index.html` vai por último, para nunca apontar para arquivos que ainda não chegaram.
- **Cache:** o `index.html` não fica em cache, enquanto os arquivos de `assets/` mudam de nome a cada build.

Os testes locais usam dublês dos serviços e não substituem teste integrado na conta AWS. Faça o primeiro teste com dados sintéticos: conexão, POST, recebimento do evento, GET autorizado e recusa de acesso por outro usuário. Revise permissões IAM, observabilidade e custos antes de uso real.

## Limitações operacionais

S3 e PostgreSQL não formam transação distribuída. Se o upload falhar ou o resultado da chamada for ambíguo, pode sobrar registro em `PROCESSANDO` sem resposta 202 ao cliente; é necessária uma rotina de reconciliação. Eventos e chamadas podem ser repetidos, as notificações não têm garantia de entrega após desconexão, e os resultados continuam disponíveis via GET. A DLQ precisa de monitoramento e procedimento de reprocessamento. A migração SQL não é executada automaticamente. Não há endpoint de CRUD de turmas nem agrupamento de versões de uma mesma produção neste incremento.

Buckets e tabela são retidos quando a stack é excluída ou substituída. A retenção e o versionamento não implementam por si só imutabilidade legal, política de retenção de dados ou backup do PostgreSQL.
