# Especificação de Requisitos de Software (ERS)

**Sistema:** Assistente de Escrita Processual
**Grupo 8:** Enzo Machado, Danilo Galvão, Luiz Augusto Godinho, Felipe Nunes
**Disciplina:** Manutenção de Software
**Versão:** 2.0 (revisão da versão 1.0)

---

## 1. Introdução

### 1.1 Propósito

Este documento especifica os requisitos do **Assistente de Escrita Processual**, desenvolvido como prova de conceito (POC 2.2) para apoiar a produção textual de estudantes. É destinado à equipe de desenvolvimento, aos professores participantes e ao stakeholder responsável pela avaliação da POC.

### 1.2 Escopo

O sistema acompanha a escrita como **processo**, e não apenas como produto. O estudante escreve o próprio texto na plataforma, passando pelas etapas de **planejar, escrever, revisar e reescrever**, e pode pedir orientação a um assistente de IA que **orienta, mas não escreve**. O professor acompanha as versões, as interações com o assistente e a evolução do estudante ao longo das atividades.

**Dentro do escopo**

- Cadastro de turmas e atividades de produção textual pelo professor.
- Editor de texto com salvamento automático e versões por etapa.
- Assistente de IA restrito a orientações, perguntas e apontamentos.
- Registro do processo de escrita (versões, etapas, interações, colagens de texto).
- Painel de acompanhamento para o professor.
- Submissão da versão final e verificação de similaridade.
- Indicadores para avaliar a hipótese da POC.

**Fora do escopo**

- Atribuição automática de notas ou conceitos.
- Rankings ou comparações públicas entre estudantes.
- Afirmação conclusiva de plágio ou de uso de IA externa (o sistema apenas fornece indícios ao professor).
- Integração com ambientes virtuais de aprendizagem (AVA) ou sistemas acadêmicos.
- Correção ortográfica e gramatical automática do texto do estudante.

### 1.3 Definições

| Termo | Definição |
|---|---|
| **Atividade** | Proposta de produção textual criada pelo professor, com tema, gênero, orientações, critérios de avaliação e prazo. |
| **Produção** | Texto de um estudante vinculado a uma atividade. |
| **Etapa** | Fase do processo de escrita: Planejar, Escrever, Revisar ou Reescrever. |
| **Versão** | Registro do conteúdo da produção em um instante. Pode ser **automática** (salvamento periódico) ou **marcada** (criada pelo estudante ao concluir uma etapa). |
| **Interação** | Par formado por uma solicitação do estudante ao assistente e a resposta do assistente. |
| **Evento de colagem** | Inserção de texto no editor por meio de colar (Ctrl+V ou equivalente). |
| **Descarregamento cognitivo** | Transferência para a IA do esforço intelectual que deveria ser do estudante (planejar, formular, revisar). |
| **Autonomia progressiva** | Redução, ao longo das atividades, da dependência do estudante em relação ao assistente. |

### 1.4 Referências

- POC 2.2: Assistente de escrita processual (classificação de risco, hipótese, salvaguardas, requisitos de dados e métricas).
- MEC, *Escolas Conectadas: IA básica*. Disponível em: https://www.gov.br/mec/pt-br/escolas-conectadas/arquivos/ia-basica.pdf
- Apresentação ao stakeholder: *Assistente de Escrita Processual*, Grupo 8.
- Lei nº 13.709/2018, Lei Geral de Proteção de Dados Pessoais (LGPD).

---

## 2. Descrição Geral

### 2.1 Problema

Quando a IA escreve pelo estudante, ele deixa de passar pelas etapas em que se aprende: planejar, formular e revisar as próprias ideias. Além disso, o professor só vê o produto final e não consegue saber como o texto foi construído nem onde o aluno precisou de ajuda.

### 2.2 Hipótese da POC

> O acompanhamento por etapas desenvolve autoria e autorregulação sem gerar dependência ou plágio assistido.

Os requisitos deste documento existem para (a) oferecer esse acompanhamento e (b) coletar os dados necessários para confirmar ou refutar a hipótese (ver Seção 8).

### 2.3 Classificação de risco

A POC tem **risco moderado** (coorte de entrada 2). Por isso, este documento inclui requisitos de privacidade, transparência e salvaguardas que limitam a atuação da IA (Seções 5 e 7).

### 2.4 Atores

| Ator | Descrição |
|---|---|
| **Estudante** | Escreve, revisa e submete a produção. Pode solicitar orientação ao assistente e consultar o próprio histórico. |
| **Professor** | Cria turmas e atividades, acompanha o processo dos estudantes e é o único responsável pela avaliação. |
| **Assistente de Escrita** | Componente de IA que fornece orientações, perguntas e apontamentos, respeitando as restrições de autoria (RN01, RN02). |

### 2.5 Premissas e restrições

- O assistente utiliza um modelo de linguagem acessado por API externa; as instruções de comportamento e os filtros de saída ficam sob controle da equipe.
- Na POC, o sistema é acessado via navegador web, em computador.
- Os estudantes participantes podem ser menores de idade; a participação depende de consentimento (RNF02).
- O idioma do sistema e do assistente é o português brasileiro.

---

## 3. Requisitos Funcionais

Prioridade: **Alta** (essencial para a demonstração), **Média** (essencial para o piloto), **Baixa** (desejável).

Os identificadores RF01 a RF15 foram mantidos da versão 1.0 para preservar a rastreabilidade; RF16 em diante são novos.

### 3.1 Gestão de turmas e atividades

#### RF16 – Gerenciar turma *(novo)*
**Prioridade:** Média
O sistema deverá permitir que o professor crie uma turma e inclua estudantes nela, de modo que cada atividade seja disponibilizada apenas aos estudantes da turma correspondente.
**Critérios de aceitação**
- O professor consegue criar uma turma e adicionar estudantes.
- Um estudante só visualiza atividades das turmas a que pertence.
- Um professor só visualiza produções das próprias turmas.

#### RF01 – Criar atividade de escrita
**Prioridade:** Alta
O sistema deverá permitir que o professor cadastre uma atividade de produção textual informando: título, tema, **gênero textual**, descrição, orientações, **critérios de avaliação** e prazo.
**Critérios de aceitação**
- Título, tema, gênero e prazo são obrigatórios.
- O gênero e as orientações informados ficam disponíveis ao assistente como contexto (RF08).
- Os critérios de avaliação ficam disponíveis ao professor para comparar a primeira versão com a final (Seção 8).

### 3.2 Produção textual e etapas

#### RF02 – Iniciar produção textual
**Prioridade:** Alta
O sistema deverá permitir que o estudante inicie uma produção vinculada a uma atividade disponível, desde que o prazo não tenha expirado. A produção inicia na etapa **Planejar**.

#### RF17 – Conduzir a produção por etapas *(novo)*
**Prioridade:** Alta
O sistema deverá organizar a produção nas etapas **Planejar → Escrever → Revisar → Reescrever**, indicando ao estudante em qual etapa ele está.
- **Planejar:** espaço para o estudante registrar tese, ideias e estrutura pretendida.
- **Escrever:** redação do texto pelo estudante.
- **Revisar:** o estudante relê o texto e pode solicitar apontamentos do assistente.
- **Reescrever:** o estudante decide o que alterar e como, a partir das próprias observações e das orientações recebidas.

**Critérios de aceitação**
- O estudante avança de etapa por ação explícita; cada avanço gera uma versão marcada (RF04).
- O estudante pode voltar a uma etapa anterior (por exemplo, de Revisar para Escrever); a volta também é registrada.
- O ciclo Revisar → Reescrever pode se repetir quantas vezes o estudante quiser antes da submissão.

#### RF03 – Editar produção textual
**Prioridade:** Alta
O sistema deverá disponibilizar um editor no qual o estudante escreve, altera e reorganiza o próprio texto.
**Critérios de aceitação**
- O editor não insere conteúdo gerado pelo assistente; não existe botão de "aplicar sugestão".
- O texto é salvo automaticamente (RF04).

#### RF18 – Registrar eventos de colagem *(novo)*
**Prioridade:** Média
O sistema deverá registrar cada evento de colagem no editor, armazenando o trecho colado, sua quantidade de caracteres, a data e o horário e a etapa em que ocorreu.
**Critérios de aceitação**
- A colagem não é bloqueada; o estudante pode colar o próprio texto vindo de outro lugar.
- O estudante é informado, no termo de ciência (RF21), de que colagens são registradas.
- Colagens acima de um limite configurável (sugestão: 200 caracteres) são destacadas para o professor no painel (RF13).

> **Justificativa:** a hipótese da POC inclui "sem plágio assistido". Sem esse registro, um texto gerado em uma IA externa e colado na plataforma seria indistinguível de um texto escrito pelo estudante.

### 3.3 Versões

#### RF04 – Salvar versões do texto
**Prioridade:** Alta
O sistema deverá registrar versões da produção de dois tipos:
- **Automáticas**, em intervalos regulares enquanto houver alterações (sugestão: a cada 1 minuto);
- **Marcadas**, ao avançar de etapa (RF17), por ação do estudante e na submissão (RF14).

Cada versão armazena o conteúdo, a data, o horário, o tipo e a etapa correspondente.

#### RF05 – Consultar histórico de versões
**Prioridade:** Alta
O sistema deverá permitir que o estudante e o professor consultem as versões anteriores, com filtro por etapa e por tipo (automática ou marcada).

#### RF06 – Comparar versões do texto
**Prioridade:** Alta
O sistema deverá permitir comparar duas versões quaisquer lado a lado, destacando inserções, exclusões e alterações.
**Critérios de aceitação**
- Por padrão, a comparação sugerida ao professor é **primeira versão marcada × versão final**.
- Trechos originados de eventos de colagem (RF18) aparecem identificados na comparação.

### 3.4 Assistente de escrita

#### RF07 – Solicitar apoio do assistente
**Prioridade:** Alta
O sistema deverá permitir que o estudante solicite apoio em qualquer etapa, por mensagem livre, podendo selecionar o trecho do texto ao qual a dúvida se refere.

#### RF08 – Fornecer orientações sobre a escrita
**Prioridade:** Alta
O assistente deverá fornecer orientações sobre **estrutura e organização, coesão e coerência, argumentação e adequação ao gênero**, considerando o tema, o gênero e as orientações da atividade (RF01) e a etapa atual (RF17).
**Formas de resposta permitidas**
- Perguntas que levem o estudante a refletir (ex.: "Sua conclusão retoma a tese da introdução?").
- Apontamentos que localizam um problema sem resolvê-lo (ex.: "O segundo parágrafo introduz uma ideia que não é desenvolvida").
- Explicações de conceitos (ex.: o que é um argumento de autoridade).

#### RF09 – Restringir a geração de conteúdo pelo assistente
**Prioridade:** Alta
O assistente **não deverá** produzir texto que possa ser incorporado à produção do estudante. Isso inclui reescrever, completar, resumir em forma de texto pronto ou parafrasear trechos do estudante, bem como redigir introduções, conclusões, parágrafos ou frases sobre o tema da atividade.
Quando o estudante solicitar esse tipo de conteúdo, o assistente deverá recusar de forma explícita e oferecer orientação no lugar (conforme o exemplo do slide 04 da apresentação).
**Critérios de aceitação**
- Exemplos ilustrativos, quando usados para explicar um conceito, devem tratar de **tema diferente** do da atividade.
- Toda resposta passa por verificação automática antes de ser exibida (RNF05); respostas reprovadas são substituídas por uma orientação genérica e registradas.
- Em um conjunto de teste com pelo menos 30 pedidos de escrita ou reescrita (diretos e disfarçados), **nenhuma** resposta contém texto aproveitável na produção.

#### RF10 – Registrar interações com o assistente
**Prioridade:** Alta
O sistema deverá armazenar cada interação: solicitação do estudante, trecho selecionado (se houver), resposta do assistente, etapa, data e horário, e se a resposta foi uma recusa (RF09).

#### RF12 – Classificar e acompanhar o apoio solicitado
**Prioridade:** Média
O sistema deverá classificar cada solicitação em uma categoria (**estrutura e organização, coesão e coerência, argumentação, adequação ao gênero, pedido de escrita ou reescrita, outro**) e calcular, por estudante e por atividade, a quantidade de solicitações por categoria e por etapa.
**Critérios de aceitação**
- É possível visualizar a evolução desses números de uma atividade para a seguinte.
- Pedidos de escrita ou reescrita aparecem separados, por indicarem tentativa de descarregamento cognitivo.

### 3.5 Acompanhamento

#### RF11 – Registrar o progresso da produção textual
**Prioridade:** Média
O sistema deverá registrar, para cada produção: tempo em cada etapa, número de versões, volume de alterações entre versões, interações (RF10) e eventos de colagem (RF18).

#### RF13 – Painel de acompanhamento do professor
**Prioridade:** Alta
O sistema deverá oferecer ao professor um painel por atividade e por estudante contendo:
- situação da produção (etapa atual, submetida ou não);
- histórico e comparação de versões (RF05, RF06);
- interações com o assistente, mostrando em que pontos o aluno pediu ajuda e que orientação recebeu (RF10);
- indicadores de apoio solicitado ao longo das atividades (RF12);
- eventos de colagem destacados (RF18);
- resultado da verificação de similaridade (RF15).

**Critérios de aceitação**
- O painel não apresenta ranking nem ordenação de estudantes por indicador (RN05).
- Indicadores são apresentados como informação de apoio, sem rótulos de julgamento (ex.: "dependente", "suspeito").

#### RF19 – Registrar devolutiva do professor *(novo)*
**Prioridade:** Baixa
O sistema deverá permitir que o professor registre comentários sobre o processo e sobre a versão final, visíveis ao estudante.

> **Justificativa:** a apresentação destaca que "as devolutivas podem tratar do processo, e não só do produto".

#### RF20 – Consultar os próprios registros *(novo)*
**Prioridade:** Média
O sistema deverá permitir que o estudante visualize tudo o que é registrado sobre sua produção: versões, interações, eventos de colagem e indicadores.

### 3.6 Submissão e originalidade

#### RF14 – Submeter a versão final
**Prioridade:** Alta
O sistema deverá permitir que o estudante submeta a versão definitiva para avaliação do professor até o prazo da atividade, mantendo todas as versões anteriores.
**Critérios de aceitação**
- Após a submissão, a produção fica bloqueada para edição.
- Submissões após o prazo são permitidas ou bloqueadas conforme configuração do professor na atividade.

#### RF15 – Verificar similaridade e originalidade do texto
**Prioridade:** Média
O sistema deverá, após a submissão, comparar a versão final com:
- as produções dos demais estudantes da mesma atividade; e
- uma base externa de referência *(a definir; ver Seção 10)*.

E apresentar ao professor os trechos similares encontrados, o percentual de similaridade e as fontes correspondentes, junto com o resumo dos eventos de colagem (RF18).
**Critérios de aceitação**
- O resultado é apresentado como **apoio**; o sistema não classifica o texto como "original" ou "plagiado" (RN06).

### 3.7 Transparência e acesso

#### RF21 – Termo de ciência e consentimento *(novo)*
**Prioridade:** Alta
No primeiro acesso, o sistema deverá apresentar ao estudante, em linguagem simples, o que é registrado (versões, interações, colagens, tempo por etapa), quem tem acesso e para que os dados são usados. O uso da plataforma depende do aceite e, para menores de idade, da existência de consentimento do responsável.

#### RF22 – Autenticação por perfil *(novo)*
**Prioridade:** Alta
O sistema deverá exigir autenticação e diferenciar os perfis de estudante e professor, liberando apenas as funções e os dados correspondentes a cada perfil.

---

## 4. Regras de Negócio

| ID | Regra | Descrição |
|---|---|---|
| **RN01** | Preservação da autoria | Todo o conteúdo da produção deve ser escrito pelo estudante. O sistema não oferece meios de inserir no texto conteúdo gerado pelo assistente. |
| **RN02** | Vedação de produção de texto pelo assistente | O assistente não redige, reescreve, completa nem parafraseia texto do estudante ou sobre o tema da atividade (RF09). |
| **RN03** | Registro do processo de escrita | Versões, etapas, interações com o assistente e eventos de colagem devem ser registrados. |
| **RN04** | Manutenção do histórico | Versões e registros não podem ser editados nem excluídos pelo estudante ou pelo professor durante o período da POC. |
| **RN05** | Uso pedagógico dos dados | Os dados de uso servem ao acompanhamento do estudante. Não podem ser usados como critério automático de avaliação, para gerar rankings ou para vigilância. |
| **RN06** | Avaliação humana da originalidade | A verificação de similaridade e os eventos de colagem são apenas indícios; cabe ao professor avaliar a originalidade e a autoria. |
| **RN07** *(nova)* | Avaliação exclusiva do professor | O assistente não atribui notas, conceitos nem julgamentos de aprovação sobre o texto. |
| **RN08** *(nova)* | Respeito ao estilo e à variação linguística | O assistente avalia o texto como um todo e não trata escolhas criativas, de estilo ou de variação linguística como erro, salvo quando a orientação da atividade exigir explicitamente a norma-padrão. |
| **RN09** *(nova)* | Sem modelo pronto | O assistente orienta por perguntas e apontamentos e não oferece texto-modelo sobre o tema, evitando a padronização dos textos. |
| **RN10** *(nova)* | Transparência ao estudante | O estudante deve saber o que é registrado e poder consultar os próprios registros (RF20, RF21). |

---

## 5. Requisitos Não Funcionais

Valores marcados com *(sugerido)* devem ser validados com o stakeholder.

| ID | Categoria | Requisito |
|---|---|---|
| **RNF01** | Privacidade | O tratamento de dados deve seguir a LGPD: coletar apenas os dados necessários aos requisitos deste documento, definir prazo de retenção ao fim da POC e **pseudonimizar** os dados usados na análise dos resultados. |
| **RNF02** | Privacidade | Para estudantes menores de idade, a participação depende do consentimento do responsável legal, obtido antes do primeiro acesso. |
| **RNF03** | Segurança | O professor acessa apenas dados das próprias turmas e o estudante apenas os próprios dados. A comunicação deve usar HTTPS e as senhas devem ser armazenadas com hash. |
| **RNF04** | Privacidade | Os textos enviados à API do modelo de linguagem não devem conter dados de identificação do estudante (nome, e-mail, matrícula). O provedor escolhido não deve usar os dados para treinamento. |
| **RNF05** | Confiabilidade do assistente | Toda resposta do assistente passa por uma verificação automática antes de ser exibida, que detecta texto aproveitável na produção (ex.: alta sobreposição com o texto do estudante ou trechos longos de prosa sobre o tema). |
| **RNF06** | Desempenho | O assistente deve responder em até 10 segundos em 90% das solicitações *(sugerido)*. |
| **RNF07** | Confiabilidade | Em caso de falha, a perda máxima de texto do estudante é de 1 minuto de edição (intervalo do salvamento automático) *(sugerido)*. |
| **RNF08** | Disponibilidade | Se o assistente estiver indisponível, o estudante deve continuar podendo escrever e salvar normalmente. |
| **RNF09** | Integridade | Os registros do processo (versões, interações, colagens) não podem ser alterados após gravados (RN04). |
| **RNF10** | Usabilidade | Interface e respostas do assistente em linguagem simples e adequada à faixa etária dos estudantes. O estudante deve identificar a etapa atual e como pedir ajuda sem treinamento prévio. |
| **RNF11** | Transparência da IA | As respostas do assistente devem ser claramente identificadas como geradas por IA. |
| **RNF12** | Acessibilidade | A interface deve seguir as diretrizes WCAG 2.1, nível AA. |
| **RNF13** | Compatibilidade | O sistema deve funcionar nas versões atuais dos navegadores Chrome, Firefox e Edge, em computador. |

---

## 6. Fluxos do Sistema

### 6.1 Fluxo principal

1. O professor cria a turma (RF16) e a atividade, com tema, gênero, orientações, critérios e prazo (RF01).
2. O estudante acessa a plataforma, lê e aceita o termo de ciência (RF21).
3. O estudante abre a atividade e inicia a produção na etapa **Planejar** (RF02, RF17), registrando tese e ideias.
4. O estudante avança para **Escrever** e redige o texto no editor (RF03); o sistema salva versões automaticamente (RF04).
5. Em qualquer etapa, o estudante pode solicitar orientação (RF07); o assistente responde com perguntas e apontamentos (RF08, RF09) e a interação é registrada (RF10, RF12).
6. O estudante avança para **Revisar**, relê o texto e pode pedir apontamentos ao assistente.
7. O estudante avança para **Reescrever** e decide o que alterar. Os passos 6 e 7 podem se repetir.
8. Durante todo o processo, o professor pode acompanhar a produção no painel (RF13).
9. O estudante submete a versão final (RF14).
10. O sistema executa a verificação de similaridade (RF15) e apresenta o resultado ao professor.
11. O professor avalia a produção e, se quiser, registra uma devolutiva sobre o processo (RF19).

### 6.2 Fluxos alternativos

**FA01 – Estudante pede ao assistente que escreva ou reescreva**
No passo 5, o estudante pede, por exemplo, "Pode reescrever minha conclusão?". O assistente recusa explicitamente e devolve perguntas que ajudem o estudante a reescrever por conta própria. A interação é registrada na categoria "pedido de escrita ou reescrita" (RF12).

**FA02 – Resposta do assistente reprovada na verificação automática**
No passo 5, a resposta gerada contém texto aproveitável. O sistema descarta a resposta, exibe uma orientação genérica e registra a ocorrência (RNF05).

**FA03 – Estudante cola um trecho longo**
Nos passos 3 a 7, o estudante cola um trecho acima do limite configurado. A colagem é aceita e registrada (RF18) e é destacada no painel do professor.

**FA04 – Assistente indisponível**
No passo 5, a API do modelo não responde. O sistema informa que o assistente está temporariamente indisponível, e o estudante continua escrevendo normalmente (RNF08).

**FA05 – Prazo expirado**
No passo 9, o prazo terminou. A submissão é bloqueada ou aceita como atrasada, conforme configuração da atividade (RF14).

**FA06 – Estudante não usa o assistente**
O estudante conclui a produção sem nenhuma solicitação. O fluxo é válido; o painel indica zero interações, o que é um dado relevante para o indicador de autonomia.

---

## 7. Salvaguardas

Cada salvaguarda prevista na POC 2.2 e cada cuidado apresentado ao stakeholder é implementado pelos requisitos abaixo.

| Salvaguarda / risco | Como o sistema trata | Requisitos |
|---|---|---|
| Vedação de produção de texto em nome do estudante | O assistente só orienta, recusa pedidos de escrita e tem as respostas verificadas automaticamente; o editor não aceita inserção automática de conteúdo. | RF03, RF09, RN01, RN02, RNF05 |
| Registro do processo de escrita para o professor | Versões por etapa, interações e colagens ficam registradas e são exibidas no painel. | RF04, RF10, RF11, RF13, RF17, RF18 |
| Testagem de efeitos de dependência em uso prolongado | O apoio solicitado é classificado e acompanhado de uma atividade para outra; o piloto prevê várias atividades. | RF12, Seção 9 |
| Plágio assistido | Registro de colagens e verificação de similaridade, sempre interpretados pelo professor. | RF15, RF18, RN06 |
| Textos padronizados | O assistente orienta por perguntas, sem modelo pronto. | RN09 |
| Variação linguística e criatividade | Escolhas de estilo não são tratadas como erro. | RN08 |
| Exposição do aluno | Termo de ciência, acesso aos próprios dados, proibição de rankings e vigilância, pseudonimização. | RF20, RF21, RN05, RN10, RNF01–RNF04 |

---

## 8. Métricas de Avaliação da POC

| Métrica (POC 2.2) | Como medir | Fonte dos dados |
|---|---|---|
| **Qualidade da produção final** | O professor aplica os critérios de avaliação da atividade (RF01) à primeira versão marcada e à versão final; compara-se a diferença. | RF01, RF04, RF06 |
| **Autonomia progressiva** | Proporção de alterações feitas na etapa Reescrever **sem** solicitação ao assistente na etapa Revisar, comparada entre atividades. | RF11, RF12, RF17 |
| **Redução do apoio solicitado** | Número de solicitações por produção e proporção de pedidos de escrita ou reescrita, comparados entre a primeira e a última atividade do piloto. | RF10, RF12 |
| **Originalidade dos textos** | Percentual de similaridade da versão final e volume de texto colado em relação ao tamanho do texto final. | RF15, RF18 |

**Critério de sucesso** *(a definir com o stakeholder)*: a hipótese é considerada sustentada se, ao longo do piloto, a qualidade entre versões melhorar, o apoio solicitado diminuir ou se mantiver estável sem aumento de pedidos de escrita, e não houver aumento de indícios de plágio.

---

## 9. Plano da POC

| Fase | Descrição | Requisitos mínimos |
|---|---|---|
| **1. Demonstração** | Uma atividade, conduzida pela equipe com o stakeholder, para validar o fluxo e o comportamento do assistente. | Prioridade **Alta** |
| **2. Piloto** | Uma turma, durante algumas semanas, com **pelo menos 3 atividades** *(sugerido)*, para permitir observar a evolução entre atividades. | Prioridades **Alta** e **Média** |

---

## 10. Questões em Aberto

1. Qual base externa será usada na verificação de similaridade (RF15)? Há ferramenta institucional disponível?
2. Qual a faixa etária e a etapa de ensino da turma piloto? Isso afeta o consentimento (RNF02) e a linguagem do assistente (RNF10).
3. Qual o prazo de retenção dos dados após o fim da POC (RNF01)?
4. Qual provedor de modelo de linguagem será usado e quais são seus termos sobre uso de dados (RNF04)?
5. Quantas atividades e qual duração terá o piloto, e quais os limiares do critério de sucesso (Seção 8)?
6. O professor poderá ajustar o comportamento do assistente por atividade (por exemplo, desabilitá-lo em uma etapa)?

---

## 11. Rastreabilidade com a POC 2.2

| Item da POC 2.2 | Requisitos |
|---|---|
| Hipótese: acompanhamento por etapas | RF17, RF04, RF13 |
| Hipótese: autoria e autorregulação | RF09, RF12, RN01, RN02 |
| Hipótese: sem dependência | RF12, Seção 8 |
| Hipótese: sem plágio assistido | RF15, RF18 |
| Requisito de dados: versões | RF04, RF05, RF06 |
| Requisito de dados: etapas | RF17, RF11 |
| Classificação de risco moderado | RF21, RF22, RNF01–RNF05 |

---

## 12. Histórico de Revisões

| Versão | Alterações |
|---|---|
| 1.0 | Versão inicial: RF01–RF15, RN01–RN06. |
| 2.0 | Inclusão das etapas do processo (RF17) e do registro de colagens (RF18). Inclusão de turma, devolutiva, acesso aos próprios dados, termo de ciência e autenticação (RF16, RF19–RF22). RF09 reescrito de forma verificável. RF01, RF04, RF06, RF08, RF12, RF13, RF14 e RF15 detalhados. Inclusão de critérios de aceitação e prioridades. Novas regras RN07–RN10. Inclusão de requisitos não funcionais, fluxos alternativos, matriz de salvaguardas, métricas operacionalizadas, plano da POC, questões em aberto e rastreabilidade. |