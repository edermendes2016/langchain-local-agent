# Avaliação de recuperação: aws-quiz

12 perguntas de referência, coleção `aws-quiz` (40 blocos), reranker `cross-encoder` (`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.50 | 0.50 |
| recall@1 | 0.50 | 0.46 |
| hit@3 | 0.83 | 0.75 |
| recall@3 | 0.79 | 0.75 |
| hit@5 | 0.92 | 0.92 |
| recall@5 | 0.88 | 0.92 |
| MRR | 0.67 | 0.65 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| aq01 | Where are the player name and the score sent to the ranking validated? | 2 | 4 |
| aq02 | How does the Lambda backend validate the user's answer in the quiz? | 1 | 2 |
| aq03 | What is the maximum score per question that the backend accepts? | 4 | 2 |
| aq04 | Which DynamoDB table stores the scores and what is the billing mode? | 1 | 1 |
| aq05 | How is public HTTP access to the Lambda function and CORS configured? | 1 | 1 |
| aq06 | Which AWS resources does the CloudFormation stack create? | 2 | 3 |
| aq07 | How does the deploy script inject the API URL into the front end? | >10 | 5 |
| aq08 | How do I remove all the resources created on AWS? | 1 | 1 |
| aq09 | How many seconds does the player have per question and how is the speed bonus calculated? | 1 | 1 |
| aq10 | How does the front end store the ranking when the API is not configured? | 2 | 1 |
| aq11 | Where are the automated tests of the backend? | 3 | >10 |
| aq12 | Where are the quiz questions with options and explanations? | 1 | 1 |
