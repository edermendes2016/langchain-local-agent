# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `bm25` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.08 | 0.17 |
| recall@1 | 0.08 | 0.17 |
| hit@3 | 0.25 | 0.25 |
| recall@3 | 0.25 | 0.21 |
| hit@5 | 0.33 | 0.33 |
| recall@5 | 0.29 | 0.29 |
| MRR | 0.21 | 0.26 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Onde são validados o nome do jogador e a pontuação enviados ao ranking? | >10 | >10 |
| aq02 | Como o backend Lambda valida a resposta do usuário no quiz? | 6 | >10 |
| aq03 | Qual a pontuação máxima por pergunta que o backend aceita? | >10 | >10 |
| aq04 | Qual tabela do DynamoDB guarda as pontuações e qual o modo de cobrança? | >10 | 9 |
| aq05 | Como é configurado o acesso HTTP público à função Lambda e o CORS? | >10 | >10 |
| aq06 | Quais recursos da AWS a stack do CloudFormation cria? | 8 | 9 |
| aq07 | Como o script de deploy injeta a URL da API no front-end? | 10 | 7 |
| aq08 | Como remover todos os recursos criados na AWS? | 3 | 1 |
| aq09 | Quantos segundos o jogador tem por pergunta e como é calculado o bônus de velocidade? | 2 | 4 |
| aq10 | Como o front-end guarda o ranking quando a API não está configurada? | 4 | 3 |
| aq11 | Onde estão os testes automatizados do backend? | >10 | 8 |
| aq12 | Onde ficam as perguntas do quiz com alternativas e explicações? | 1 | 1 |
