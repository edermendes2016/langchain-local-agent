"""Recuperação em duas etapas: busca vetorial ampla no ChromaDB + reranking com cross-encoder."""

from __future__ import annotations

from dataclasses import dataclass

from config import RepoConfig
from indexer import get_collection

_RERANKERS: dict[str, object] = {}


def _reranker(model_name: str):
    if model_name not in _RERANKERS:
        from sentence_transformers import CrossEncoder
        _RERANKERS[model_name] = CrossEncoder(model_name)
    return _RERANKERS[model_name]


@dataclass
class Hit:
    source: str
    start_line: int
    end_line: int
    text: str
    vector_score: float  # similaridade de cosseno (1 - distância)
    vector_rank: int  # posição na busca vetorial (1 = melhor)
    rerank_score: float | None = None

    @property
    def ref(self) -> str:
        return f"{self.source}:{self.start_line}"

    @property
    def ext(self) -> str:
        return "." + self.source.rsplit(".", 1)[-1] if "." in self.source else ""

    @property
    def score(self) -> float:
        return self.rerank_score if self.rerank_score is not None else self.vector_score


class Retriever:
    def __init__(self, cfg: RepoConfig):
        self.cfg = cfg
        _, self.collection = get_collection(cfg)

    def count(self) -> int:
        return self.collection.count()

    def vector_search(self, question: str, n: int) -> list[Hit]:
        """Etapa 1: collection.query() devolve os n blocos mais próximos da pergunta."""
        res = self.collection.query(query_texts=[question], n_results=n)
        hits = []
        for rank, (doc, meta, dist) in enumerate(
                zip(res["documents"][0], res["metadatas"][0], res["distances"][0]), start=1):
            text = doc.split("\n", 1)[1] if doc.startswith("# arquivo: ") else doc  # tira o cabeçalho contextual
            hits.append(Hit(meta["source"], meta["start_line"], meta["end_line"], text, 1 - dist, rank))
        return hits

    def rerank(self, question: str, hits: list[Hit]) -> list[Hit]:
        """Etapa 2: o cross-encoder lê pergunta e bloco juntos e reordena os candidatos."""
        model = _reranker(self.cfg.reranker_model)
        pairs = [(question, f"{h.source}\n{h.text}") for h in hits]
        scores = model.predict(pairs, show_progress_bar=False)
        for h, s in zip(hits, scores):
            h.rerank_score = float(s)
        return sorted(hits, key=lambda h: h.rerank_score, reverse=True)

    def retrieve(self, question: str, k: int = 6, rerank: bool = True, fetch_k: int | None = None) -> list[Hit]:
        """Top-k final. Com rerank, busca fetch_k candidatos (padrão 4x k, mínimo 20) e mantém os k melhores."""
        if not rerank:
            return self.vector_search(question, k)
        fetch_k = max(fetch_k or 0, k, 4 * k, 20)
        candidates = self.vector_search(question, min(fetch_k, self.count()))
        return self.rerank(question, candidates)[:k]
