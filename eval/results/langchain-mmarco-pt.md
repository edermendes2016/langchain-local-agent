# Avaliação de recuperação: langchain

18 perguntas de referência, coleção `tutorial_collection` (2347 blocos), reranker `cross-encoder` (`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`), 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.83 | 0.72 |
| recall@1 | 0.83 | 0.72 |
| hit@3 | 0.89 | 0.89 |
| recall@3 | 0.89 | 0.89 |
| hit@5 | 0.89 | 0.89 |
| recall@5 | 0.89 | 0.89 |
| MRR | 0.86 | 0.81 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| lc01 | Onde fica definida a classe base abstrata dos modelos de chat? | 1 | 1 |
| lc02 | Que classe implementa o encadeamento de runnables com o operador pipe, executando um depois do outro? | 1 | 1 |
| lc03 | Onde está a classe que executa vários runnables em paralelo sobre a mesma entrada? | 1 | 1 |
| lc04 | Qual classe representa a mensagem de resposta da IA, com chamadas de ferramenta e metadados de uso? | 1 | 1 |
| lc05 | Onde é definido o template de prompt para conversas com lista de mensagens de sistema e de usuário? | 1 | 2 |
| lc06 | Que parser converte a saída do modelo em texto simples? | 1 | 1 |
| lc07 | Onde está o decorador que transforma uma função Python em uma ferramenta para agentes? | >10 | >10 |
| lc08 | Qual é a interface abstrata dos recuperadores de documentos e qual método eles implementam? | 1 | 2 |
| lc09 | Onde fica a classe Document que guarda o conteúdo da página e os metadados? | 1 | 1 |
| lc10 | Onde está o gerenciador de callbacks que dispara eventos de início e fim de execução? | 1 | 1 |
| lc11 | Existe um vector store em memória? Onde ele é implementado? | 1 | 1 |
| lc12 | Qual interface define como textos são convertidos em embeddings? | 1 | 1 |
| lc13 | Como é implementado o cache em memória das respostas dos modelos? | 1 | 1 |
| lc14 | Onde está o limitador de taxa de requisições em memória para chamadas de modelo? | 1 | 1 |
| lc15 | Qual função garante uma configuração RunnableConfig válida, preenchendo valores padrão? | >10 | 3 |
| lc16 | Onde está o template de prompt com exemplos few-shot? | 1 | 1 |
| lc17 | Qual classe interpreta a saída do modelo como JSON? | 2 | 6 |
| lc18 | Onde está a função que corta uma lista de mensagens para caber em um limite de tokens? | 1 | 1 |
