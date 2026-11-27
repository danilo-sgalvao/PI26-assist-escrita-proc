# Protótipo de baixa fidelidade — T05 (#9)

- **Versão:** 0.2
- **Data:** 27/11/2026 (versão inicial: 11/11/2026)
- **Autor:** Enzo Machado, com apoio de IA (Codex)
- **Revisor:** área A, pendente
- **Estado:** proposta para revisão

Abra [index.html](index.html) no navegador. O menu percorre os fluxos sem backend. Os dados são ilustrativos; links e controles não autenticam, não salvam e não consultam a API. O wireframe representa o **fluxo previsto para as fatias 1 a 5**, não as funções já implementadas na `main`.

A versão 0.2 preserva o protótipo de 11/11 e o alinha ao [design de dados e API](../../arquitetura/modelo-de-dados-e-api.md) aceito como base em 19/11: identidade e perfis no Cognito, aceite do termo no servidor, texto e pedido de apoio processados pelo Bedrock com saída restrita ao catálogo da equipe, versões consultadas no servidor e papéis distintos de estudante e professor. O texto exibido no termo é uma proposta de interface sujeita à revisão da área A.

| Tela | Requisitos rastreados | Tarefa atual do backlog | Fluxo principal |
|---|---|---|---|
| Acesso | RF22 | T80 | Entrar como estudante ou professor; o perfil controla a visão |
| Termo de ciência | RF21, RF22, RN10 | T80 | Conhecer o uso dos dados e aceitar; consentimento do responsável quando necessário |
| Atividades | RF01, RF02, RF16, RF22 | T80 | Consultar atividades vinculadas e iniciar uma produção |
| Editor por etapas | RF03, RF04, RF14, RF17, RF18 | T87, T96 | Planejar, escrever, salvar, mudar de etapa, registrar colagens e submeter |
| Histórico e comparação | RF04, RF05, RF06, RF18 | T87 | Filtrar versões vindas do servidor e comparar duas |
| Painel de apoio | RF07–RF10, RF12, RN01, RN02 | T93 | Pedir orientação sobre trecho selecionado; ver resposta do catálogo ou recusa |
| Painel do professor | RF05, RF06, RF10–RF13, RF15, RF18, RN05, RN06 | T98, T102 | Acompanhar uma atividade sem ranking nem veredito de plágio |
| Meus registros | RF04, RF05, RF10–RF12, RF18, RF20, RN10 | T99 | Consultar apenas os próprios registros e indicadores |

A comparação entre versões será calculada no servidor, conforme a decisão D5 do design. A tela de similaridade do professor depende da fatia 5. O registro de colagens e o painel “Meus registros” são itens *Should* do backlog.

## Situação da T06 (#10)

O esqueleto React, TypeScript, Vite, roteamento, cliente HTTP, ESLint e Vitest foi criado por Enzo na branch `feat/T06-esqueleto-frontend` (commit `4cfaf50`). A `main` recebeu um frontend baseado nesse esqueleto no commit `a5d38b9`, com adaptações para Cognito, API Gateway e fluxo assíncrono. Esta regularização não reaplica o commit antigo, pois a `main` já contém uma versão evoluída do frontend.

A página atual do termo é estática e verifica a saúde da API; ela ainda não grava o aceite do usuário. O aceite persistido pertence à T80. O critério `/api/health` escrito na issue T06 pertence à arquitetura antiga; a API SAM usa `GET /saude`. O CI geral está em desenvolvimento na T69, e a correção do health check está em desenvolvimento na T111. Esses itens devem ser verificados antes de encerrar formalmente a T06.

## Pontos para revisão da área A

1. Confirmar a redação do termo, inclusive o processamento pelo Amazon Bedrock e o consentimento de responsáveis por menores.
2. Validar o fluxo de etapas, sobretudo a volta e o ciclo Revisar → Reescrever.
3. Validar a separação entre a visão do professor e a do estudante.
4. Verificar a rastreabilidade acima contra os critérios de aceitação das novas tarefas.

O conteúdo e a rastreabilidade foram atualizados com auxílio de IA e precisam da revisão humana prevista na T05.
