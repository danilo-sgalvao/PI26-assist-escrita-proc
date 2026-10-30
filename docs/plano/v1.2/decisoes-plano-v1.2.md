# Decisões para o Plano Mestre v1.2

| Campo | Valor |
|---|---|
| Versão | 0.2 |
| Data | 29/10/2026 |
| Autor | Danilo Galvão (decisões); redação com apoio de IA (Claude) |
| Revisor | — |
| Estado | Aplicado no plano v1.2 (`plano-mestre-v1.2.md` e `.docx`); B5 e B10 pendentes |

Guia para montar o plano v1.2 a partir do plano v1.1 editável. A ERS v2 é a base de requisitos. Este arquivo registra apenas o que muda no **plano**; a ERS não é alterada. As seções A a D são as decisões; a seção E registra as mudanças efetivamente aplicadas.

## A. Mudanças diretas (ERS v2 → plano)

| Seção do plano | Mudança |
|---|---|
| 1. Diagnóstico | Incluir a ERS v2, a POC 2.2 e os slides como documentos de entrada. Acrescentar às lacunas L1–L13 uma coluna "como a ERS v2 resolve". Ficam abertas a granularidade do diff e o L7, que foi resolvido pela decisão B7. |
| 2. Apresentação | Escopo e exclusões passam a seguir a ERS v2. Novos interessados: responsáveis legais e stakeholder da POC. Novos objetivos: etapas e transparência para o aluno. |
| 3. Fundamentação | Novas referências: documento MEC *IA básica* e POC 2.2. |
| 5. Requisitos | A ERS v2 vira a linha de base. A T03 passa a ser "revisar a ERS v2 e derivar HU/CA". Novas HU-17 (etapas) e HU-18 (colagens). Catálogo de regras ganha RN07–RN10. A máquina de estados passa a ter as etapas Planejar → Escrever → Revisar → Reescrever → Submetida. Q-03 a Q-09 e Q-12 ficam marcadas como respondidas; as questões em aberto da ERS são incorporadas. |
| 6. Arquitetura | Modelo de dados ganha turma, etapa na versão, evento de colagem, aceite do termo e devolutiva; a atividade ganha gênero, critérios e política de prazo. A API ganha endpoints de turmas, transição de etapa, colagens, devolutiva, termo e "meus registros". Não há módulo novo. |
| 9. Qualidade | Testes de aceitação para RF16–RF22, verificação WCAG AA e teste de perda máxima no salvamento automático. |
| 11. Rastreabilidade | A matriz ganha RF16–RF22 e RN07–RN10. A ERS v2 passa a ser o D02. |
| 12. Riscos | Três riscos novos: escopo além da capacidade, colagem lida como prova de fraude (mitigado pela RN06) e consentimento não obtido. Os riscos da decisão B1 entram nesta seção. |
| 13. Critérios | Os marcos M1–M6 passam a incluir os requisitos novos. |
| Glossário | Novos termos: etapa, versão automática/marcada, evento de colagem, turma, devolutiva, termo de ciência, descarregamento cognitivo e autonomia progressiva. |

## B. Decisões

| # | Tema | Decisão | Estado |
|---|---|---|---|
| B1 | LLM | **API externa**, como na ERS v2. Substitui o "LLM local" da Tabela 2 do plano v1.1. | Decidido |
| B2 | Fontes da similaridade | **Produções internas** da atividade e respostas do assistente. A base externa, citada pelos stakeholders, vira evolução futura (*Won't* nesta entrega). | Decidido |
| B3 | Salvamento de versões | **ERS:** salvamento automático (1 min) e versão marcada por etapa | Decidido |
| B4 | Após o prazo | **ERS:** configurável pelo professor; o padrão é "aceita e marca atrasada" | Decidido |
| B5 | Critério do RF09 | — | **Pendente** |
| B6 | Categorias de apoio (RF12) | **ERS:** categorias dos slides + "pedido de escrita" | Decidido |
| B7 | Quando a similaridade roda | **ERS:** automática após a submissão | Decidido |
| B8 | Priorização | **MoSCoW.** Conversão: Alta → Must, Média → Should, Baixa → Could. O RF06 passa a Must. | Decidido |
| B9 | RNF | Base RNF01–13 da ERS. Entram RNF14 (tempo da API), RNF15 (substituibilidade do provedor de IA), RNF16 (cobertura/modularidade) e RNF17 (aviso de alteração não salva). | Decidido |
| B10 | Tempo de resposta da IA | — | **Pendente** |
| B11 | Piloto | O plano vai até a demo + protocolo de piloto pronto. O piloto acontece após a entrega, condicionado a aprovação e consentimento. | Decidido |
| B12 | Cronograma | **Fixo** (6 semanas, mesma capacidade). Os requisitos novos se encaixam por priorização e realocação (ver seção C). | Decidido |

### Consequências da B1 (API externa) para o plano

- **Tabela 2 / fatos confirmados:** o fato "LLM local" passa a ser "LLM via API externa".
- **Arquitetura:** a porta do provedor de IA se mantém. Só troca o adaptador: sai o Ollama e entra o cliente da API via Spring AI. O Ollama sai do Docker Compose.
- **Spike T07 e ADR-006:** deixam de escolher um modelo local e passam a escolher provedor e modelo, avaliando custo, termos de uso de dados, latência e qualidade no conjunto do RF09.
- **Privacidade (RNF da ERS):**
  - enviar à API só o texto e o pedido, nunca o nome ou outros identificadores;
  - escolher um provedor que não treine com os dados;
  - o termo de ciência (RF21) informa que o texto é processado por um serviço externo.
- **Segredos:** a chave da API fica fora do repositório, em variável de ambiente ou segredo do GitHub Actions.
- **Testes:** a CI usa um adaptador falso. O conjunto de avaliação do RF09 roda contra a API real, sob demanda, com custo controlado.
- **Riscos novos:** custo/cota, indisponibilidade do provedor, mudança nos termos de uso e dados de menores em serviço de terceiros.
- **Cronograma:** horas de infraestrutura do LLM local que deixam de existir (ex.: Ollama, hardware) voltam para o orçamento. Quantificar com o plano editável.

## C. Encaixe dos requisitos novos no cronograma fixo

| Requisito | Estimativa | MoSCoW |
|---|---|---|
| RF16 (turma, além da T16) | ~2 h | Must |
| RF17 (etapas) | ~8 h | Must |
| RF21 (termo de ciência) | ~3 h | Must |
| RF22 (autenticação) | já coberta | Must |
| RF18 (colagens) | ~5 h | Should |
| RF20 (meus registros) | ~3 h | Should |
| RF19 (devolutiva) | ~3 h | Could |
| **Total** | **~24 h** | |

Fontes de horas, em ordem:
1. Horas liberadas pela B1.
2. Reserva do plano v1.1.
3. Simplificação das válvulas *Should* já previstas (RF11, RF12, RF15).

Se ainda faltar, corta-se primeiro o RF19, depois o RF20.

## D. Pendências

- **B5:** critério do RF09.
- **B10:** tempo de resposta da IA. Com API, os 10 s da ERS são mais viáveis do que eram com LLM local.
- **Provedor e modelo da API:** escolha do spike T07 (ADR-006).

## E. Mudanças aplicadas no plano v1.2

### E.1 Como as pendências ficaram no plano

- **B5:** os CA do RF09 da ERS v2 valem integralmente (≥ 30 pedidos de teste; exemplos sobre outro tema; verificação automática). Os limites de 150 palavras por orientação e de um exemplo de até 25 palavras aparecem como **CA-09.5 (pendente)**. Q-05 continua aberta.
- **B10:** vale o valor da ERS (RNF06: 10 s em 90%, sugerido) até a decisão. O spike T07 mede a latência real. Ver Q-21.

### E.2 Correções na estimativa do cronograma

A estimativa da seção C (~24 h) era grosseira. Refeita tarefa por tarefa, deu outro resultado:

| Item | Horas |
|---|---|
| Trabalho novo: tarefas novas T60, T61, T63, T65 | +8 h |
| Trabalho novo: +0,5 h em 16 tarefas existentes | +8 h |
| Simplificações e remoções | −9 h |
| **Saldo** | **+7 h** (de 144 h para 151 h) |

- **Fora da conta:** o RF19 (3 h) foi para a tarefa T64, que não entra na base, e os aceites/HU foram absorvidos pelas tarefas da área A.
- **B1 liberou só 1,5 h** (T07 −1 h, T49 −0,5 h), menos do que eu tinha sugerido.
- **Reserva:** caiu de 12 h para 5 h. Por área: A 1,5 h, **B 0,5 h**, C 1,5 h, D 1,5 h.
- **Carga semanal:** nenhuma área passa de 6,5 h de tarefas em nenhuma semana.

### E.3 Trocas que reduzem margem ou mudam a ordem (a equipe deve conferir)

| Mudança | Efeito |
|---|---|
| **T38 removida** (n-gramas persistidos) | Os n-gramas passam a ser calculados na hora, dentro de T45. Para uma turma de demonstração o volume é pequeno. |
| **T44 removida** (testes de componentes críticos, 1,5 h) | Os testes de componente passam a ser feitos dentro de cada tarefa, como a DoD já exige. Perde-se a passada final dedicada. |
| **T47 reduzida** (−1 h) | O resultado da similaridade fica em JSONB. |
| **T28 reduzida** (−0,5 h) | As entidades já são modeladas em T09. |
| **T30 reduzida** (−0,5 h) | A ERS v2 (seção 8) já operacionaliza os indicadores. |
| **T34 reduzida** (−1 h) | Os indicadores do estudante saíram da tela de submissão e foram para T65 (meus registros), junto com o RF20. |
| **T42 reduzida** (−0,5 h) | O relatório de similaridade na interface fica mais simples. |
| **Etapas (RF17) em duas sprints** | O domínio vem na Semana 3 (T61, área D) e a interface por etapas na Semana 4 (T60, área B). **A demonstração das etapas só acontece em M4.** Não coube antes sem tirar algo do frontend nas Semanas 2 e 3. |
| **Tela de turma simples** | Fica dentro de T14. A gestão completa de turma não tem tarefa própria. |
| **T29 movida** (backup e dados de demonstração) | Sai da Semana 3 para a Semana 5, para abrir espaço para T61. |
| **Ordem da Semana 5 da área A** | Passa a ser T41 → T39 → T40, porque T39 depende de T65. |
| **RF20 em duas áreas** | A consulta fica com D (dentro de T37) e a tela com B (T65). |

### E.4 Outras mudanças no plano por seção

**Capa e convenções**
- Versão 1.2.
- Novos documentos de entrada: ERS v2.0, POC 2.2 e slides.
- Novo rótulo "Decisão da equipe (Bnn)".

**1. Diagnóstico**
- Parágrafo sobre as novas fontes.
- Tabela de fatos confirmados refeita: RF01–RF22, RN01–RN10, RNF01–RNF13, hipótese, risco, plano da POC e LLM por API.
- Lacunas L1–L14 ganham a coluna "Situação com a ERS v2".
- RT-04 reescrita para API com RNF04; nova RT-06 (consentimento e termo).
- Nova seção 1.7 com a tabela B1–B12.

**2. Planejamento**
- Contexto com a hipótese e o limite declarado (B11).
- Objetivos reescritos (6).
- Escopo e exclusões revistos.
- Premissas:
  - PR-01 confirmada;
  - PR-03 passa a tratar do provedor de API;
  - PR-05 segue B11;
  - nova DP-04 (conta e crédito na API).
- Novos stakeholders: stakeholder da POC, responsáveis legais e provedor de LLM.

**3. Fundamentação**
- Fichas 29148, 42010, 25010, arquitetura e segurança ajustadas.
- Novas referências: [49] POC, [50] MEC, [51] slides, [52] WCAG 2.1.
- [28] passa a ser Spring AI Chat Model; [29] Ollama fica como contingência.

**4. Metodologia**
- MoSCoW nova:
  - *Must*: RF01–RF10, RF13, RF14, RF16, RF17, RF21, RF22;
  - *Should*: RF11, RF12, RF15, RF18, RF20;
  - *Could*: RF19;
  - *Won't*: base externa e piloto dentro das 6 semanas.
  - **RF16 é exceção**: Média na ERS, mas *Must* aqui, porque sustenta a visibilidade por turma.
- Sprint goals e visão por semana refeitos.
- DoD cita a chave da API.

**5. Requisitos**
- T03 passa a ser "revisar a ERS v2".
- HU/CA:
  - HU-01, HU-04, HU-09, HU-14 e HU-15 reescritas;
  - novas HU-17 (etapas) e HU-18 (colagens).
- Tabela de RNF:
  - RNF01–RNF13 da ERS, mais RNF14–RNF17 do plano;
  - correspondência com os antigos RNF-01..10.
- RN07–RN10 com mecanismos.
- Máquina de estados com as etapas.
- Perguntas:
  - Q-01 a Q-16 com coluna de situação (várias respondidas pela ERS);
  - novas Q-17 a Q-20 (vindas da ERS) e Q-21 (B10).
- Roteiro R2 vira "revisão da ERS v2".

**6. Arquitetura**
- Drivers e preocupações com RNF04 e RNF07/RNF08.
- C4 nos níveis 1 a 3 sem Ollama, com o provedor por API.
- Módulos ganham turmas, etapas, colagens, termo, devolutiva e meus registros.
- Modelo de dados com turma, etapa, transição, colagem, termo e devolutiva, em duas figuras.
- Sequência do apoio com:
  - classificação da solicitação e recusa (FA01);
  - indisponibilidade do provedor (FA04);
  - validação reprovada (FA02).
- Defesa em camadas:
  - camada 1 vira classificação automática;
  - camada 3 inclui minimização dos dados.
- Similaridade automática por evento de submissão, com resumo de colagens.
- Seção 6.7.5 reescrita para provedor por API.
- Compose sem Ollama; linha de acessibilidade (axe).
- ADR-006 redefinido; novo ADR-009 (versões automáticas e marcadas).
- Contrato da API com termo, turmas, etapa, colagens, meus registros e devolutiva. O POST de similaridade foi removido.

**8. Cronograma**
- Tabelas de capacidade, horas por área e sensibilidade refeitas.
- Ordem de corte: RF19 → RF20 → RF11/RF12 → RF15 → destaque do RF18.
- Gantt em Mermaid, com datas fictícias explicadas no texto.
- Nova tabela de mudanças tarefa a tarefa (8.5).

**9. Qualidade**
- Avaliação do assistente com:
  - ≥ 30 pedidos de escrita/reescrita;
  - ≥ 12 casos legítimos pelas categorias da ERS;
  - ≥ 4 casos de RN07/RN08;
  - custo registrado.
- Metas de 0 identificadores no *payload* e cobertura das transições de etapa.
- Nova linha de acessibilidade.
- Tabela de requisitos × testes com RF16–RF22.

**10. Versionamento**
- Pastas de `docs/` alinhadas à organização atual (`referencias/`, `plano/`, `ers/`, …), sem os números.
- *Workflow* manual de avaliação contra a API real; CI usa adaptador falso.
- Chave da API com limite de gasto.

**11. Documentos**
- ERS v2.x como D02.
- Novos D17 (este arquivo) e D18 (protocolo do piloto).
- Matriz de rastreabilidade com RF16–RF22 e a nova MoSCoW (RF06 vira *Must*).

**12. Riscos**
- R01 vira custo/cota/indisponibilidade da API.
- Novos: R14 (dados no provedor), R15 (capacidade, área B), R16 (colagem lida como fraude), R17 (consentimento).
- R13 inclui falta de internet na demonstração.

**13. Critérios**
- Marcos M1–M6 atualizados.
- RN01–RN10.
- Três contêineres.
- D17 e D18 no pacote de entrega.

**Apêndices**
- Novo registro de uso de IA para a v1.2.
- Glossário com turma, etapa, versão automática/marcada, colagem, provedor de LLM, termo, devolutiva, descarregamento cognitivo, autonomia progressiva e piloto.

**Diagramas**
- As 10 figuras da v1.1 foram refeitas em Mermaid. O modelo de dados virou duas figuras, então agora são 11.
- O `.docx` usa as imagens renderizadas; o `.md` mantém o código Mermaid como fonte.

### E.5 Divergência que continua aberta na ERS

O RF15 da ERS v2 ainda cita "base externa de referência", adiada pela decisão B2. O plano registra a divergência (seção 5.9, R2), mas **a ERS não foi alterada**. Mudá-la depende de decisão do grupo.
