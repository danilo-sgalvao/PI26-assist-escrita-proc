<!-- Modelo do Apêndice C do plano mestre v1.2. Processo: docs/manutencao/processo-de-manutencao.md -->

## Tarefa e requisitos

Fecha #<issue> · Txx · DEF/MUD-nnn (se houver) · Categoria ISO 14764: <corretiva | preventiva | adaptativa | aditiva | perfectiva | emergencial | não se aplica> · RF/RN/RNF: <...> · CA: <...>

## Design do incremento (plano, seção 4.2.3)

<!-- Obrigatório em tarefa de implementação. Em PR só de documentação, escreva "Não se aplica". -->

- Componentes (Lambdas, componentes React, módulos):
- Endpoints (rota, entrada, saída, erros):
- Dados (tabelas, migração, chaves no S3/DynamoDB):
- Sequência (se envolver mais de 2 componentes):
- Testes previstos por CA:
- Alternativas descartadas:

## O que mudou

## Como testar

## Evidências (prints, logs, resultado de testes)

## Impacto

- [ ] Contrato da API
- [ ] Esquema do banco / dados gravados
- [ ] Prompt / guardrail (RN01/RN02)
- [ ] Infraestrutura (`infra/template.yaml`, permissões IAM)
- [ ] Documentação

## Segurança

- [ ] Nenhum segredo, chave, token ou senha no diff, em prints ou em logs
- [ ] Nenhum dado real de aluno; nada que identifique o aluno vai ao Bedrock
- [ ] Permissões IAM, CORS e autorizadores continuam no mínimo necessário

## Checklist da DoD

- [ ] Testes adequados (para defeito: teste que reproduz o problema)
- [ ] CI verde
- [ ] Docs atualizadas
- [ ] Revisor do anel A→B→C→D→A indicado (o autor não aprova o próprio PR)
- [ ] Uso de IA declarado, se houve
