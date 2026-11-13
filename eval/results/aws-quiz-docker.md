# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `cross-encoder` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.42 | 0.33 |
| recall@1 | 0.38 | 0.29 |
| hit@3 | 0.50 | 0.50 |
| recall@3 | 0.46 | 0.46 |
| hit@5 | 0.67 | 0.75 |
| recall@5 | 0.62 | 0.75 |
| MRR | 0.49 | 0.48 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Onde são validados o nome do jogador e a pontuação enviados ao ranking? | 5 | >10 |
| aq02 | Como o backend Lambda valida a resposta do usuário no quiz? | 1 | 4 |
| aq03 | Qual a pontuação máxima por pergunta que o backend aceita? | >10 | >10 |
| aq04 | Qual tabela do DynamoDB guarda as pontuações e qual o modo de cobrança? | >10 | 4 |
| aq05 | Como é configurado o acesso HTTP público à função Lambda e o CORS? | 5 | 4 |
| aq06 | Quais recursos da AWS a stack do CloudFormation cria? | >10 | 8 |
| aq07 | Como o script de deploy injeta a URL da API no front-end? | 2 | 3 |
| aq08 | Como remover todos os recursos criados na AWS? | 1 | 1 |
| aq09 | Quantos segundos o jogador tem por pergunta e como é calculado o bônus de velocidade? | 1 | 2 |
| aq10 | Como o front-end guarda o ranking quando a API não está configurada? | 1 | 1 |
| aq11 | Onde estão os testes automatizados do backend? | >10 | 1 |
| aq12 | Onde ficam as perguntas do quiz com alternativas e explicações? | 1 | 1 |

## Respostas do LLM local

Modelo `qwen2.5-coder:3b`, k = 6, com reranking.

- Citam o arquivo esperado: **7/12**
- Citam o arquivo esperado e mencionam todas as palavras-chave: **3/12**
- Tempo médio por resposta: **43 s**

| Id | Cita o arquivo | Palavras-chave | Tempo |
|---|---|---|---|
| aq01 | não | 0/1 | 33 s |
| aq02 | sim | 1/1 | 30 s |
| aq03 | não | 0/1 | 46 s |
| aq04 | não | 0/1 | 25 s |
| aq05 | não | 1/1 | 28 s |
| aq06 | sim | 1/1 | 52 s |
| aq07 | sim | 1/1 | 29 s |
| aq08 | sim | 0/1 | 23 s |
| aq09 | não | 1/1 | 31 s |
| aq10 | sim | 0/1 | 173 s |
| aq11 | sim | 0/1 | 17 s |
| aq12 | sim | 0/1 | 24 s |

A conferência de respostas é automática e simples (texto contém o caminho ou o nome do arquivo esperado e as palavras-chave). Ela mede ancoragem, não qualidade da redação.
