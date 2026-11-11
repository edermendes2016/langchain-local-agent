# Avaliação de recuperação: langchain

18 perguntas de referência, coleção `tutorial_collection` (2347 blocos), reranker `cross-encoder/ms-marco-MiniLM-L-6-v2`, 40 candidatos antes do reranking.

| Métrica | Busca vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0.39 | 0.61 |
| recall@1 | 0.39 | 0.61 |
| hit@3 | 0.56 | 0.83 |
| recall@3 | 0.56 | 0.83 |
| hit@5 | 0.72 | 0.89 |
| recall@5 | 0.72 | 0.89 |
| MRR | 0.50 | 0.71 |

## Posição do primeiro bloco correto

| Id | Pergunta | Vetorial | Rerank |
|---|---|---|---|
| lc01 | Onde fica definida a classe base abstrata dos modelos de chat? | 1 | 1 |
| lc02 | Que classe implementa o encadeamento de runnables com o operador pipe, executando um depois do outro? | 1 | 1 |
| lc03 | Onde está a classe que executa vários runnables em paralelo sobre a mesma entrada? | 1 | 1 |
| lc04 | Qual classe representa a mensagem de resposta da IA, com chamadas de ferramenta e metadados de uso? | >10 | >10 |
| lc05 | Onde é definido o template de prompt para conversas com lista de mensagens de sistema e de usuário? | 1 | 1 |
| lc06 | Que parser converte a saída do modelo em texto simples? | 4 | 1 |
| lc07 | Onde está o decorador que transforma uma função Python em uma ferramenta para agentes? | >10 | 2 |
| lc08 | Qual é a interface abstrata dos recuperadores de documentos e qual método eles implementam? | 5 | 1 |
| lc09 | Onde fica a classe Document que guarda o conteúdo da página e os metadados? | >10 | 5 |
| lc10 | Onde está o gerenciador de callbacks que dispara eventos de início e fim de execução? | 1 | 1 |
| lc11 | Existe um vector store em memória? Onde ele é implementado? | 3 | 2 |
| lc12 | Qual interface define como textos são convertidos em embeddings? | 7 | 1 |
| lc13 | Como é implementado o cache em memória das respostas dos modelos? | 2 | 1 |
| lc14 | Onde está o limitador de taxa de requisições em memória para chamadas de modelo? | >10 | >10 |
| lc15 | Qual função garante uma configuração RunnableConfig válida, preenchendo valores padrão? | 5 | 3 |
| lc16 | Onde está o template de prompt com exemplos few-shot? | 1 | 1 |
| lc17 | Qual classe interpreta a saída do modelo como JSON? | 3 | 3 |
| lc18 | Onde está a função que corta uma lista de mensagens para caber em um limite de tokens? | 1 | 1 |

## Respostas do LLM local

Modelo `prism-ml/bonsai-27b`, k = 6, com reranking.

- Citam o arquivo esperado: **14/18**
- Citam o arquivo esperado e mencionam todas as palavras-chave: **11/18**
- Tempo médio por resposta: **49 s**

| Id | Cita o arquivo | Palavras-chave | Tempo |
|---|---|---|---|
| lc01 | sim | 1/1 | 24 s |
| lc02 | não | 1/1 | 58 s |
| lc03 | sim | 1/1 | 21 s |
| lc04 | não | 1/1 | 29 s |
| lc05 | sim | 0/1 | 38 s |
| lc06 | sim | 1/1 | 18 s |
| lc07 | sim | 1/1 | 40 s |
| lc08 | sim | 1/1 | 44 s |
| lc09 | sim | 1/1 | 34 s |
| lc10 | sim | 0/1 | 66 s |
| lc11 | sim | 1/1 | 64 s |
| lc12 | sim | 1/1 | 83 s |
| lc13 | sim | 0/1 | 60 s |
| lc14 | não | 0/1 | 39 s |
| lc15 | não | 1/1 | 90 s |
| lc16 | sim | 1/1 | 65 s |
| lc17 | sim | 1/1 | 39 s |
| lc18 | sim | 1/1 | 77 s |

A conferência de respostas é automática e simples (texto contém o caminho ou o nome do arquivo esperado e as palavras-chave). Ela mede ancoragem, não qualidade da redação.
