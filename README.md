# Assistente de Escrita Processual

Prova de conceito do Grupo 8 para a disciplina de Manutenção de Software. A documentação está em `docs/`; o contexto e a hierarquia documental estão em [CLAUDE.md](CLAUDE.md).

A [base de conhecimento RAG](conhecimento/README.md) reúne os documentos cadastrados, com extração, metadados, referências às fontes e busca BM25 offline. Comece pelo [mapa do projeto](conhecimento/mapa-do-projeto.md) para entender requisitos, decisões, arquitetura proposta e pendências.

```powershell
python -m pip install -r requirements-rag.txt
python ferramentas/rag.py construir
python ferramentas/rag.py buscar "RF09 restrições de autoria"
python ferramentas/rag.py contexto "Quais fontes entram na similaridade RF15?"
```

A ferramenta prepara evidências para consultas de engenharia e para uso com um modelo de IA. A fundação do backend e as instruções de execução estão em [backend/README.md](backend/README.md); as demais funcionalidades pedagógicas dependem das etapas seguintes.
