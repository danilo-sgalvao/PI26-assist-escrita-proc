# Assistente de Escrita Processual — Grupo 8

Trabalho da disciplina **Manutenção de Software** (UFG, 6º semestre). Prova de conceito (POC 2.2) de uma plataforma em que o estudante escreve o próprio texto e uma IA **orienta sem escrever**, enquanto o professor acompanha o processo (versões, interações, evolução).

**Equipe:** Danilo Galvão, Enzo Machado, Felipe Nunes, Luiz Augusto Godinho.
**Idioma:** todo o conteúdo (documentos, código, commits, issues) é em português do Brasil.

## Arquivos da pasta

Todos os documentos ficam em `docs/`, que já corresponde à pasta `docs/` do futuro monorepo. Organização:
- `referencias/`: material externo ou apresentado, somente leitura;
- `ers/`: uma subpasta por versão da ERS;
- `plano/`: uma subpasta por versão do plano.

Versões antigas não são apagadas nem sobrescritas.

| Arquivo | O que é | Situação |
|---|---|---|
| `docs/referencias/POC 2.2. Assistente de escrita processual.pdf` | Enunciado da POC: risco moderado, hipótese, salvaguardas, requisitos de dados e métricas de saída | Fonte externa (não editar) |
| `docs/referencias/AssistentedeEscritaProcessual_2.pdf` | Slides apresentados ao stakeholder (linguagem não técnica) | Referência |
| `docs/ers/v1.0/ESPECIFICAÇÃO DE REQUISITOS DE SOFTWARE – ERS GRUPO 8.pdf` | ERS v1.0 original: RF01–RF15, RN01–RN06 | Superada pela v2 |
| `docs/ers/v2/ERS-Grupo8-v2.md` | ERS v2.0 revisada; **o `.md` é a fonte** | Base de requisitos; em revisão pela equipe |
| `docs/ers/v2/ERS-Grupo8-v2.docx` | Versão Word gerada a partir do `.md` (capa, sumário, A4) | Regerar sempre que o `.md` mudar |
| `docs/plano/v1.1/PDS_Assistente_Escrita_Processual_v1.1.docx` | Plano mestre v1.1 editável (Word) | Base para a v1.2; não editar |
| `docs/plano/v1.1/Plano_Mestre_Assistente_Escrita_Processual_v1.1.pdf` | PDF do plano mestre v1.1 (processo, arquitetura, stack, cronograma, qualidade, riscos) | Proposta para aprovação da equipe e do professor |
| `docs/plano/v1.2/decisoes-plano-v1.2.md` | Decisões B1–B12 e registro das mudanças aplicadas no plano v1.2 (seção E) | B5 e B10 pendentes |
| `docs/plano/v1.2/plano-mestre-v1.2.md` | Plano mestre v1.2, enriquecido com a ERS v2; **o `.md` é a fonte** (diagramas em Mermaid) | Proposta para aprovação da equipe e do professor |
| `docs/plano/v1.2/plano-mestre-v1.2.docx` | Versão Word gerada a partir do `.md` (diagramas renderizados, sumário, tabelas largas em paisagem) | Regerar sempre que o `.md` mudar |

O texto da POC é curto. O documento complementar dela é https://www.gov.br/mec/pt-br/escolas-conectadas/arquivos/ia-basica.pdf.

## Hipótese e regras centrais

- **Hipótese da POC:** acompanhar a escrita por etapas desenvolve autoria e autorregulação sem gerar dependência nem plágio assistido.
- **Métricas:** qualidade da produção final, autonomia progressiva (redução do apoio solicitado ao longo das atividades) e originalidade verificada.
- **Regras que não se negociam:** a IA não escreve, não reescreve, não completa nem parafraseia o texto do aluno (RN01/RN02); o histórico de versões nunca é apagado (RN04); indicadores não viram nota, ranking ou vigilância (RN05); a similaridade apenas apoia a avaliação, e quem decide sobre originalidade é o professor (RN06).

## Fatos confirmados pela equipe (não mudar sem aprovação)

- Prazo de **6 semanas** até a entrega final; quatro integrantes.
- Frontend em **React + TypeScript**.
- Assistente baseado em **LLM acessado por API externa** (decisão B1, 29/10/2026, que substitui o "LLM local" do plano v1.1). Provedor e modelo serão escolhidos no spike T07 (ADR-006). Por isso valem três cuidados:
  - nunca enviar nome ou outros identificadores do aluno à API;
  - usar provedor que não treine com os dados;
  - o termo de ciência (RF21) informa o processamento externo.
- Persistência e acesso a dados em **Java** (exigência do enunciado).
- Similaridade (RF15) compara a produção com **textos internos** (outras produções da atividade) e com as **respostas do assistente** (decisão B2). Base externa e serviço antiplágio ficam como evolução futura (*Won't* nesta entrega), mesmo os stakeholders tendo citado produção externa.

## Propostas do plano mestre (valem até virar ADR ou mudança aprovada)

- **Processo:** iterativo, baseado em Scrum, com sprints de 1 semana e quadro Kanban (WIP ≤ 4 em desenvolvimento e ≤ 4 em revisão). Marcos M1–M6, um por semana. Cronograma relativo (Semana 1–6, dias D1–D5), porque D0 ainda não foi definido.
- **Áreas e revisão em anel:** A = Requisitos/Produto/Qualidade (Product Owner), B = Frontend, C = Backend/API/Assistente, D = Persistência/Dados/Infra. Anel de revisão A→B→C→D→A; o autor nunca aprova o próprio trabalho. Ainda falta definir quem fica em cada área (tarefa T01).
- **Arquitetura:** SPA + monólito modular com portas e adaptadores. Módulos: `identidade`, `atividades`, `producao`, `apoio`, `acompanhamento`, `similaridade`, `compartilhado`.
- **Stack:**
  - Java 25 + Spring Boot 4.x (Maven); Spring Data JPA/Hibernate, PostgreSQL 18 e Flyway;
  - Spring Security com sessão, cookie HttpOnly e CSRF;
  - Spring AI com adaptador para a API externa de LLM (provedor e modelo definidos no spike T07, ADR-006); na CI, adaptador falso, e a chave da API fica fora do repositório;
  - java-diff-utils para o diff por palavras;
  - Vite, Vitest e Testing Library no frontend;
  - JUnit, Testcontainers e ArchUnit no backend;
  - GitHub Actions; Docker Compose local.
- **Defesa da RN02 em camadas:** classificação da solicitação (pedido de escrita recebe recusa explícita), prompt de sistema versionado, texto do aluno delimitado e sem identificadores, validador determinístico de saída (`GuardrailDeAutoria`), registro de bloqueios e proteção do prompt. O validador é a garantia final, não o prompt.
- **Similaridade:** contenção de n-gramas de palavras (n = 5), sem veredito de plágio.
- **Versões:** imutáveis (append-only, com UPDATE/DELETE bloqueados no banco); o progresso é calculado a partir delas, sem tabela duplicada.

## Convenções

- **IDs:**
  - RF01–RF15 e RN01–RN06 mantêm a numeração da ERS original; itens novos são acrescentados ao final da sequência.
  - Demais prefixos: HU-nn / CA-nn.m, Q-xx / H-xx, ADR-nnn, Tnn, CT-nn.m, DEF-nnn, Rnn, MUD-nnn.
  - O nome do teste cita o CA (ex.: `deveRejeitarEdicaoAposSubmissao_CA14_2`).
- **Valores numéricos ainda não validados** aparecem marcados como *(sugerido)* ou "proposta".
- **Git (quando o repositório existir):**
  - monorepo `backend/`, `frontend/`, `infra/`, `docs/`, `.github/`;
  - GitHub Flow com branches `tipo/Txx-descricao` de no máximo 2 dias e squash merge;
  - Conventional Commits em português citando a issue (`feat(apoio): valida limite de palavras (#26)`);
  - PR segue o modelo do Apêndice C do plano, com a seção "Design do incremento".
- **Documentos:** em Markdown, com cabeçalho de título, versão, data, autor, revisor e estado. Uso de IA é sempre declarado (Apêndice D do plano).

## Hierarquia entre os documentos

1. **Fatos confirmados pela equipe** (seção acima) valem sobre tudo.
2. **ERS v2** (`docs/ers/v2/ERS-Grupo8-v2.md`, versão 2.0) é a base de requisitos. O plano mestre **não** está acima dela. Não editar a ERS sem pedido explícito: divergências com o plano ou com os fatos confirmados são levadas ao grupo, não corrigidas por conta própria. A divergência conhecida hoje: o RF15 da ERS cita base externa na similaridade, mas a decisão B2 limita a similaridade a textos internos.
3. **Plano mestre** define processo, arquitetura, stack e cronograma. Versão vigente: **plano v1.2** (`docs/plano/v1.2/plano-mestre-v1.2.md`), já enriquecido com a ERS v2. O que mudou em relação à v1.1, e por quê, está em `docs/plano/v1.2/decisoes-plano-v1.2.md`.

## Pontos de atenção

- O **cronograma é fixo** (B12): 6 semanas, 10 h por pessoa por semana. A v1.2 tem 151 h de tarefas (a v1.1 tinha 144 h) e 5 h de reserva. A área B (frontend) só tem 0,5 h de reserva. Nenhuma área passa de 6,5 h de tarefas por semana.
- **Prioridades (MoSCoW):**
  - *Must*: RF01–RF10, RF13, RF14, RF16, RF17, RF21, RF22;
  - *Should*: RF11, RF12, RF15, RF18, RF20;
  - *Could*: RF19 (tarefa T64, fora da base).
- **Ordem de corte:** RF19 → RF20 → RF11/RF12 → RF15 → destaque do RF18.
- As etapas (RF17) só aparecem na interface na Semana 4 (M4).
- **Tarefas novas:** T60, T61, T63, T64, T65. **Tarefas removidas:** T38 e T44.
- **Regerar o `.docx` do plano:** usar o conversor do Markdown com Mermaid renderizado pelo mermaid-cli (Chrome local) e atualizar o sumário no Word. Os scripts ficam no scratchpad da sessão, não no repositório.
- Divergências entre ERS v2 e plano v1.1 já decididas a favor da ERS:
  - salvamento automático + versões marcadas por etapa;
  - prazo configurável pelo professor (padrão: aceita e marca atrasada);
  - categorias de apoio dos slides + "pedido de escrita";
  - similaridade automática após a submissão.

  A priorização segue MoSCoW (Alta → Must, Média → Should, Baixa → Could; RF06 é Must). Os RNF partem dos RNF01–13 da ERS, mais RNF14–17 vindos do plano.
- Pendentes: critério do RF09 (B5) e tempo de resposta da IA (B10).
- O piloto com turma fica para depois da entrega. Nas 6 semanas, o plano entrega a demo e o protocolo do piloto.
- Ainda não existe código nem repositório git nesta pasta. Por enquanto ela só contém documentos.
