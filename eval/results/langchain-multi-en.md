# Avaliação de recuperação: langchain

18 perguntas de referência, coleção `tutorial_collection` (2347 blocos), reranker `cross-encoder` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.72 | 0.89 |
| recall@1 | 0.72 | 0.89 |
| hit@3 | 0.89 | 0.94 |
| recall@3 | 0.89 | 0.94 |
| hit@5 | 0.89 | 0.94 |
| recall@5 | 0.89 | 0.94 |
| MRR | 0.81 | 0.92 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| lc01 | Where is the abstract base class for chat models defined? | 1 | 1 |
| lc02 | Which class implements chaining runnables with the pipe operator, running one after another? | 1 | 1 |
| lc03 | Where is the class that runs several runnables in parallel on the same input? | 1 | 1 |
| lc04 | Which class represents the AI response message, with tool calls and usage metadata? | 1 | 1 |
| lc05 | Where is the prompt template for conversations with a list of system and user messages defined? | 1 | 1 |
| lc06 | Which parser converts the model output into plain text? | 2 | 1 |
| lc07 | Where is the decorator that turns a Python function into a tool for agents? | >10 | 2 |
| lc08 | What is the abstract interface for document retrievers and which method do they implement? | 2 | 1 |
| lc09 | Where is the Document class that holds the page content and the metadata? | 1 | 1 |
| lc10 | Where is the callback manager that fires the start and end events of a run? | 1 | 1 |
| lc11 | Is there an in-memory vector store? Where is it implemented? | 1 | 1 |
| lc12 | Which interface defines how texts are converted into embeddings? | 1 | 1 |
| lc13 | How is the in-memory cache of model responses implemented? | 1 | 1 |
| lc14 | Where is the in-memory rate limiter for model calls? | 1 | 1 |
| lc15 | Which function ensures a valid RunnableConfig, filling in default values? | >10 | >10 |
| lc16 | Where is the prompt template with few-shot examples? | 2 | 1 |
| lc17 | Which class parses the model output as JSON? | 1 | 1 |
| lc18 | Where is the function that trims a list of messages to fit a token limit? | 1 | 1 |
