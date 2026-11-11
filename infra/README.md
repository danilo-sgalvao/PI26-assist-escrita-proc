# Arquitetura assíncrona AWS SAM

Versão: 0.2 · Data: 11/11/2026 · Autor: equipe com apoio de IA · Revisor: pendente · Estado: implementação para avaliação

O template provisiona Cognito, REST API, WebSocket, S3 privado e versionado, CloudFront, SNS, SQS e DLQ, DynamoDB e cinco Lambdas Python. O PostgreSQL, sua rede e o modelo Bedrock são **pré-requisitos externos**; não são criados pela stack. O acesso direto ao PostgreSQL em Python foi autorizado pelo usuário e diverge da exigência Java dos documentos anteriores: a equipe deve registrar a decisão.

## Fluxo e contrato

1. `POST /v1/producoes`, protegido pelo Cognito, recebe JSON `{"texto":"...", "consentimento":true}` e retorna `202` com `id_producao` e `status`. Cada submissão cria um identificador e uma chave S3 próprios. O limite é 100.000 bytes no corpo.
2. S3 publica o evento `ObjectCreated` no SNS e o SQS entrega ao processador. Ele valida bucket, chave e versão, consulta o proprietário no PostgreSQL e lê a **versão exata** no S3.
3. Para evitar enviar a redação ou identificadores ao modelo, a função calcula somente quantidades de palavras, frases e parágrafos. O Bedrock recebe essas métricas e retorna códigos de uma lista fechada; a aplicação só exibe orientações fixas. O mecanismo oferece orientação estrutural genérica, não revisão semântica nem diagnóstico ortográfico.
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

## Validar e implantar

```powershell
python -m unittest discover -s infra/tests -v
sam validate --lint --template-file infra/template.yaml --region <regiao>
sam build --template-file infra/template.yaml --use-container
sam deploy --guided
```

Informe no deploy `DatabaseHost`, `DatabaseName`, `DatabaseUser`, `DatabaseUserArn`, `PrivateSubnets`, `LambdaSecurityGroups` e `BedrockModelArn`. Use nome de stack curto em minúsculas: ele integra o nome global do bucket. O deploy cria recursos cobrados. As saídas apresentam URLs, pool e cliente Cognito e nomes dos recursos. Publique a SPA no bucket de frontend; CloudFront usa Origin Access Control. Route 53 e domínio próprio não estão configurados.

Os testes locais usam dublês dos serviços e não substituem teste integrado na conta AWS. Faça o primeiro teste com dados sintéticos: conexão, POST, recebimento do evento, GET autorizado e recusa de acesso por outro usuário. Revise permissões IAM, observabilidade e custos antes de uso real.

## Limitações operacionais

S3 e PostgreSQL não formam transação distribuída. Se o upload falhar ou o resultado da chamada for ambíguo, pode sobrar registro em `PROCESSANDO` sem resposta 202 ao cliente; é necessária uma rotina de reconciliação. Eventos e chamadas podem ser repetidos, as notificações não têm garantia de entrega após desconexão, e os resultados continuam disponíveis via GET. A DLQ precisa de monitoramento e procedimento de reprocessamento. A migração SQL não é executada automaticamente. Não há endpoint de CRUD de turmas nem agrupamento de versões de uma mesma produção neste incremento.

Buckets e tabela são retidos quando a stack é excluída ou substituída. A retenção e o versionamento não implementam por si só imutabilidade legal, política de retenção de dados ou backup do PostgreSQL.
