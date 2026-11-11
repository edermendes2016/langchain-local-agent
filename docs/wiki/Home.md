# Agente RAG local para o código do LangChain

Passo a passo para rodar tudo na sua máquina: um modelo local no LM Studio, um banco vetorial ChromaDB e um script Python que responde perguntas sobre o código-fonte do LangChain citando arquivo e linha.

## Roteiro

1. [Subir o LLM local no LM Studio](1-LM-Studio)
2. [Preparar o ambiente Python](2-Ambiente-Python)
3. [Indexar o código no ChromaDB](3-Indexacao)
4. [Enviar um prompt e receber a resposta](4-Consulta-RAG)
5. [Problemas comuns](5-Problemas-comuns)

## Como funciona, em uma linha

pergunta → `collection.query()` no ChromaDB → trechos de código relevantes → `ChatOpenAI` apontando para o LM Studio (`prism-ml/bonsai-27b`) → resposta com fontes.

## Requisitos

- Windows 11, Python 3.12, Git
- LM Studio com o modelo `prism-ml/bonsai-27b` baixado
- Cerca de 3 GB livres em disco para as dependências (o PyTorch é a maior parte)

Código: https://github.com/edermendes2016/langchain-local-agent
