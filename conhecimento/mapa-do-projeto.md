# Mapa de conhecimento do Assistente de Escrita Processual

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Data | 30/10/2026 |
| Autor | Síntese elaborada com apoio de IA (Codex) |
| Revisor | Pendente pela equipe |
| Estado | Material derivado para consulta; prevalecem as fontes abaixo |

O projeto do Grupo 8, na disciplina de Manutenção de Software da UFG, é uma POC em que o estudante escreve e a IA orienta sem produzir texto por ele. O professor acompanha o processo e continua responsável pela avaliação. Equipe: Danilo Galvão, Enzo Machado, Felipe Nunes e Luiz Augusto Godinho. A hipótese é que acompanhar a escrita por etapas desenvolve autoria e autorregulação sem dependência ou plágio assistido. A classificação de risco é moderada, coorte de entrada 2. Fontes: [contexto](../CLAUDE.md), [POC](../docs/referencias/POC%202.2.%20Assistente%20de%20escrita%20processual.pdf) e [ERS v2, seções 1–2](../docs/ers/v2/ERS-Grupo8-v2.md).

## Fontes e autoridade

| Fonte | Uso na base |
|---|---|
| [CLAUDE.md](../CLAUDE.md) | Fatos confirmados pela equipe e hierarquia entre documentos |
| [Decisões do plano v1.2](../docs/plano/v1.2/decisoes-plano-v1.2.md) | B1–B12, exceções e registro das alterações efetivamente aplicadas |
| [ERS v2](../docs/ers/v2/ERS-Grupo8-v2.md) | Base de requisitos RF01–RF22, RN01–RN10 e RNF01–RNF13 |
| [Plano mestre v1.2](../docs/plano/v1.2/plano-mestre-v1.2.md) | Processo, proposta de arquitetura/stack, cronograma, qualidade e rastreabilidade |
| [Apresentação](../docs/referencias/AssistentedeEscritaProcessual_2.pdf) e POC | Objetivo pedagógico, hipótese, salvaguardas e visão do stakeholder |
| ERS v1.0 e plano v1.1 | História e comparação entre versões; não definem a recomendação atual |

Fatos confirmados prevalecem; a ERS v2 prevalece sobre o plano em requisitos. O plano v1.2 continua como proposta para aprovação da equipe e validação do professor. As decisões da equipe registradas não tornam automaticamente aceitos os ADRs propostos. Word/PDF são representações quando há fonte canônica cadastrada. Fonte: [hierarquia documental](../CLAUDE.md#hierarquia-entre-os-documentos).

## Fluxo e requisitos funcionais

O professor cria turma e atividade; o estudante toma ciência dos registros e consente, inicia a produção em Planejar, avança por Escrever, Revisar e Reescrever, podendo voltar e repetir o ciclo antes da submissão. Há salvamento automático e versões marcadas nas transições. A submissão bloqueia edição e dispara a similaridade. O professor acompanha o processo e avalia os indícios. Fontes: [ERS v2, seções 3 e 6](../docs/ers/v2/ERS-Grupo8-v2.md) e [B3/B4/B7](../docs/plano/v1.2/decisoes-plano-v1.2.md).

| Requisito | Conhecimento principal | MoSCoW do plano |
|---|---|---|
| RF01 | Atividade com título, tema, gênero, orientações, critérios e prazo | Must |
| RF02 | Início de produção vinculada à atividade; etapa inicial Planejar | Must |
| RF03 | Editor para texto do estudante, sem aplicar conteúdo da IA | Must |
| RF04 | Versões automáticas quando houver alteração e versões marcadas | Must |
| RF05 | Histórico com filtros por etapa e tipo | Must |
| RF06 | Comparação de quaisquer duas versões; padrão primeira marcada × final | Must |
| RF07 | Pedido de apoio livre em qualquer etapa e seleção de trecho | Must |
| RF08 | Perguntas, apontamentos e explicações sobre escrita | Must |
| RF09 | Recusa explícita de escrita/reescrita e verificação automática de toda resposta | Must |
| RF10 | Registro de solicitação, orientação, etapa, data e recusa | Must |
| RF11 | Progresso: tempo por etapa, versões, alterações, interações e colagens | Should |
| RF12 | Categorias de apoio e evolução entre atividades e etapas | Should |
| RF13 | Painel do professor, sem ranking ou rótulo de julgamento | Must |
| RF14 | Submissão final, política configurável para atraso e bloqueio de edição | Must |
| RF15 | Similaridade após submissão, com trechos e fontes; divergência de corpus abaixo | Should |
| RF16 | Gestão de turma e visibilidade por vínculo | Must, apesar de Média na ERS |
| RF17 | Planejar → Escrever → Revisar → Reescrever, transições registradas | Must |
| RF18 | Colagem aceita e registrada com trecho, tamanho, etapa e horário | Should |
| RF19 | Devolutiva do professor visível ao estudante | Could, fora da base de horas |
| RF20 | Consulta do estudante aos próprios registros | Should |
| RF21 | Termo de ciência e consentimento antes do uso | Must |
| RF22 | Autenticação e autorização por perfil | Must |

As descrições vêm da [ERS v2, seção 3](../docs/ers/v2/ERS-Grupo8-v2.md); a priorização vem do [plano v1.2, seção 4.5](../docs/plano/v1.2/plano-mestre-v1.2.md). Must não equivale a implementação já concluída. O RF16 sobe de Média para Must por sustentar a visibilidade por turma. Valores de intervalo de salvamento e destaque de colagens continuam sugeridos, respectivamente 1 minuto e 200 caracteres.

## Autoria e regras de negócio

| Regra | Implicação |
|---|---|
| RN01–RN02 | Todo texto da produção é do estudante; a IA não redige, reescreve, completa ou parafraseia |
| RN03–RN04 | Registrar processo e manter histórico sem edição/exclusão durante a POC |
| RN05–RN06 | Indicadores não geram nota, ranking ou vigilância; similaridade e colagem são indícios interpretados pelo professor |
| RN07 | Avaliação e julgamento são exclusivos do professor |
| RN08 | Respeitar estilo e variação linguística; considerar norma-padrão somente se exigida pela atividade |
| RN09 | Orientar sem oferecer texto-modelo sobre o tema |
| RN10 | Informar o estudante sobre os registros e permitir que os consulte |

O RF09 exige pelo menos 30 pedidos de escrita/reescrita no conjunto de teste, nenhum com resposta aproveitável. Exemplos conceituais devem usar tema diferente do da atividade. As categorias do RF12 são estrutura/organização, coesão/coerência, argumentação, adequação ao gênero, pedido de escrita/reescrita e outro. Fonte: [ERS v2, seções 3.4, 4 e 7](../docs/ers/v2/ERS-Grupo8-v2.md).

## Decisões e divergências

| Decisão | Estado e efeito |
|---|---|
| B1 | API externa de LLM substitui a recomendação local da v1.1; o usuário definiu AWS Bedrock, e modelo/região dependem de T07/ADR-006 |
| B2 | Corpus de similaridade desta entrega: produções internas da atividade e respostas do assistente; base externa é evolução futura |
| B3 | Salvamento automático e versões marcadas por etapa, conforme ERS |
| B4 | Atraso configurável; padrão aceita e marca como atrasada |
| B5 | Pendente: limites numéricos do RF09; 150 palavras por orientação e exemplo de até 25 são proposta |
| B6 | Categorias de apoio da ERS/apresentação mais pedidos de escrita |
| B7 | Similaridade automática após submissão |
| B8 | MoSCoW; RF06 passa a Must; RF19 é Could |
| B9 | RNF01–13 da ERS, acrescidos de RNF14–17 candidatos do plano |
| B10 | Pendente: latência da IA; 10 s em 90% continua como valor sugerido da ERS |
| B11 | Entrega em seis semanas inclui demonstração e protocolo; piloto posterior, condicionado a aprovação/consentimento |
| B12 | Cronograma fixo, mesma capacidade; requisitos encaixados por realocação e priorização |

**Divergência preservada:** o RF15 da ERS v2 ainda prevê uma base externa; os fatos confirmados e B2 limitam o escopo atual ao corpus interno e às respostas do assistente. Essa divergência deve ser explicada nas respostas; a base RAG não altera o texto da ERS. Fontes: [decisões, seções B e E](../docs/plano/v1.2/decisoes-plano-v1.2.md) e [CLAUDE.md](../CLAUDE.md).

## Arquitetura e dados propostos

A proposta é SPA com monólito modular por domínio e portas/adaptadores. Módulos: identidade, atividades, producao, apoio, acompanhamento, similaridade e compartilhado. Frontend confirmado: React + TypeScript. Persistência e acesso a dados em Java são restrição confirmada. Java 25, Spring Boot 4.x, PostgreSQL 18, Spring Data JPA/Hibernate, Flyway, Spring Security por sessão/cookie HttpOnly/CSRF, Spring AI, Vite e java-diff-utils compõem a recomendação do plano, sujeita aos ADRs e à validação de compatibilidade. Fontes: [fatos e propostas](../CLAUDE.md) e [plano, seções 6.1–6.9](../docs/plano/v1.2/plano-mestre-v1.2.md).

O modelo proposto contém usuários, turmas/matrículas, atividades, produções, versões, transições de etapa, colagens, interações de apoio, aceite do termo, devolutivas e análises/resultados de similaridade. Versões, transições, interações e colagens são append-only, com UPDATE/DELETE rejeitados no banco. Progresso é derivado dos registros; migrações são versionadas. Similaridade proposta: contenção de n-gramas em Java, n inicial de 5 palavras e pelo menos 2 n-gramas consecutivos, a calibrar em T45. Ela localiza sobreposição literal e não emite veredito. Fontes: [plano, seções 6.4 e 6.6](../docs/plano/v1.2/plano-mestre-v1.2.md).

A defesa de autoria combina classificação do pedido, recusa explícita, prompt versionado, delimitação do texto, minimização de dados enviados, validador determinístico de saída, registro de bloqueios e proteção da chave. A proposta coloca o GuardrailDeAutoria como última camada de validação; sua eficácia precisa dos testes previstos e não é demonstrada pela existência do plano ou desta base. Fonte: [plano, seção 6.5](../docs/plano/v1.2/plano-mestre-v1.2.md).

## Privacidade e qualidade

RNF01–RNF04 tratam de minimização, retenção ainda a definir, pseudonimização, consentimento do responsável para menores, autorização por turma/perfil, HTTPS, hash de senhas e envio à API sem nome/e-mail/matrícula. O provedor escolhido não deve usar os dados para treinamento. RNF05 exige verificação de saída; RNF06–RNF09 tratam de latência sugerida, perda máxima sugerida de um minuto, escrita disponível mesmo sem assistente e integridade. RNF10–RNF13 cobrem linguagem simples, identificação das respostas de IA, WCAG 2.1 AA e Chrome/Firefox/Edge em computador. Fonte: [ERS v2, seção 5](../docs/ers/v2/ERS-Grupo8-v2.md).

RNF14–RNF17 são candidatos do plano: API em até 1 s no p95 fora IA/similaridade, substituição do provedor por adaptador/configuração, cobertura/modularidade e aviso de alteração não salva. Metas propostas: 70% de cobertura de linhas em domínio/aplicação; 90% de ramos no guardrail, transições e similaridade; 100% de CA Must aprovados em M6 e de testes negativos de autorização; zero identificadores no payload do provedor. Fontes: [plano, seções 5.5 e 9](../docs/plano/v1.2/plano-mestre-v1.2.md).

## Processo, capacidade e marcos

O plano adota processo iterativo baseado em Scrum com sprints semanais, quadro Kanban e WIP ≤ 4 em desenvolvimento e em revisão. Há refinamento uma sprint à frente e design do incremento antes de implementar cada requisito. A revisão em anel é A → B → C → D → A; autor e aprovador são diferentes. Áreas: A requisitos/produto/qualidade, B frontend, C backend/API/assistente, D persistência/dados/infra. A atribuição dos nomes às áreas continua em T01. Fontes: [plano, seções 4 e 7](../docs/plano/v1.2/plano-mestre-v1.2.md).

| Marco | Semana | Resultado planejado |
|---|---|---|
| M1 | 1 | Linha de base, ADRs, spike do provedor, esqueleto integrado e CI |
| M2 | 2 | Turmas/atividades, editor/versões, autenticação e termo |
| M3 | 3 | Comparação, apoio com defesa de autoria, etapas no domínio e avaliação adversarial |
| M4 | 4 | Acompanhamento, submissão, etapas na interface e colagens |
| M5 | 5 | Similaridade e próprios registros; verificação dos RNF; congelamento v0.9.0 |
| M6 | 6 | Estabilização, documentação, demonstração e entrega v1.0.0 |

O prazo de seis semanas é confirmado; a capacidade é planejada com 10 h por pessoa por semana, cuja disponibilidade real ainda requer Q-15. Das 240 h totais, 60 h são eventos, 24 h revisão, 151 h tarefas e 5 h reserva. Frontend tem 38,5 h de tarefas e apenas 0,5 h de reserva. O cronograma é relativo: D0 não foi definido e as datas do Gantt são fictícias. Ordem de corte: RF19 → RF20 → simplificar RF11/RF12 → RF15 → destaque RF18. T38 e T44 foram removidas; T29 foi movida para Semana 5; T60/T61/T63/T65 são novas; T64 é opcional. Fontes: [plano, seção 8](../docs/plano/v1.2/plano-mestre-v1.2.md) e [decisões, seção E](../docs/plano/v1.2/decisoes-plano-v1.2.md).

## Avaliação da hipótese e pendências

A POC mede qualidade comparando primeira versão marcada e final segundo os critérios do professor; autonomia pela proporção de alterações em Reescrever sem pedido em Revisar entre atividades; redução de apoio pela evolução das solicitações e pedidos de escrita; originalidade por similaridade e volume colado, com interpretação humana. O piloto prevê pelo menos três atividades como sugestão, após a entrega, com consentimento e protocolo. Limiares de sucesso, duração, turma e faixa etária ainda dependem de decisão. Fonte: [ERS v2, seções 8–10](../docs/ers/v2/ERS-Grupo8-v2.md) e B11.

Além de B5/B10, continuam questões sobre critérios da disciplina e aceite de prioridades (Q-01), regras documentais herdadas (Q-02), pré-cadastro (Q-04), diff por palavras (Q-10), turma/idade e dados reais (Q-13), modelo e região Bedrock (Q-14, parcialmente respondida), D0/capacidade real (Q-15), retenção (Q-18), piloto/limiares (Q-19) e ajuste do assistente por atividade (Q-20). Hipóteses padrão permitem planejar, mas não são respostas confirmadas. Fontes: [plano, seção 5.8](../docs/plano/v1.2/plano-mestre-v1.2.md) e [ADR-006](../docs/arquitetura/ADR-006-bedrock.md).

## Histórico e limites de interpretação

A ERS v1.0 tinha RF01–RF15 e RN01–RN06, com vedação centrada na geração integral. A v2 amplia e torna verificável a proibição, inclui RF16–RF22, RN07–RN10, RNF, fluxos, salvaguardas e métricas. O plano v1.1 recomendava Ollama local e 144 h de tarefas; a v1.2 usa API externa, amplia o escopo e chega a 151 h. Fontes: [histórico da ERS](../docs/ers/v2/ERS-Grupo8-v2.md), [decisões](../docs/plano/v1.2/decisoes-plano-v1.2.md) e fontes históricas cadastradas em [fontes.json](fontes.json).

As referências a normas ISO são referências de escopo publicado: o plano declara que não consultou o texto integral pago e não afirma conformidade formal. Referências bibliográficas locais não comprovam leitura do conteúdo externo. Este mapa descreve o planejamento, não certifica implementação, conformidade legal ou eficácia pedagógica. Consulte a fonte original e seu estado antes de tomar uma decisão de engenharia.
