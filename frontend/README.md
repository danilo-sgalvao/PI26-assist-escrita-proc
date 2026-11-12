# Frontend Entrelinhas

Interface React + TypeScript para autenticação Cognito, envio assíncrono de redações e consulta de revisões. Baseada no esqueleto da branch `feat/T06-esqueleto-frontend`; preserva a página de termo de ciência.

## Executar

Requisitos: Node.js 22.22.2 ou superior. Copie `.env.example` para `.env.local` e preencha os valores das saídas da stack SAM:

- `VITE_API_URL`: URL REST incluindo estágio, sem barra final.
- `VITE_WEBSOCKET_URL`: URL WSS incluindo estágio.
- `VITE_COGNITO_REGION` e `VITE_COGNITO_CLIENT_ID`: região e cliente público do Cognito.

O cliente Cognito precisa permitir `USER_PASSWORD_AUTH`. O primeiro acesso suporta `NEW_PASSWORD_REQUIRED`; outras etapas de autenticação ainda não estão implementadas. Configure CORS na API REST para a origem exata da SPA, incluindo `Authorization`, `Content-Type` e os métodos POST, GET e OPTIONS. As alterações na infraestrutura são feitas separadamente.

```powershell
npm ci
npm run dev
npm test
npm run lint
npm run build
```

O build em `dist/` pode ser enviado ao bucket de frontend e entregue pelo CloudFront. Para a rota direta do termo de ciência, configure fallback SPA no CloudFront. As variáveis `VITE_*` são públicas no bundle: não inclua senhas, segredos ou tokens nelas.

## Contrato utilizado

- `POST /producoes`: ID token no cabeçalho `Authorization`; JSON `{texto, consentimento: true}`; HTTP 202 com `{id_producao, status}`.
- `GET /producoes/{id}`: mesmo ID token; resposta `{id_producao, status, sugestoes: string[]}`.
- WebSocket: token de acesso Cognito no parâmetro `token`; a mensagem `{tipo: "REVISAO_DISPONIVEL", id_producao}` dispara nova consulta REST. O token não deve constar em logs de requisição. Na indisponibilidade do WebSocket, a interface consulta revisões em andamento a cada 10 segundos.

O histórico de IDs e horários é mantido apenas no `sessionStorage` do navegador, separado por usuário; o texto e os tokens não são persistidos nesse armazenamento. A API atual não oferece listagem de versões nem leitura do texto salvo; portanto, o histórico não sincroniza entre dispositivos e não permite reabrir o conteúdo das versões. O rascunho presente no editor é mantido somente na memória e se perde ao recarregar; copie seu texto antes de fechar a página. O checkbox registra a autorização enviada à API, não substitui eventual fluxo formal de consentimento do responsável.
