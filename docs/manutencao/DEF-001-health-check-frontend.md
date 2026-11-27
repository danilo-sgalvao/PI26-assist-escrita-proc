# DEF-001 — Health check do frontend consulta rota inexistente (`/api/health`)

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Data | 26/11/2026 |
| Autor | Luiz Augusto Godinho (com apoio de IA; ver seção 11) |
| Revisor | A definir no PR (Danilo Galvão, Felipe Nunes ou Enzo Machado) |
| Estado | Corrigido, em revisão |
| Issue / tarefa | #117 · T111 |
| Categoria (ISO/IEC/IEEE 14764) | **Corretiva**: corrige um defeito encontrado no produto, que estava em produção no `main` |
| Requisito afetado | RF21 (termo de ciência), página que mostra o estado da API |
| Conformidade | Manutenção de Software: T-M04 (corretiva), lacuna 5 · Implantação e Entrega: I24, C6, T-I14 |

## 1. Relato

A página do termo de ciência (`/`, componente `TermoDeCiencia`) verifica se a API está no ar e mostra "API disponível." ou "API indisponível no momento.". Quando a variável `VITE_API_URL` não está configurada, `frontend/src/api/http.ts` recorre a `GET /api/health` na própria origem da SPA. Essa rota não existe: a API REST da stack SAM (`infra/template.yaml`) expõe `GET /saude`, sem prefixo `/api`, num domínio do API Gateway diferente do domínio do CloudFront. O teste `TermoDeCiencia.test.tsx` não pegava o problema, porque confirmava justamente a chamada a `/api/health`.

O defeito foi apontado na análise de conformidade das disciplinas (`docs/conformidade/01-manutencao-de-software.md`, lacuna 5, e `03-implantacao-e-entrega-de-software.md`, item I24).

## 2. Passos para reproduzir

1. Em `frontend/`, sem `.env.local` (ou com `VITE_API_URL` vazio), rodar `npm ci`.
2. Rodar o teste de regressão criado nesta correção contra o código antigo:

   ```powershell
   npx vitest run src/api/http.test.ts src/pages/TermoDeCiencia.test.tsx
   ```

3. Alternativa manual: `npm run build` sem `VITE_API_URL`, publicar `dist/` no CloudFront com o fallback de SPA recomendado no `frontend/README.md` e abrir a página do termo. Ou `npm run dev` e observar no navegador a requisição a `/api/health`.

## 3. Resultado esperado

- O health check consulta somente a rota que a API realmente expõe: `GET {VITE_API_URL}/saude`.
- Sem `VITE_API_URL`, nenhuma requisição é feita a uma rota inexistente e a página **não** afirma que a API está disponível.

## 4. Resultado obtido (antes da correção)

- Sem `VITE_API_URL`, o frontend faz `GET /api/health` na origem da própria SPA.
- No CloudFront com fallback de SPA, qualquer caminho desconhecido devolve o `index.html` com HTTP 200, e a página mostra **"API disponível."** mesmo sem API nenhuma: um **falso positivo**.
- No `npm run dev`, o Vite encaminha `/api` para `http://localhost:8080`, endereço do backend Spring Boot que foi removido em 11/11/2026; a página mostra "indisponível", mas por um motivo que não tem relação com a API real.
- Saída dos testes de regressão contra o código antigo (2 falhas):

  ```
  × naoDeveRecorrerARotaInexistenteApiHealthSemApiConfigurada_DEF001
    AssertionError: promise resolved "undefined" instead of rejecting
  × naoDeveAnunciarApiDisponivelSemApiConfigurada_DEF001
    Expected element to have text content: API indisponível no momento.
    Received: API disponível.
  Test Files  2 failed (2)
       Tests  2 failed | 4 passed (6)
  ```

## 5. Severidade

**Média** (plano v1.2, tabela 88): comportamento incorreto com contorno simples. Com `VITE_API_URL` configurado, como pede o `frontend/README.md`, o caminho correto (`/saude`) já era usado. O defeito não viola RN01/RN02/RN04 nem expõe dados, mas a mensagem falsa de "API disponível." engana quem diagnostica um deploy mal configurado.

## 6. Causa raiz

Resíduo da arquitetura anterior, que sobreviveu à migração para a arquitetura serverless:

1. O esqueleto do frontend (commit `4cfaf50`, #10) foi escrito para o backend Spring Boot. Ele chamava `/api/health` na mesma origem e configurava no Vite um proxy `/api` → `http://localhost:8080`.
2. Ao adaptar o frontend à API SAM (commit `a5d38b9`), passou-se a usar `${VITE_API_URL}/saude`, mas `/api/health` ficou como alternativa quando a variável falta. O proxy do Vite e a função `getJson` (tipada para caminhos `/api/...` e sem uso) também ficaram.
3. O teste do `TermoDeCiencia` roda sem `VITE_API_URL` e, por isso, exercitava só a alternativa, fixando `/api/health` como resultado esperado. O oráculo do teste estava errado, e o defeito passava pelos testes.

## 7. Correção

Decisão sobre o comportamento sem `VITE_API_URL`: **falhar de forma explícita, sem fazer requisição**. Alternativas consideradas:

| Alternativa | Por que foi descartada |
|---|---|
| Trocar a alternativa por `/saude` na mesma origem | O CloudFront só entrega a SPA (bucket S3) e não encaminha rotas para a API; com o fallback de SPA, o falso positivo continuaria |
| Manter um proxy do Vite apontando para a API | Não há API local: a stack SAM roda na AWS e o `sam local` não faz parte do fluxo documentado. O proxy esconderia a falta de configuração só no ambiente de desenvolvimento |
| Criar a rota `/api/health` na API | Duplicaria o `GET /saude` já existente e mexeria na infra, fora do escopo de uma correção no frontend |

A decisão é coerente com o restante do frontend e com a documentação: o `frontend/README.md` e o `.env.example` tratam `VITE_API_URL` como obrigatória, e `entrar()` em `revisoes.ts` também falha de forma explícita quando a configuração do Cognito falta.

Mudanças:

- `frontend/src/api/http.ts`: `verificarSaude()` usa só `${VITE_API_URL}/saude` e, sem a variável, rejeita com `A URL da API não foi configurada (VITE_API_URL).`, sem chamar `fetch`. A página mostra "API indisponível no momento.". A função `getJson`, sem uso e presa ao prefixo `/api`, foi removida.
- `frontend/vite.config.ts`: removido o proxy `/api` → `localhost:8080`, resíduo do backend Spring.
- `frontend/README.md`: `GET /saude` incluído no contrato utilizado, com o comportamento sem `VITE_API_URL`.
- `frontend/src/api/revisoes.test.ts`: correção do erro de lint pré-existente (`_url` sem uso), necessária para o `npm run lint` passar; não tem relação com o defeito.

## 8. Teste de regressão

| Teste | Arquivo | Antes | Depois |
|---|---|---|---|
| `naoDeveRecorrerARotaInexistenteApiHealthSemApiConfigurada_DEF001` | `frontend/src/api/http.test.ts` | ❌ falha | ✅ passa |
| `naoDeveAnunciarApiDisponivelSemApiConfigurada_DEF001` | `frontend/src/pages/TermoDeCiencia.test.tsx` | ❌ falha | ✅ passa |
| `deveConsultarRotaSaudeDaApiConfigurada_DEF001` (com barra final na URL) | `frontend/src/api/http.test.ts` | ✅ passa | ✅ passa |
| `deveFalharQuandoSaudeNaoResponde200_DEF001` | `frontend/src/api/http.test.ts` | ✅ passa | ✅ passa |
| `mostra o termo e confirma a conexão com GET /saude da API configurada` (atualizado; antes esperava `/api/health`) | `frontend/src/pages/TermoDeCiencia.test.tsx` | — | ✅ passa |

Os dois primeiros reproduzem o defeito; os outros protegem o caminho correto, que já funcionava. Depois da correção, em `frontend/`: `npm test` com 11 testes passando em 4 arquivos, e `npm run lint` e `npm run build` sem erros.

## 9. Verificação

- Automatizada: os testes acima, rodados localmente; ainda não há CI (o workflow está sendo criado na T69).
- Manual, pendente para o revisor ou para o próximo deploy: com `VITE_API_URL` apontando para o estágio `v1`, abrir a página do termo e confirmar "API disponível." e a requisição `GET .../v1/saude` com HTTP 200 nas ferramentas do navegador.

## 10. Observação fora do escopo

`frontend/src/api/revisoes.ts` monta as URLs de `POST /producoes` e `GET /producoes/{id}` com o mesmo `VITE_API_URL || ''`. Sem a variável, as chamadas iriam para a origem da SPA. Isso não é exercitado hoje, porque o login falha antes por falta da configuração do Cognito, mas vale a mesma validação explícita numa manutenção futura.

## 11. Uso de IA

Registro conforme o Apêndice D do plano v1.2: o diagnóstico, a correção, os testes e este registro foram feitos com o Claude Code (Anthropic), modelo Claude Opus 5.5, em 26/11/2026, a partir da descrição da tarefa T111 (issue #117). A revisão e a aprovação ficam com a equipe, no PR.
