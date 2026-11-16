# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `cross-encoder` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.58 | 0.33 |
| recall@1 | 0.58 | 0.29 |
| hit@3 | 0.83 | 0.50 |
| recall@3 | 0.79 | 0.46 |
| hit@5 | 0.83 | 0.75 |
| recall@5 | 0.79 | 0.75 |
| MRR | 0.69 | 0.48 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Onde são validados o nome do jogador e a pontuação enviados ao ranking? | 2 | >10 |
| aq02 | Como o backend Lambda valida a resposta do usuário no quiz? | 1 | 4 |
| aq03 | Qual a pontuação máxima por pergunta que o backend aceita? | >10 | >10 |
| aq04 | Qual tabela do DynamoDB guarda as pontuações e qual o modo de cobrança? | 1 | 4 |
| aq05 | Como é configurado o acesso HTTP público à função Lambda e o CORS? | 1 | 4 |
| aq06 | Quais recursos da AWS a stack do CloudFormation cria? | 2 | 8 |
| aq07 | Como o script de deploy injeta a URL da API no front-end? | >10 | 3 |
| aq08 | Como remover todos os recursos criados na AWS? | 1 | 1 |
| aq09 | Quantos segundos o jogador tem por pergunta e como é calculado o bônus de velocidade? | 1 | 2 |
| aq10 | Como o front-end guarda o ranking quando a API não está configurada? | 3 | 1 |
| aq11 | Onde estão os testes automatizados do backend? | 1 | 1 |
| aq12 | Onde ficam as perguntas do quiz com alternativas e explicações? | 1 | 1 |
