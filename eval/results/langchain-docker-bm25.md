# Avaliação de recuperação: langchain

18 perguntas de referência, coleção `langchain-core` (2347 blocos), reranker `bm25` (`cross-encoder/ms-marco-MiniLM-L-6-v2`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.44 | 0.50 |
| recall@1 | 0.44 | 0.50 |
| hit@3 | 0.61 | 0.67 |
| recall@3 | 0.61 | 0.67 |
| hit@5 | 0.67 | 0.67 |
| recall@5 | 0.67 | 0.67 |
| MRR | 0.56 | 0.60 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| lc01 | Onde fica definida a classe base abstrata dos modelos de chat? | 1 | 1 |
| lc02 | Que classe implementa o encadeamento de runnables com o operador pipe, executando um depois do outro? | 1 | 1 |
| lc03 | Onde está a classe que executa vários runnables em paralelo sobre a mesma entrada? | 5 | 7 |
| lc04 | Qual classe representa a mensagem de resposta da IA, com chamadas de ferramenta e metadados de uso? | >10 | >10 |
| lc05 | Onde é definido o template de prompt para conversas com lista de mensagens de sistema e de usuário? | 1 | 1 |
| lc06 | Que parser converte a saída do modelo em texto simples? | 1 | 2 |
| lc07 | Onde está o decorador que transforma uma função Python em uma ferramenta para agentes? | >10 | >10 |
| lc08 | Qual é a interface abstrata dos recuperadores de documentos e qual método eles implementam? | >10 | >10 |
| lc09 | Onde fica a classe Document que guarda o conteúdo da página e os metadados? | 6 | 1 |
| lc10 | Onde está o gerenciador de callbacks que dispara eventos de início e fim de execução? | 1 | 1 |
| lc11 | Existe um vector store em memória? Onde ele é implementado? | 2 | 1 |
| lc12 | Qual interface define como textos são convertidos em embeddings? | 1 | 1 |
| lc13 | Como é implementado o cache em memória das respostas dos modelos? | 7 | 10 |
| lc14 | Onde está o limitador de taxa de requisições em memória para chamadas de modelo? | 2 | 2 |
| lc15 | Qual função garante uma configuração RunnableConfig válida, preenchendo valores padrão? | 2 | 2 |
| lc16 | Onde está o template de prompt com exemplos few-shot? | 1 | 1 |
| lc17 | Qual classe interpreta a saída do modelo como JSON? | >10 | >10 |
| lc18 | Onde está a função que corta uma lista de mensagens para caber em um limite de tokens? | 1 | 1 |
