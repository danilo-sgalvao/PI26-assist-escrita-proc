# Backend do Assistente de Escrita Processual

Fundação da etapa 1: Java 25, Spring Boot 4, PostgreSQL, Flyway, autenticação por sessão, perfis, CSRF e aceite do termo. O assistente pedagógico será implementado em etapa posterior.

## Executar localmente

Requisitos: JDK 25, Docker com Compose e acesso à internet na primeira execução do Maven Wrapper. Na raiz do repositório:

```powershell
docker compose -f infra/compose.yaml up -d --wait
cd backend
$env:SPRING_PROFILES_ACTIVE = 'demo'
$env:DEMO_PASSWORD = '<senha exclusiva de demonstração com pelo menos 12 caracteres>'
$env:COOKIE_SECURE = 'false'
.\mvnw.cmd spring-boot:run
```

No Linux/macOS, use `./mvnw`. O PostgreSQL local é publicado somente em `127.0.0.1:35432`; `POSTGRES_PORT` permite mudar a porta e `DATABASE_URL` deve acompanhar a alteração. O usuário e a senha padrão do banco são exclusivos para desenvolvimento local (`assistente` / `assistente_local`); para outra senha, configure `POSTGRES_PASSWORD` no Compose e `DATABASE_PASSWORD` no backend. Em ambiente com HTTPS mantenha `COOKIE_SECURE=true` (padrão).

O perfil `demo` cria usuários sintéticos `estudante@demo.local` e `professor@demo.local` usando o hash BCrypt de `DEMO_PASSWORD`; ele não é ativado por padrão. A senha é usada apenas na criação inicial: mudar a variável depois não altera usuários existentes. Nenhum cadastro de usuário real é fornecido nesta etapa.

### Fluxo HTTP

1. `GET /api/csrf` retorna o token e o nome do cabeçalho CSRF.
2. `POST /api/login` recebe `username` e `password` como `application/x-www-form-urlencoded` e exige o token CSRF; sucesso retorna 204 e estabelece sessão em cookie HttpOnly.
3. Para estudante, `GET /api/termo` mostra o texto e `POST /api/termo/aceite` registra o aceite da versão vigente, com CSRF. Depois do login, obtenha um novo token CSRF. Até aceitar o termo, o estudante recebe 403 ao acessar os demais recursos protegidos.
4. `GET /api/eu` consulta a sessão; `GET /api/professor` exige perfil de professor. `POST /api/logout` exige CSRF e invalida a sessão. `GET /api/health` é público.

Para menores, o aceite exige que `consentimento_responsavel` já esteja registrado no cadastro. Não há interface de obtenção desse consentimento nesta etapa; para dados reais será necessário implementar e revisar esse processo. O texto do termo é preliminar e deve ser aprovado pela equipe e pelo professor.

## Testes

```powershell
cd backend
.\mvnw.cmd verify
```

Os testes usam H2 em modo PostgreSQL e cobrem login/sessão, credenciais incorretas, CSRF, perfis, bloqueio antes do aceite e consentimento prévio de responsáveis. O fluxo também foi exercitado manualmente com PostgreSQL no Compose. A CI executa `verify` sem chamar a AWS.

## Experimento AWS Bedrock

O experimento é um programa isolado, sem endpoint de produção; envia apenas uma pergunta sintética fixa e imprime resposta, latência e contagem de tokens. Chamar o serviço pode gerar custos. É necessário configurar modelo, região e credenciais válidas com permissão mínima `bedrock:InvokeModel`, sem colocar credenciais no repositório:

```powershell
$env:AWS_REGION = '<região com modelo disponível>'
$env:BEDROCK_MODEL_ID = '<id do modelo habilitado>'
.\mvnw.cmd compile exec:java "-Dexec.mainClass=br.ufg.grupo8.assistente.ExperimentoBedrock"
```

O SDK usa a cadeia padrão de credenciais AWS. Registrar custo, qualidade, latência e decisão no [ADR-006](../docs/arquitetura/ADR-006-bedrock.md). Não foi possível medir o serviço neste ambiente porque a configuração AWS e o modelo não estavam disponíveis. Não use textos de estudantes no experimento.

## Limites atuais

Não há cadastro de usuários, gestão de turmas, persistência de sessão entre reinicializações nem controle de frequência de tentativas nesta etapa. A solução foi verificada em ambiente local e precisa de configuração HTTPS, revisão de segurança e processo de provisionamento antes de uso com pessoas reais. Os textos completos do termo e as regras de retenção exigem revisão e aprovação.
