# Base de conhecimento RAG do projeto

| Campo | Valor |
|---|---|
| Versão | 1.0 |
| Data | 30/10/2026 |
| Autor | Elaborado com apoio de IA (Codex), a pedido do usuário |
| Revisor | Pendente de revisão pela equipe |
| Estado | Base documental local construída e verificada; síntese derivada, sem aprovação de requisitos novos |

Esta base permite localizar evidências na documentação do Assistente de Escrita Processual e preparar um contexto com citações para um modelo de linguagem. O corpus cobre os **12 arquivos locais** cadastrados: contexto do projeto, enunciado da POC, apresentação, versões da ERS e dos planos, representações em Word/PDF e ADR do Bedrock. O [mapa do projeto](mapa-do-projeto.md) oferece a leitura inicial por assunto.

## Execução

Requisitos: Python 3.10 ou superior, SQLite com FTS5 e a dependência de extração em `requirements-rag.txt`. Validado nesta máquina com Python 3.14.7 e pypdf 6.19.0. Execute da raiz do repositório:

```powershell
python -m pip install -r requirements-rag.txt
python ferramentas/rag.py construir
python ferramentas/rag.py verificar
```

O índice SQLite já foi construído neste ambiente e pode ser usado imediatamente. Ele é ignorado pelo Git; reconstrua depois de clonar o repositório ou mudar de máquina.

### Buscar trechos

```powershell
python ferramentas/rag.py buscar "RF09 restringir geração de conteúdo"
python ferramentas/rag.py buscar "B5 B10 pendentes" --limite 3
python ferramentas/rag.py buscar "RNF04 privacidade treinamento" --fonte ers-v2 --json
python ferramentas/rag.py buscar "Ollama modelo local" --historico
python ferramentas/rag.py buscar "Ollama" --historico --fonte plano-v1-1
```

O resultado inclui ID do trecho, caminho, seção, versão, estado e localização. Em Markdown, o localizador usa linhas do arquivo original; em PDF, página física iniciando em 1; em DOCX, posição do elemento no corpo de `word/document.xml`, sem inferir página. `--fonte` recebe o ID do [cadastro](fontes.json). Uma fonte histórica exige também `--historico`. O limite aceito é de 1 a 50 trechos.

### Preparar contexto para IA

```powershell
python ferramentas/rag.py contexto "Quais fontes entram na similaridade RF15?"
```

O comando produz as [orientações de resposta](politica-rag.md), a pergunta e as evidências em JSON com citações. Além dos resultados da busca, inclui obrigatoriamente os trechos dos fatos confirmados, da hierarquia documental, das decisões B1–B12 e do tratamento de B5/B10. Isso permite que o consumidor veja a divergência do RF15 mesmo quando o requisito isolado aparece primeiro no ranking. A política instrui a citar as fontes, indicar pendências e declarar ausência de evidência; o comportamento efetivo de um modelo precisa de avaliação própria.

Use essa saída como contexto em uma consulta a um modelo de sua escolha. **Não há chamada de LLM nem geração automática de resposta nesta ferramenta.** A etapa implementada é a base documental com recuperação e preparação de contexto do RAG. Ela não depende de chave de API e não envia arquivos a serviços externos.

## Organização

| Arquivo ou diretório | Finalidade |
|---|---|
| `fontes.json` | Cadastro explícito das fontes, versões, estados, papéis e precedência documental |
| `mapa-do-projeto.md` | Síntese navegável dos conhecimentos e das decisões, com links aos originais |
| `politica-rag.md` | Orientações para o consumidor interpretar evidências, divergências e limites |
| `transcricoes/` | Transcrição da imagem da POC e descrições dos dez diagramas históricos, vinculadas por SHA-256 às fontes |
| `avaliacao.json` | 15 consultas de referência com fontes e evidências esperadas entre os cinco primeiros resultados |
| `gerado/inventario.json` | Hash, quantidade de unidades e caracteres extraídos por arquivo |
| `gerado/textos/*.json` | Texto extraído de cada fonte com unidades e localizadores, incluindo as representações |
| `gerado/trechos.jsonl` | Corpus segmentado, portável para outros mecanismos de recuperação |
| `gerado/indice.sqlite3` | Índice FTS5/BM25 local, reconstruível e ignorado pelo Git |
| `../ferramentas/rag.py` | Extração, segmentação, construção, busca, contexto, verificação e avaliação |
| `../ferramentas/test_rag.py` | Testes de extração, recuperação, contexto e atualização |

O corpus atual tem **2.156 trechos**, dos quais **297 são consultáveis por padrão**. O total também inclui fontes históricas, representações e títulos sem corpo. As representações são preservadas na exportação e excluídas da busca; as fontes históricas entram mediante opção explícita; títulos sem corpo não ocupam resultados. O inventário é a fonte da contagem de arquivos, unidades e caracteres.

## Recuperação e rastreabilidade

A busca usa **SQLite FTS5 com BM25**, sem vetores ou embeddings. Remove diferenças de acentuação e palavras funcionais comuns nas consultas, permite busca por IDs como RF09, RNF04 e ADR-006 e favorece correspondências em seções e identificadores de linhas de tabela. Quando um identificador é informado, o trecho precisa conter esse identificador. As palavras restantes ampliam a recuperação por OR. Janelas quase iguais da mesma seção são reduzidas nos resultados.

A segmentação tem teto de 1.800 caracteres e sobreposição alvo de 220 caracteres dentro de cada unidade, preferindo limites de linha ou palavra. Unidades são seções no Markdown, páginas no PDF e parágrafos/tabelas no Word. Um bloco DOCX pequeno não é agrupado artificialmente a outros blocos; por isso as representações e a fonte histórica em Word geram muitos trechos curtos. Tabelas permanecem em texto com linhas e células na ordem de origem; o consumidor pode precisar consultar a unidade completa para recuperar o cabeçalho de uma tabela longa.

Cada linha do JSONL contém `id`, `fonte_id`, `caminho`, `titulo`, `versao`, `estado`, `papel`, `precedencia`, `secao`, `localizacao`, `texto` e `sha256_fonte`. Representações têm `representacao_de`; trechos enriquecidos visualmente têm `transcricao_visual`. IDs têm o formato `fonte:ordinal` e são reproduzíveis para a mesma entrada; podem mudar após edições. Para auditoria, guarde também o hash e a versão da fonte.

A pontuação representa relevância textual, não autoridade. A precedência numérica é um desempate; a interpretação das fontes é regida pela hierarquia e pelas exceções documentadas. Uma consulta histórica também pode recuperar trechos vigentes que discutem uma opção antiga. Use `--fonte` para restringir a uma versão específica.

## Atualização

1. Acrescente ou altere os documentos de origem pelo processo de revisão da equipe.
2. Se houver arquivo novo em `docs/` com extensão `.md`, `.pdf` ou `.docx`, cadastre-o em `fontes.json` com estado e versão. A construção acusa documentos sem cadastro.
3. Se a POC ou o Word histórico mudarem, confira novamente suas imagens e atualize os arquivos em `transcricoes/`, incluindo o hash. A construção rejeita transcrições associadas a bytes diferentes.
4. Rode `construir`, `verificar`, os testes e `avaliar`.
5. Revise o mapa e a política se a hierarquia, as decisões ou as pendências mudarem.

Os comandos de consulta verificam os hashes dos documentos e das transcrições, o cadastro e a correspondência entre corpus e índice. Se uma fonte mudar, a consulta para com orientação para reconstruir. Os JSONs são gravados com UTF-8 e LF para permitir comparação determinística entre execuções.

## Verificação

```powershell
python -m unittest ferramentas.test_rag -v
python ferramentas/rag.py avaliar
```

Na entrega: **10 testes automatizados aprovados e 15/15 consultas de referência aprovadas**. A avaliação verifica a presença de uma evidência esperada entre os cinco primeiros resultados, mais uma consulta sem correspondência. É uma verificação inicial sobre o próprio corpus, não uma medida de precisão geral, de entendimento semântico ou de qualidade de respostas geradas. Os testes também cobrem filtragem histórica, exclusão de representações, origem, seções irmãs, caracteres acentuados, consultas por ID e detecção de fonte alterada.

## Cobertura e limites

- PDFs são extraídos pela camada de texto. O enunciado da POC contém o conteúdo principal em imagem; ele recebeu transcrição visual conferida da página 1, preservando o texto selecionável original.
- Os dez diagramas do plano v1.1 receberam descrições semânticas conferidas nas imagens originais e localizadas nos blocos do Word. Para o plano v1.2, os diagramas estão disponíveis como Mermaid no Markdown canônico. A extração automática não faz OCR nem interpreta imagens novas; esses casos exigem revisão e complemento explícito.
- A leitura do Word cobre o corpo e as tabelas, preservando a ordem. Não reconstrói a paginação, comentários, cabeçalhos, rodapés ou uma representação visual completa do documento.
- Markdown é a fonte canônica da ERS v2 e do plano v1.2. O Word v1.1 é a fonte histórica editável; seu PDF é representação. Exclusão de representações é uma decisão editorial do cadastro, não uma afirmação de identidade entre todos os textos e formatos.
- Links bibliográficos, inclusive o documento complementar do MEC, não foram baixados nem incorporados. A base distingue o que os documentos locais dizem dessas fontes do conteúdo externo efetivamente consultado.
- Busca lexical pode perder paráfrases e sinônimos. Consultas vagas podem retornar coincidências fracas. Prefira códigos e termos do domínio e confira as citações. O JSONL permite adicionar futuramente recuperação vetorial, com avaliação própria.
- Esta base consulta o conhecimento de engenharia do projeto. Não contém produções reais de estudantes e não implementa o assistente pedagógico nem seu guardrail.

## Uso de IA

Solicitação original: “leia toda documentação e crie uma base de conhecimento RAG”. Ferramenta: Codex, em 30/10/2026. Uso: inventário, extração, inspeção das imagens, descrições visuais, síntese com fontes, implementação da recuperação e testes. Revisão humana: pendente pela equipe. Os documentos originais foram preservados.
