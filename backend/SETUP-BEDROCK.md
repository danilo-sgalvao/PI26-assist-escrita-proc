# Configuração da conexão com AWS Bedrock

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data | 30/10/2026 |
| Autor | Implementado com apoio de IA (Codex) |
| Revisor | A definir |
| Estado | Implementação de transporte para revisão; modelo e região pendentes |

Este guia prepara a conexão do backend Java/Spring Boot com a API Converse do AWS Bedrock. A implementação adiciona uma porta `AssistenteGateway` e um adaptador que recebe instrução e mensagem, retorna texto bruto e informa o uso de tokens. O adaptador fica desabilitado por padrão e não cria endpoint HTTP.

## Pré-requisitos

1. Integrar primeiro à `main` a branch `codex/add-fundacao-backend`, que fornece projeto Maven, AWS SDK 2, Spring Boot, testes e infraestrutura. Esta branch foi criada diretamente de `main` e contém somente os novos arquivos da conexão; isoladamente, ela não contém `pom.xml` ou Maven Wrapper.
2. Usar JDK 25 e Maven Wrapper da fundação. Configurar uma conta AWS, uma região e um modelo ou perfil de inferência com suporte à API Converse e acesso habilitado. Modelo e região precisam ser aprovados no ADR-006; não há escolha implícita neste código.
3. Provisionar uma identidade IAM com a ação `bedrock:InvokeModel` limitada aos recursos necessários. Para perfil de inferência, verificar também as permissões do perfil e dos modelos e regiões de destino. A primeira ativação de certos modelos pode exigir permissões do AWS Marketplace e aceite de termos; consultar a documentação da AWS.
4. Configurar credenciais temporárias para o processo, por exemplo com papel de execução no ambiente AWS ou variáveis temporárias obtidas pelo mecanismo de autenticação da organização. O SDK usa sua cadeia padrão de credenciais; nunca adicionar credenciais em arquivos versionados. Perfis IAM Identity Center ou papéis assumidos podem exigir módulos adicionais de SSO/STS no classpath; confirme as dependências antes de adotá-los. A existência de credenciais não prova autorização ao modelo.
5. Configurar orçamento e alertas na conta. O diagnóstico chama o serviço real e pode gerar cobrança por tokens; o limite de tokens não é um teto de custo financeiro.

Fontes oficiais: [Converse e permissão de invocação](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html), [cadeia de credenciais do SDK Java 2](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials-chain.html), [acesso a modelos](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html), [perfis de inferência e regiões](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html).

## Variáveis do backend

Defina as seguintes variáveis somente no ambiente que usará o serviço. No PowerShell:

```powershell
$env:ASSISTENTE_BEDROCK_HABILITADO = 'true'
$env:ASSISTENTE_BEDROCK_REGIAO = '<região AWS>'
$env:ASSISTENTE_BEDROCK_MODELO = '<ID ou ARN do modelo ou perfil de inferência>'
$env:ASSISTENTE_BEDROCK_TIMEOUT_SEGUNDOS = '30'
$env:ASSISTENTE_BEDROCK_MAX_TOKENS = '256'
```

O limite de timeout aceito é 1–120 segundos; o limite de saída é 1–4096 tokens e deve ser compatível com o modelo. As duas últimas variáveis são opcionais e seus padrões são 30 segundos e 256 tokens. Se a integração estiver habilitada, região e modelo são obrigatórios; erros de configuração impedem a inicialização. Com a integração desabilitada, nenhuma credencial ou região é necessária e não há `AssistenteGateway` registrado.

O componente `ConfiguracaoBedrock` cria um cliente `BedrockRuntimeClient` com timeout global e registra `AssistenteGateway`, quando habilitado. A implementação `BedrockGateway` envia instruções como mensagem de sistema e o conteúdo como mensagem de usuário, com temperatura zero. Ela recusa entradas vazias ou acima dos limites, respostas vazias, truncadas, com ferramenta solicitada ou bloqueadas, e converte falhas do SDK em `BedrockIndisponivelException`. O chamador deve tratar indisponibilidade sem impedir a escrita/salvamento. O texto retornado é **saída bruta não confiável**.

## Diagnóstico com dados sintéticos

Após integrar a fundação e configurar credenciais, escolha o mesmo modelo e região para o comando de diagnóstico:

```powershell
cd backend
$env:AWS_REGION = $env:ASSISTENTE_BEDROCK_REGIAO
$env:BEDROCK_MODEL_ID = $env:ASSISTENTE_BEDROCK_MODELO
.\mvnw.cmd compile exec:java "-Dexec.mainClass=br.ufg.grupo8.assistente.bedrock.TesteConexaoBedrock"
```

O comando envia uma pergunta fixa sobre o conceito de tese, sem textos de estudantes, e imprime resposta, latência e contagem de tokens. A pergunta não prova o cumprimento do RF09. Registre região, modelo/perfil, credenciais usadas pelo tipo de papel, latência, tokens, custo apurado e resultado no ADR-006 sem registrar chaves. Repita com os casos de teste previstos em T07 antes de concluir escolha e avaliação.

Para executar o backend com a integração habilitada, configure também o PostgreSQL e as demais variáveis conforme `backend/README.md` da branch de fundação, depois rode `.\mvnw.cmd spring-boot:run`. A conexão é um componente Java interno, não um serviço HTTP para testar diretamente pelo navegador.

## Testes sem AWS

```powershell
cd backend
.\mvnw.cmd verify
```

Os testes substituem o cliente AWS por um dublê e verificam mensagem, instrução, modelo, tokens, limites, falhas do SDK, respostas bloqueadas/truncadas e ativação explícita. Não fazem rede, não usam credenciais e não geram custo. Os testes devem ser executados no projeto após a integração da branch de fundação.

## Segurança e dados

Antes de qualquer uso com texto de estudante, implementar o serviço pedagógico com autorização por recurso, montagem de contexto minimizada, tratamento de dados pessoais, classificação de pedidos, recusa e `GuardrailDeAutoria`, persistência da interação e avaliação adversarial de RF09. O adaptador, por si só, não detecta identificadores nem verifica se uma resposta escreve pelo estudante; não deve ser conectado diretamente à interface ou a um endpoint público. Não enviar dados reais no diagnóstico.

Avaliar para a região, modelo e conta escolhidos: termos e retenção aplicáveis, eventuais destinos de inferência entre regiões e a configuração de logs. O [logging de invocação](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html), quando ativado, pode registrar entradas e saídas. A AWS descreve [regras de retenção e possíveis exceções por modelo](https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html); essas informações devem ser validadas antes do piloto.

## Falhas comuns

- **Configuração incompleta:** `ASSISTENTE_BEDROCK_REGIAO` e `ASSISTENTE_BEDROCK_MODELO` devem estar definidos quando habilitado; o comando sintético usa `AWS_REGION` e `BEDROCK_MODEL_ID`.
- **Credenciais ausentes/expiradas:** verificar a cadeia de credenciais e renovar as credenciais temporárias no ambiente. Não compartilhar tokens na issue ou em logs.
- **AccessDeniedException:** conferir IAM, políticas da organização, região, ativação do modelo, Marketplace e perfil de inferência; não conceder permissões amplas como solução padrão.
- **Throttling, timeout, modelo indisponível:** verificar cota, região e indisponibilidade, além do timeout. A aplicação consumidora deve exibir indisponibilidade e permitir que o estudante continue escrevendo.
- **Resposta recusada ou truncada:** o adaptador falha de forma controlada; investigar a configuração do modelo e o limite de saída com dados sintéticos.

A conexão foi compilada e testada em cópia temporária da fundação. A chamada real permanece pendente de conta, credenciais, modelo e região; nenhuma configuração de conta AWS foi modificada.
