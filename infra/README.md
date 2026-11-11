# Fundação AWS SAM

Versão: 0.1 · Data: 11/11/2026 · Autor: equipe com apoio de IA · Revisor: pendente · Estado: inicial

Esta fundação implementa os recursos de suporte da arquitetura proposta: Cognito, API Gateway REST e WebSocket, frontend S3 privado com CloudFront, bucket versionado de redações, eventos S3 → SNS → SQS com fila de falhas, e DynamoDB. Ela **não é uma aplicação funcional**: a REST tem apenas uma rota simulada de saúde, o WebSocket não tem rotas, e não há consumidores na fila. As Lambdas em `lambdas/` validam eventos e falham de forma segura enquanto os adaptadores de persistência e IA não estão disponíveis. Ainda não estão declaradas ou conectadas no template SAM; a ingestão e o WebSocket retornam 503 e o processador sinaliza todas as mensagens para reprocessamento.

O diagrama propõe uma arquitetura diferente do plano de monólito modular existente. Sua adoção, autenticação e a escolha do Bedrock devem ser conciliadas com as decisões e requisitos do projeto. O usuário autorizou acesso direto ao PostgreSQL pelas Lambdas Python; isso diverge da exigência em Java registrada nos documentos e precisa ser reconciliado pela equipe. Nenhum modelo ou prompt está configurado: a regra de que a IA não escreve pelo estudante precisa de validação determinística e das demais defesas do projeto antes de integrar o Bedrock.

## Validar e implantar

Requisitos: AWS SAM CLI, AWS CLI autenticada, permissões CloudFormation/IAM e uma região com os serviços necessários. A implantação cria recursos cobrados; revise custos e parâmetros antes de executá-la. Use nome de stack curto, em minúsculas, pois ele integra o nome global do bucket de redações.

```powershell
sam validate --template-file infra/template.yaml
sam build --template-file infra/template.yaml
sam deploy --guided
```

Após a implantação, use as saídas da stack para configurar e publicar a SPA no bucket privado. O CloudFront usa Origin Access Control. Route 53 e domínio próprio não foram configurados; exigem uma zona hospedada e, para HTTPS com domínio próprio, certificado apropriado.

## Próximos incrementos

- Implementar as Lambdas Python e a API REST: autenticação, autorização por usuário/turma, submissão e acesso aos metadados. Configurar CORS para a origem exata da SPA e conciliar a integração com a exigência existente de acesso a dados em Java.
- Provisionar PostgreSQL/RDS em rede privada, credenciais gerenciadas, migrações e acesso Java; estabelecer o vínculo entre redação, versão e identidade sem enviar identificadores ao modelo.
- Implementar `$connect`/`$disconnect` com validação JWT e armazenamento/limpeza dos IDs; vincular as rotas ao WebSocket e aplicar autorização. A API WebSocket atual não aceita conexões úteis.
- Implementar consumidor SQS idempotente, leitura da versão correta no S3, salvaguardas de autoria, invocação Bedrock e escrita no DynamoDB; configurar concorrência, falhas parciais, visibilidade e permissão `execute-api:ManageConnections` restrita ao estágio. Até então, mensagens acumulam e expiram conforme retenção da fila.
- Implementar leitura autorizada das sugestões via REST, observabilidade e testes de integração. Reconciliar gravações de RDS e S3 e lidar com eventos duplicados ou fora de ordem.

Buckets e tabela usam políticas de retenção ao excluir ou substituir a stack; podem continuar gerando custos e exigir limpeza deliberada. O versionamento do S3 preserva versões, mas não substitui regras de imutabilidade ou backup.
