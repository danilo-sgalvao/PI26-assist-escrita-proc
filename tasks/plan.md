# Plano de desenvolvimento do backend

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Data | 30/10/2026 |
| Autor | Planejamento com apoio de IA (Codex) |
| Revisor | A definir |
| Estado | Proposta para revisão pela equipe |

Este plano divide o backend do Assistente de Escrita Processual em cinco entregas verificáveis. A integração de IA será com AWS Bedrock, conforme orientação do usuário. O modelo, a região e a configuração ainda serão definidos e registrados em ADR-006. A ERS v2 continua como base dos requisitos e o plano mestre v1.2 permanece a referência de cronograma e prioridades. Este documento não altera a ERS.

## 1. Fundação, acesso e prova técnica do Bedrock

- Criar o projeto Java/Spring Boot com Maven, PostgreSQL e migrações Flyway; configurar ambiente local, testes e integração contínua.
- Implementar autenticação por sessão, perfis de professor e estudante, autorização inicial e registro do aceite do termo de ciência (RF21–RF22). Preparar dados de demonstração.
- Executar o spike T07 em paralelo: verificar acesso ao Bedrock, modelos disponíveis na região, termos, custo, latência e qualidade em português. Testar a chamada por um adaptador isolado, sem dados reais.
- Usar papéis e credenciais AWS apropriados ao ambiente, com permissões mínimas e sem segredos no repositório. Documentar configuração, região, modelo e limites de custo; registrar os resultados e a decisão em ADR-006.

**Aceite:** aplicação e banco iniciam em ambiente limpo; autenticação e restrições por perfil são testadas; chamada experimental ao Bedrock funciona com dados sintéticos, ou o bloqueio de acesso e seu responsável ficam registrados.

## 2. Turmas, atividades e processo de escrita

- Implementar turmas, matrícula, atividades e início de produção com autorização por vínculo (RF01–RF02 e RF16).
- Implementar edição, versões automáticas e marcadas, histórico e comparação de versões (RF03–RF06). Persistir registros de forma imutável e criar versão automática somente se houver alteração.
- Implementar transições Planejar → Escrever → Revisar → Reescrever, retornos registrados e versões marcadas (RF17); registrar colagens como informação, sem bloquear a ação (RF18, Should).
- Aplicar política de prazo configurável, com padrão de aceitar e marcar atraso; preservar o histórico e a propriedade dos dados.

**Aceite:** um professor cria turma e atividade; um estudante autorizado inicia e percorre a produção, consulta e compara versões; testes comprovam isolamento entre turmas e rejeição de alteração/exclusão de registros imutáveis. Conforme o plano mestre, a demonstração das etapas na interface ocorre em M4.

## 3. Apoio pedagógico com AWS Bedrock

- Implementar RF07–RF10 e RF12: solicitação de apoio, classificação, contexto da atividade e etapa, registro de interações e identificação de respostas de IA.
- Implementar a porta `AssistenteGateway` e um adaptador Bedrock, preferencialmente com Spring AI e API Converse, após confirmar compatibilidade das versões escolhidas. Configurar timeout, tratamento de indisponibilidade e parâmetros por ambiente; manter um adaptador falso para CI.
- Recusar explicitamente pedidos de redação ou reescrita. Para os demais, enviar instruções versionadas e conteúdo delimitado; minimizar dados e não incluir identificadores do estudante. A escrita e o salvamento devem continuar disponíveis quando a IA falhar.
- Validar toda resposta antes da exibição com o GuardrailDeAutoria; em reprovação, devolver orientação genérica e registrar o bloqueio. Testar ataques de instrução e verificar manualmente os casos adversariais: regras determinísticas são uma camada de defesa, sem garantia geral contra todas as respostas indevidas.
- Avaliar pelo menos 30 pedidos de escrita/reescrita diretos ou disfarçados, além de pedidos legítimos. Registrar custo, latência e resultados de avaliação com dados sintéticos. Os limites numéricos de resposta (B5) e a meta final de latência (B10) continuam pendentes.

**Aceite:** fluxo de apoio funciona com o adaptador falso e, sob demanda, com Bedrock; a suíte de pelo menos 30 pedidos não apresenta texto aproveitável nos casos avaliados; testes verificam minimização do payload, recusa, bloqueio, registro e operação em caso de falha.

## 4. Submissão, acompanhamento e similaridade

- Implementar submissão com versão final marcada, aplicação da política de prazo e bloqueio de edição ou transição posterior (RF14).
- Disponibilizar ao professor acompanhamento por atividade e estudante, histórico, comparação, interações, progresso e eventos de colagem; disponibilizar ao estudante os próprios registros (RF11–RF13 e RF20). Impedir acesso fora do vínculo e evitar rankings e rótulos de julgamento.
- Disparar a similaridade automaticamente após a submissão (RF15, Should). Comparar a produção com textos internos da mesma atividade e respostas do assistente recebidas pelo estudante, apresentando fontes e trechos sem veredito de plágio. A implementação proposta usa contenção de n-gramas de palavras, com parâmetros calibrados por testes.
- Registrar a divergência: a ERS v2 menciona base externa; B2 determina que ela fica para evolução futura. Devolutiva do professor (RF19) é Could e depende de capacidade após o escopo prioritário.

**Aceite:** submissão impede novas edições; consultas respeitam perfil e turma; análise automática detecta cópias literais nos casos de teste e apresenta evidências sem classificação automática de plágio.

## 5. Integração, validação e entrega

- Integrar o backend ao frontend e executar o fluxo completo com dados sintéticos, incluindo falha do Bedrock, autorização negativa, perda de conexão e políticas de prazo.
- Executar testes de unidade, integração com PostgreSQL, API e arquitetura; conferir critérios de aceitação, segurança e privacidade, desempenho, imutabilidade e restauração de backup.
- Completar documentação de execução e configuração, contrato OpenAPI, decisões arquiteturais e rastreabilidade RF/RN/RNF → testes. Preparar demonstração e protocolo de piloto; o piloto com estudantes ocorre após a entrega e depende de aprovação e consentimento.
- Validar metas do plano mestre ou registrar desvios para decisão da equipe. Não considerar concluídos os requisitos Should removidos ou simplificados sem registrar a mudança.

**Aceite:** fluxo ponta a ponta demonstrado; testes e CI aprovados; requisitos Must com evidências; nenhum defeito bloqueante ou alto em aberto; backup restaurado e documentação de execução revisada.

## Dependências e decisões

Ordem principal: 1 → 2 → 3 → 4 → 5. O spike Bedrock começa na etapa 1, antes da implementação completa do assistente; o desenvolvimento de turmas e versões pode avançar enquanto a escolha de modelo é avaliada. A etapa 4 depende dos dados de produção e interações para apresentar acompanhamento e similaridade.

O prazo geral existente é de seis semanas; estas cinco etapas são agrupamentos de desenvolvimento, não cinco semanas nem estimativas adicionais. B5, B10, modelo, região, retenção de dados e condições do piloto permanecem decisões abertas. Confirmar também políticas de acesso, registros de invocação, disponibilidade do modelo e processamento regional antes do uso de dados reais.

Fontes do projeto: [ERS v2](../docs/ers/v2/ERS-Grupo8-v2.md), [decisões v1.2](../docs/plano/v1.2/decisoes-plano-v1.2.md), [plano mestre v1.2](../docs/plano/v1.2/plano-mestre-v1.2.md). Referências técnicas: [Spring AI — Bedrock Converse](https://docs.spring.io/spring-ai/reference/api/chat/bedrock-converse.html), [AWS — API Converse](https://docs.aws.amazon.com/bedrock/latest/userguide/conversation-inference.html).

Registro de IA: Codex, 30/10/2026; solicitação: “planeje etapas de desenvolvimento do backend no maximo 5 etapas; a conexão será com aws bedrock para IA”. A equipe deve revisar o plano e as decisões antes de adotá-los.
