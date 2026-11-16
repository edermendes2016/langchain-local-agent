# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `cross-encoder` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.50 | 0.83 |
| recall@1 | 0.50 | 0.79 |
| hit@3 | 0.83 | 0.92 |
| recall@3 | 0.79 | 0.92 |
| hit@5 | 0.92 | 1.00 |
| recall@5 | 0.88 | 1.00 |
| MRR | 0.67 | 0.89 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Where are the player name and the score sent to the ranking validated? | 2 | 1 |
| aq02 | How does the Lambda backend validate the user's answer in the quiz? | 1 | 1 |
| aq03 | What is the maximum score per question that the backend accepts? | 4 | 1 |
| aq04 | Which DynamoDB table stores the scores and what is the billing mode? | 1 | 1 |
| aq05 | How is public HTTP access to the Lambda function and CORS configured? | 1 | 1 |
| aq06 | Which AWS resources does the CloudFormation stack create? | 2 | 5 |
| aq07 | How does the deploy script inject the API URL into the front end? | >10 | 2 |
| aq08 | How do I remove all the resources created on AWS? | 1 | 1 |
| aq09 | How many seconds does the player have per question and how is the speed bonus calculated? | 1 | 1 |
| aq10 | How does the front end store the ranking when the API is not configured? | 2 | 1 |
| aq11 | Where are the automated tests of the backend? | 3 | 1 |
| aq12 | Where are the quiz questions with options and explanations? | 1 | 1 |
