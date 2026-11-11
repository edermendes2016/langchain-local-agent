"""Recuperação: busca vetorial no ChromaDB com collection.query()."""

from __future__ import annotations

from dataclasses import dataclass

from config import RepoConfig
from indexer import get_collection


@dataclass
class Hit:
    source: str
    start_line: int
    end_line: int
    text: str
    vector_score: float  # similaridade de cosseno (1 - distância)
    rerank_score: float | None = None

    @property
    def ref(self) -> str:
        return f"{self.source}:{self.start_line}"

    @property
    def ext(self) -> str:
        return "." + self.source.rsplit(".", 1)[-1] if "." in self.source else ""


class Retriever:
    def __init__(self, cfg: RepoConfig):
        self.cfg = cfg
        _, self.collection = get_collection(cfg)

    def count(self) -> int:
        return self.collection.count()

    def retrieve(self, question: str, k: int = 6) -> list[Hit]:
        res = self.collection.query(query_texts=[question], n_results=k)
        hits = []
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
            text = doc.split("\n", 1)[1] if doc.startswith("# arquivo: ") else doc  # tira o cabeçalho contextual
            hits.append(Hit(meta["source"], meta["start_line"], meta["end_line"], text, 1 - dist))
        return hits
