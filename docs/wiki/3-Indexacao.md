# 3. Indexar o código no ChromaDB

```powershell
python agent_local.py index
```

O que acontece:

1. O `DirectoryLoader` lê todos os `.py` de `libs/core/langchain_core`.
2. O `RecursiveCharacterTextSplitter` (modo Python) corta em blocos de 1500 caracteres, respeitando `class` e `def`.
3. Cada bloco vai para a coleção com o método explícito do ChromaDB:

```python
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="tutorial_collection", ...)
collection.add(documents=[...], metadatas=[...], ids=[...])
```

Os metadados guardam o arquivo e a linha inicial, que depois aparecem nas respostas.

Na primeira execução o modelo de embeddings `all-MiniLM-L6-v2` é baixado automaticamente. Resultado esperado no núcleo do LangChain: cerca de 187 arquivos, 2.347 blocos e perto de 30 segundos.

![Indexação concluída](images/03-indexacao.png)

Para indexar outra parte do repositório ou refazer do zero:

```powershell
python agent_local.py index --scope libs --reset
```

Próximo passo: [Enviar um prompt](4-Consulta-RAG)
