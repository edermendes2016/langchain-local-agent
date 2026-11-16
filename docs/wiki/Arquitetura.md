# Arquitetura

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/wiki/edermendes2016/langchain-local-agent/images/arquitetura-rag-dark.svg">
  <img alt="Arquitetura do agente RAG local: indexação no ChromaDB e consulta com reranking e LLM local" src="https://raw.githubusercontent.com/wiki/edermendes2016/langchain-local-agent/images/arquitetura-rag-light.svg" width="100%">
</picture>

O agente tem duas fases: **indexar** o código uma vez e **consultar** a cada pergunta. As cores do desenho mostram qual serviço do Docker faz cada etapa.

## Os serviços

| Serviço | Papel |
|---|---|
| `agent` | Python com a interface Streamlit. Lê os arquivos, divide em blocos, faz o reranking, monta o prompt e conversa com os outros serviços. |
| `ollama` | Serve o modelo de embeddings (`nomic-embed-text`) e o LLM (`qwen2.5-coder:3b`). |
| `chroma` | Banco vetorial com o índice, guardado em volume. |

Detalhes de configuração, volumes e GPU estão em [Rodar tudo com Docker](Docker).

## 1. Indexação (uma vez)

1. O `DirectoryLoader` lê os arquivos do repositório (`.py`, `.js`, `.html`, `.yaml`, `.md`).
2. O `RecursiveCharacterTextSplitter` divide cada arquivo em blocos de cerca de 1.500 caracteres, respeitando a estrutura da linguagem, e guarda o arquivo e a linha de cada bloco.
3. O modelo de embeddings transforma cada bloco em um vetor.
4. Os vetores e os metadados entram no ChromaDB com `collection.add()`.

A indexação roda sozinha no primeiro start. Se o índice já existir, ela é pulada.

## 2. Consulta (a cada pergunta)

1. A pergunta vira um vetor com o mesmo modelo de embeddings.
2. `collection.query()` traz os 40 blocos mais parecidos.
3. O reranker (cross-encoder) lê a pergunta junto com cada bloco e fica com os 6 melhores.
4. O prompt junta a pergunta, os 6 trechos e a regra de responder só com o contexto e citar as fontes.
5. O LLM local gera a resposta.
6. A interface mostra a resposta com `arquivo:linha`, a tabela de fontes e os trechos, para você conferir.

## Por que assim

- Dividir por linguagem e guardar arquivo e linha permite citar a fonte exata: [Boas práticas de RAG](Boas-praticas-RAG).
- A busca vetorial é rápida, mas imprecisa. O reranking corrige a ordem dos candidatos: [Reranking](Reranking).
- Cada escolha foi medida com perguntas de referência: [Avaliação](Avaliacao).

## Editar o desenho

Os diagramas foram desenhados no estilo do Excalidraw. Para ajustar, baixe o arquivo [arquitetura-rag.excalidraw](https://github.com/edermendes2016/langchain-local-agent/blob/main/docs/img/arquitetura-rag.excalidraw) e abra em [excalidraw.com](https://excalidraw.com).
