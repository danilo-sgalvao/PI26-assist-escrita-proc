# Executar backend e PostgreSQL com Docker

| Campo | Valor |
|---|---|
| Versão | 0.1 |
| Data | 30/10/2026 |
| Autor | Implementação com apoio de IA (Codex) |
| Revisor | A definir |
| Estado | Configuração para desenvolvimento local |

A imagem do backend é compilada com Maven Wrapper e Java 25 e executada com JRE 25 como usuário sem privilégios. O Compose complementar aproveita o PostgreSQL da fundação e espera o banco ficar saudável antes de iniciar o backend.

## Pré-requisitos

A branch `codex/add-docker-backend` foi criada a partir de `main` e contém apenas a adição de Docker. Primeiro integre `codex/add-fundacao-backend`: ela fornece o código Java, o Maven Wrapper e `infra/compose.yaml`. Após integrar a conexão Bedrock, `backend/SETUP-BEDROCK.md` detalha sua configuração. Instale Docker Engine/Desktop com Compose e inicie o serviço Docker. A primeira compilação precisa acessar o Docker Hub e o Maven Central.

## Iniciar

Na raiz do projeto, no PowerShell:

```powershell
$env:SPRING_PROFILES_ACTIVE = 'demo'
$env:DEMO_PASSWORD = '<senha de demonstração com pelo menos 12 caracteres>'
docker compose -f infra/compose.yaml -f infra/compose.backend.yaml up --build -d --wait
Invoke-RestMethod http://localhost:18080/api/health
```

A aplicação atende somente em `127.0.0.1:18080` por padrão. Configure `BACKEND_PORT` para mudar a porta no host; dentro do contêiner permanece 8080. O PostgreSQL atende na rede interna pelo nome `postgres:5432` e, para acesso a partir do host, em `127.0.0.1:35432`, configurável por `POSTGRES_PORT` no Compose da fundação. Ambos usam a mesma senha configurada em `POSTGRES_PASSWORD`; o padrão `assistente_local` é exclusivamente para desenvolvimento.

O perfil `demo` cria `estudante@demo.local` e `professor@demo.local`, com a senha de `DEMO_PASSWORD` no primeiro início. Sem `SPRING_PROFILES_ACTIVE=demo`, não são criadas contas de demonstração. Alterar a senha no ambiente não substitui contas já persistidas no volume. A configuração `COOKIE_SECURE=false` é para HTTP local; use HTTPS e `COOKIE_SECURE=true` para um ambiente apropriado.

Para inspecionar logs e interromper os serviços sem apagar o banco:

```powershell
docker compose -f infra/compose.yaml -f infra/compose.backend.yaml logs -f backend
docker compose -f infra/compose.yaml -f infra/compose.backend.yaml stop
```

O volume de dados do PostgreSQL persiste. `down -v` remove o volume e os dados: use apenas quando a exclusão for desejada. Se uma porta estiver ocupada, defina `BACKEND_PORT` ou `POSTGRES_PORT` antes de iniciar.

## AWS Bedrock

A integração só estará disponível após integrar `codex/add-conexao-bedrock`. O override repassa `ASSISTENTE_BEDROCK_HABILITADO`, `ASSISTENTE_BEDROCK_REGIAO`, `ASSISTENTE_BEDROCK_MODELO`, `ASSISTENTE_BEDROCK_TIMEOUT_SEGUNDOS` e `ASSISTENTE_BEDROCK_MAX_TOKENS`, além de `AWS_REGION`. A integração fica desabilitada por padrão.

As variáveis `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` e `AWS_SESSION_TOKEN` são repassadas quando presentes no host. O Compose expõe essas variáveis ao processo do contêiner, portanto use apenas credenciais temporárias em ambiente local confiável. A cadeia de credenciais precisa funcionar dentro do contêiner: uma configuração de perfil no computador não é automaticamente disponibilizada ao contêiner. Para serviços AWS, prefira papel de execução; para desenvolvimento, configure um mecanismo de credenciais temporárias apropriado ao seu ambiente, sem incluir segredos na imagem ou no repositório. Não envie textos de alunos no diagnóstico. Consulte o guia do Bedrock após integrar a branch correspondente.

## Verificação

```powershell
docker compose -f infra/compose.yaml -f infra/compose.backend.yaml config --quiet
docker compose -f infra/compose.yaml -f infra/compose.backend.yaml up --build -d --wait
Invoke-RestMethod http://localhost:18080/api/health
```

O build da imagem executa `package` com os testes desabilitados; execute os testes da fundação com o Maven Wrapper ou pela CI antes da integração. A imagem e o Compose são para desenvolvimento local, não representam implantação de produção.
