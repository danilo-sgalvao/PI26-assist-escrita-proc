# ADR-006 Acesso ao modelo pelo AWS Bedrock

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data | 30/10/2026 |
| Autor | Preparado com apoio de IA (Codex) |
| Revisor | A definir |
| Estado | Proposto; validação do experimento pendente |

## Contexto e decisão

O usuário definiu AWS Bedrock como serviço de IA para o backend. O modelo, a região e o mecanismo de integração definitivo permanecem em avaliação. A prova técnica isolada utiliza AWS SDK para Java 2 e a API Converse; Spring AI permanece alternativa para o adaptador definitivo na etapa 3. O experimento usa exclusivamente um prompt sintético fixo e não expõe endpoint HTTP.

## Resultado do spike nesta máquina

Em 30/10/2026 não foram encontrados `AWS_REGION`, `BEDROCK_MODEL_ID`, `AWS_PROFILE`, `AWS_ACCESS_KEY_ID`, `AWS_WEB_IDENTITY_TOKEN_FILE` nem arquivos locais padrão de configuração/credenciais AWS. Não foi feita chamada real: acesso, modelos disponíveis, latência, qualidade e custo não foram medidos. Responsável pelo desbloqueio: equipe do projeto, a definir.

Após configurar credenciais apropriadas, região e modelo, executar o procedimento de [backend/README.md](../../backend/README.md). Registrar modelo, região, disponibilidade, custo, tokens, latência, qualidade e termos de tratamento de dados; comparar opções antes de aceitar este ADR. Observar processamento entre regiões e registros de invocação na configuração escolhida. Não usar dados reais até a avaliação de privacidade e os consentimentos necessários.

## Segurança e limitações

O SDK usa a cadeia padrão de credenciais; preferir credenciais temporárias e permissões mínimas para invocação. Configurar orçamento e monitoramento na conta AWS. O resultado do experimento não é implementação do assistente pedagógico: classificação, validação de saída e controle de autoria pertencem à etapa 3.

Referências: [AWS — Converse API](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html); [AWS SDK para Java — exemplos Bedrock](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/java_bedrock-runtime_code_examples.html).
