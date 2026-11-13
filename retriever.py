"""Recuperação em duas etapas: busca vetorial ampla no ChromaDB + reranking.

Reranking configurável (`reranker` no repos.yaml ou variável RERANKER):
  cross-encoder  modelo cross-encoder do sentence-transformers (mais preciso, exige PyTorch)
  bm25           fusão RRF entre a ordem vetorial e a ordem lexical BM25 (leve, ótimo para nomes exatos)
  none           só busca vetorial
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from config import RepoConfig
from indexer import get_collection

_RERANKERS: dict[str, object] = {}
RRF_K = 60  # constante padrão da Reciprocal Rank Fusion


def _cross_encoder(model_name: str):
    if model_name not in _RERANKERS:
        from sentence_transformers import CrossEncoder
        _RERANKERS[model_name] = CrossEncoder(model_name)
    return _RERANKERS[model_name]


def _tokens(text: str) -> list[str]:
    """Tokeniza código: separa por não alfanuméricos e também por camelCase/snake_case."""
    out = []
    for word in re.findall(r"[A-Za-z_][A-Za-z0-9_]*|\d+", text):
        out.append(word.lower())
        parts = re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", word.replace("_", " "))
        if len(parts) > 1:
            out.extend(p.lower() for p in parts)
    return out


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
        """Etapa 2: reordena os candidatos conforme o reranker configurado."""
        mode = self.cfg.reranker
        if mode == "cross-encoder":
            model = _cross_encoder(self.cfg.reranker_model)
            scores = model.predict([(question, f"{h.source}\n{h.text}") for h in hits], show_progress_bar=False)
            for h, s in zip(hits, scores):
                h.rerank_score = float(s)
        elif mode == "bm25":
            from rank_bm25 import BM25Okapi
            bm25 = BM25Okapi([_tokens(f"{h.source} {h.text}") for h in hits])
            lexical = bm25.get_scores(_tokens(question))
            order = sorted(range(len(hits)), key=lambda i: lexical[i], reverse=True)
            lex_rank = {i: r for r, i in enumerate(order, start=1)}
            for i, h in enumerate(hits):  # Reciprocal Rank Fusion: vetorial + lexical
                h.rerank_score = 1 / (RRF_K + h.vector_rank) + 1 / (RRF_K + lex_rank[i])
        else:
            return hits
        return sorted(hits, key=lambda h: h.rerank_score, reverse=True)

    def retrieve(self, question: str, k: int = 6, rerank: bool = True, fetch_k: int | None = None) -> list[Hit]:
        """Top-k final. Com rerank, busca fetch_k candidatos (padrão 4x k, mínimo 20) e mantém os k melhores."""
        if not rerank or self.cfg.reranker == "none":
            return self.vector_search(question, k)
        fetch_k = max(fetch_k or 0, k, 4 * k, 20)
        candidates = self.vector_search(question, min(fetch_k, self.count()))
        return self.rerank(question, candidates)[:k]
