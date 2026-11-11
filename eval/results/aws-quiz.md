# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `cross-encoder/ms-marco-MiniLM-L-6-v2`, 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.08 | 0.33 |
| recall@1 | 0.08 | 0.29 |
| hit@3 | 0.25 | 0.50 |
| recall@3 | 0.25 | 0.46 |
| hit@5 | 0.33 | 0.75 |
| recall@5 | 0.29 | 0.75 |
| MRR | 0.21 | 0.48 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Onde são validados o nome do jogador e a pontuação enviados ao ranking? | >10 | >10 |
| aq02 | Como o backend Lambda valida a resposta do usuário no quiz? | 6 | 4 |
| aq03 | Qual a pontuação máxima por pergunta que o backend aceita? | >10 | >10 |
| aq04 | Qual tabela do DynamoDB guarda as pontuações e qual o modo de cobrança? | >10 | 4 |
| aq05 | Como é configurado o acesso HTTP público à função Lambda e o CORS? | >10 | 4 |
| aq06 | Quais recursos da AWS a stack do CloudFormation cria? | 8 | 8 |
| aq07 | Como o script de deploy injeta a URL da API no front-end? | 10 | 3 |
| aq08 | Como remover todos os recursos criados na AWS? | 3 | 1 |
| aq09 | Quantos segundos o jogador tem por pergunta e como é calculado o bônus de velocidade? | 2 | 2 |
| aq10 | Como o front-end guarda o ranking quando a API não está configurada? | 4 | 1 |
| aq11 | Onde estão os testes automatizados do backend? | >10 | 1 |
| aq12 | Onde ficam as perguntas do quiz com alternativas e explicações? | 1 | 1 |

## Respostas do LLM local

Modelo `prism-ml/bonsai-27b`, k = 6, com reranking.

- Citam o arquivo esperado: **8/12**
- Citam o arquivo esperado e mencionam todas as palavras-chave: **5/12**
- Tempo médio por resposta: **66 s**

| Id | Cita o arquivo | Palavras-chave | Tempo |
|---|---|---|---|
| aq01 | não | 0/1 | 76 s |
| aq02 | sim | 1/1 | 78 s |
| aq03 | não | 1/1 | 92 s |
| aq04 | sim | 0/1 | 52 s |
| aq05 | não | 1/1 | 50 s |
| aq06 | não | 1/1 | 42 s |
| aq07 | sim | 1/1 | 127 s |
| aq08 | sim | 0/1 | 86 s |
| aq09 | sim | 1/1 | 45 s |
| aq10 | sim | 1/1 | 38 s |
| aq11 | sim | 1/1 | 44 s |
| aq12 | sim | 0/1 | 60 s |

A conferência de respostas é automática e simples (texto contém o caminho ou o nome do arquivo esperado e as palavras-chave). Ela mede ancoragem, não qualidade da redação.
