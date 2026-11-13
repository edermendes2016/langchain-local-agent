# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `bm25` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.42 | 0.33 |
| recall@1 | 0.38 | 0.29 |
| hit@3 | 0.50 | 0.42 |
| recall@3 | 0.46 | 0.38 |
| hit@5 | 0.67 | 0.50 |
| recall@5 | 0.62 | 0.46 |
| MRR | 0.49 | 0.44 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Onde são validados o nome do jogador e a pontuação enviados ao ranking? | 5 | >10 |
| aq02 | Como o backend Lambda valida a resposta do usuário no quiz? | 1 | 6 |
| aq03 | Qual a pontuação máxima por pergunta que o backend aceita? | >10 | >10 |
| aq04 | Qual tabela do DynamoDB guarda as pontuações e qual o modo de cobrança? | >10 | 10 |
| aq05 | Como é configurado o acesso HTTP público à função Lambda e o CORS? | 5 | 4 |
| aq06 | Quais recursos da AWS a stack do CloudFormation cria? | >10 | 10 |
| aq07 | Como o script de deploy injeta a URL da API no front-end? | 2 | 2 |
| aq08 | Como remover todos os recursos criados na AWS? | 1 | 1 |
| aq09 | Quantos segundos o jogador tem por pergunta e como é calculado o bônus de velocidade? | 1 | 1 |
| aq10 | Como o front-end guarda o ranking quando a API não está configurada? | 1 | 1 |
| aq11 | Onde estão os testes automatizados do backend? | >10 | 7 |
| aq12 | Onde ficam as perguntas do quiz com alternativas e explicações? | 1 | 1 |
