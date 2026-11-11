"""
Agente RAG local para análise de código do repositório LangChain.

Fluxo:
  1. index  -> carrega arquivos .py com DirectoryLoader, divide com RecursiveCharacterTextSplitter
               e grava os blocos no ChromaDB via collection.add(documents, metadatas, ids).
  2. ask    -> recupera os blocos mais relevantes com collection.query() e envia o contexto
               para o LLM local (LM Studio, modelo prism-ml/bonsai-27b) via ChatOpenAI.

Uso:
  python agent_local.py index                      # indexa o escopo padrão (libs/core/langchain_core)
  python agent_local.py index --scope libs --reset # reindexa todo o diretório libs
  python agent_local.py ask "Onde fica a classe base dos modelos de chat?"
  python agent_local.py ask                        # roda a pergunta arquitetural de demonstração
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
from pathlib import Path

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_openai import ChatOpenAI
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

# Saída UTF-8 no terminal do Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# Configuração (pode ser sobrescrita por variáveis de ambiente)
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
REPO_PATH = Path(os.getenv("REPO_PATH", BASE_DIR / "langchain_repo"))
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))
COLLECTION_NAME = "tutorial_collection"
DEFAULT_SCOPE = "libs/core/langchain_core"

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")  # sentence-transformers, roda local
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:1234/v1")  # LM Studio
LLM_MODEL = os.getenv("LLM_MODEL", "prism-ml/bonsai-27b")

DEMO_QUESTION = (
    "Onde está implementada a classe base dos modelos de chat (BaseChatModel) "
    "e como o método invoke chega até a geração da resposta?"
)

SYSTEM_PROMPT = (
    "Você é um arquiteto de software analisando o código-fonte do LangChain. "
    "Responda em português do Brasil usando APENAS os trechos de código fornecidos no contexto. "
    "Cite os arquivos (caminho e linha) que sustentam cada afirmação. "
    "Se o contexto não for suficiente, diga isso claramente em vez de inventar."
)


# ---------------------------------------------------------------------------
# ChromaDB: cliente e coleção (padrão explícito)
# ---------------------------------------------------------------------------
def get_collection():
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    embedding_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    collection = chroma_client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )
    return chroma_client, collection


# ---------------------------------------------------------------------------
# Indexação
# ---------------------------------------------------------------------------
def index_repository(scope: str, reset: bool, batch_size: int = 256) -> None:
    target = REPO_PATH / scope
    if not target.exists():
        sys.exit(f"Pasta não encontrada: {target}. Clone o repositório antes:\n"
                 f"  git clone --depth 1 https://github.com/langchain-ai/langchain.git {REPO_PATH}")

    chroma_client, collection = get_collection()
    if reset:
        chroma_client.delete_collection(COLLECTION_NAME)
        chroma_client, collection = get_collection()
    elif collection.count() > 0:
        print(f"A coleção '{COLLECTION_NAME}' já tem {collection.count()} blocos. "
              "Use --reset para reindexar.")
        return

    print(f"Carregando arquivos .py de {target} ...")
    loader = DirectoryLoader(
        str(target),
        glob="**/*.py",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
        show_progress=True,
        use_multithreading=True,
        silent_errors=True,
    )
    docs = loader.load()
    print(f"{len(docs)} arquivos carregados.")

    # Splitter com separadores próprios para Python (class, def, ...)
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON,
        chunk_size=1500,
        chunk_overlap=200,
        add_start_index=True,
    )
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} blocos gerados. Gravando no ChromaDB ...")

    # Linha inicial de cada bloco (para citar arquivo:linha na resposta)
    file_text = {d.metadata["source"]: d.page_content for d in docs}

    documents, metadatas, ids = [], [], []
    for i, chunk in enumerate(chunks):
        source = chunk.metadata["source"]
        start = chunk.metadata.get("start_index", 0)
        line = file_text[source].count("\n", 0, max(start, 0)) + 1
        rel = Path(source).resolve().relative_to(REPO_PATH.resolve()).as_posix()
        documents.append(chunk.page_content)
        metadatas.append({"source": rel, "start_line": line})
        ids.append(hashlib.sha1(f"{rel}:{start}:{i}".encode()).hexdigest())

    t0 = time.time()
    for b in range(0, len(documents), batch_size):
        # Inserção explícita com collection.add()
        collection.add(
            documents=documents[b:b + batch_size],
            metadatas=metadatas[b:b + batch_size],
            ids=ids[b:b + batch_size],
        )
        done = min(b + batch_size, len(documents))
        print(f"  {done}/{len(documents)} blocos indexados", end="\r")
    print(f"\nIndexação concluída em {time.time() - t0:.1f}s. Total na coleção: {collection.count()}")


# ---------------------------------------------------------------------------
# Consulta RAG
# ---------------------------------------------------------------------------
def ask(question: str, k: int = 6) -> None:
    _, collection = get_collection()
    if collection.count() == 0:
        sys.exit("A coleção está vazia. Rode primeiro: python agent_local.py index")

    print(f"\nPERGUNTA: {question}\n")
    results = collection.query(query_texts=[question], n_results=k)

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    dists = results["distances"][0]

    print(f"--- DOCUMENTOS RECUPERADOS DA '{COLLECTION_NAME}' ---")
    context_parts = []
    for n, (doc, meta, dist) in enumerate(zip(docs, metas, dists), start=1):
        ref = f"{meta['source']}:{meta['start_line']}"
        print(f"[{n}] {ref}  (similaridade {1 - dist:.3f})")
        context_parts.append(f"### Fonte [{n}] {ref}\n```python\n{doc}\n```")
    context = "\n\n".join(context_parts)

    llm = ChatOpenAI(
        model=LLM_MODEL,
        base_url=LLM_BASE_URL,
        api_key="lm-studio",
        temperature=0,
        timeout=600,
    )
    messages = [
        ("system", SYSTEM_PROMPT),
        ("human", f"Contexto recuperado do repositório:\n\n{context}\n\nPergunta: {question}"),
    ]

    print(f"\nConsultando {LLM_MODEL} em {LLM_BASE_URL} ...")
    t0 = time.time()
    try:
        answer = llm.invoke(messages).content
    except Exception as exc:  # LM Studio fechado ou modelo não carregado
        sys.exit(f"\nFalha ao falar com o LM Studio: {exc}\n"
                 f"Abra o LM Studio, carregue o modelo '{LLM_MODEL}' e ligue o servidor local na porta 1234.")

    # Alguns modelos locais devolvem o raciocínio entre <think>...</think>
    answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

    print(f"\n--- RESPOSTA DO AGENTE ({time.time() - t0:.1f}s) ---\n")
    print(answer)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Agente RAG local sobre o código do LangChain")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_index = sub.add_parser("index", help="Indexa os arquivos .py no ChromaDB")
    p_index.add_argument("--scope", default=DEFAULT_SCOPE,
                         help=f"Subpasta do repositório a indexar (padrão: {DEFAULT_SCOPE})")
    p_index.add_argument("--reset", action="store_true", help="Apaga e recria a coleção")

    p_ask = sub.add_parser("ask", help="Faz uma pergunta sobre o código")
    p_ask.add_argument("question", nargs="?", default=DEMO_QUESTION)
    p_ask.add_argument("-k", type=int, default=6, help="Quantidade de blocos recuperados")

    args = parser.parse_args()
    if args.cmd == "index":
        index_repository(args.scope, args.reset)
    else:
        ask(args.question, args.k)


if __name__ == "__main__":
    main()
