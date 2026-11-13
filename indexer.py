"""Indexação: carrega arquivos, divide por linguagem e grava no ChromaDB com collection.add()."""

from __future__ import annotations

import hashlib
import time
from collections import defaultdict
from pathlib import Path

import chromadb
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

from config import CHROMA_HOST, CHROMA_PATH, CHROMA_PORT, RepoConfig

# Extensão -> linguagem do splitter. Sem entrada, usa os separadores genéricos.
LANGUAGE_BY_EXT = {
    ".py": Language.PYTHON,
    ".js": Language.JS,
    ".ts": Language.TS,
    ".html": Language.HTML,
    ".md": Language.MARKDOWN,
}
# Extensão -> nome da linguagem para realce de sintaxe na interface.
HIGHLIGHT_BY_EXT = {".py": "python", ".js": "javascript", ".ts": "typescript", ".html": "html",
                    ".css": "css", ".sh": "bash", ".yaml": "yaml", ".yml": "yaml", ".md": "markdown"}


def embedding_function(cfg: RepoConfig):
    """Embeddings locais: sentence-transformers (padrão) ou um modelo servido pelo Ollama."""
    if cfg.embedding_provider == "ollama":
        from chromadb.utils.embedding_functions import OllamaEmbeddingFunction
        return OllamaEmbeddingFunction(url=cfg.ollama_url, model_name=cfg.embedding_model, timeout=300)
    from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
    return SentenceTransformerEmbeddingFunction(model_name=cfg.embedding_model)


def get_client():
    """Servidor Chroma (Docker) quando CHROMA_HOST está definido; senão, banco em disco."""
    if CHROMA_HOST:
        return chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection(cfg: RepoConfig, reset: bool = False):
    """Cliente + coleção do repositório (padrão explícito do ChromaDB)."""
    chroma_client = get_client()
    if reset:
        try:
            chroma_client.delete_collection(cfg.collection)
        except Exception:
            pass
    collection = chroma_client.get_or_create_collection(
        name=cfg.collection,
        embedding_function=embedding_function(cfg),
        metadata={"hnsw:space": "cosine"},
    )
    return chroma_client, collection

def _splitter(ext: str, cfg: RepoConfig) -> RecursiveCharacterTextSplitter:
    kwargs = dict(chunk_size=cfg.chunk_size, chunk_overlap=cfg.chunk_overlap, add_start_index=True)
    lang = LANGUAGE_BY_EXT.get(ext)
    if lang:
        return RecursiveCharacterTextSplitter.from_language(language=lang, **kwargs)
    return RecursiveCharacterTextSplitter(**kwargs)


def load_documents(cfg: RepoConfig):
    docs = []
    for pattern in cfg.include:
        loader = DirectoryLoader(
            str(cfg.target),
            glob=pattern,
            exclude=cfg.exclude,
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8", "autodetect_encoding": True},
            use_multithreading=True,
            silent_errors=True,
        )
        docs.extend(loader.load())
    return docs


def index_repository(cfg: RepoConfig, reset: bool = False, batch_size: int = 64, log=print) -> int:
    if not cfg.target.exists():
        raise SystemExit(f"Pasta não encontrada: {cfg.target}\n"
                         f"Rode antes: python agent_local.py clone -r {cfg.name}")

    _, collection = get_collection(cfg, reset=reset)
    if collection.count() > 0:
        log(f"A coleção '{cfg.collection}' já tem {collection.count()} blocos. Use --reset para reindexar.")
        return collection.count()

    log(f"Carregando {cfg.include} de {cfg.target} ...")
    docs = load_documents(cfg)
    log(f"{len(docs)} arquivos carregados.")

    # Divide cada grupo de extensão com o splitter da sua linguagem
    by_ext = defaultdict(list)
    for d in docs:
        by_ext[Path(d.metadata["source"]).suffix.lower()].append(d)

    documents, metadatas, ids = [], [], []
    for ext, group in by_ext.items():
        splitter = _splitter(ext, cfg)
        text_by_source = {d.metadata["source"]: d.page_content for d in group}
        for chunk in splitter.split_documents(group):
            source = Path(chunk.metadata["source"]).resolve()
            rel = source.relative_to(cfg.path.resolve()).as_posix()
            start = int(chunk.metadata.get("start_index", 0))
            original = text_by_source[chunk.metadata["source"]]
            start_line = original.count("\n", 0, start) + 1
            end_line = start_line + chunk.page_content.count("\n")
            # Cabeçalho contextual: o caminho entra no texto embutido e ajuda perguntas sobre arquivos
            documents.append(f"# arquivo: {rel}\n{chunk.page_content}")
            metadatas.append({"source": rel, "start_line": start_line, "end_line": end_line,
                              "ext": ext, "repo": cfg.name})
            ids.append(hashlib.sha1(f"{cfg.name}:{rel}:{start}".encode()).hexdigest())

    log(f"{len(documents)} blocos gerados. Gravando no ChromaDB ...")
    t0 = time.time()
    for b in range(0, len(documents), batch_size):
        collection.add(  # inserção explícita
            documents=documents[b:b + batch_size],
            metadatas=metadatas[b:b + batch_size],
            ids=ids[b:b + batch_size],
        )
        log(f"  {min(b + batch_size, len(documents))}/{len(documents)} blocos indexados")
    log(f"Indexação concluída em {time.time() - t0:.1f}s. Total na coleção '{cfg.collection}': {collection.count()}")
    return collection.count()
