# Indexação

```powershell
python agent_local.py index -r langchain
python agent_local.py index -r aws-quiz
```

O que acontece com cada repositório do `repos.yaml`:

1. O `DirectoryLoader` lê os arquivos que casam com `include`, ignorando o que está em `exclude`.
2. O `RecursiveCharacterTextSplitter` divide cada arquivo com o splitter da sua linguagem (Python, JavaScript, HTML, Markdown) ou com separadores genéricos para YAML, shell e CSS.
3. Cada bloco entra na coleção do repositório com o método explícito do ChromaDB:

```python
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="tutorial_collection", ...)
collection.add(documents=[...], metadatas=[...], ids=[...])
```

Os metadados guardam arquivo, linha inicial e final, extensão e nome do repositório. Os ids são determinísticos (hash de repositório, arquivo e posição), então a mesma entrada sempre gera o mesmo id.

Resultado nesta máquina: `langchain` com 187 arquivos e 2.347 blocos em cerca de 45 s; `aws-quiz` com 12 arquivos e 40 blocos em cerca de 1 s. Na primeira execução o modelo de embeddings `all-MiniLM-L6-v2` é baixado.

![Indexação concluída](images/03-indexacao.png)

Para refazer do zero: `python agent_local.py index -r langchain --reset`.

Próximo: [Consulta RAG](Consulta-RAG)
