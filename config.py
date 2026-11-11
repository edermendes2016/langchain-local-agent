"""Leitura do repos.yaml e resolução das configurações de cada repositório."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = Path(os.getenv("REPOS_CONFIG", BASE_DIR / "repos.yaml"))
CHROMA_PATH = os.getenv("CHROMA_PATH", str(BASE_DIR / "chroma_db"))


@dataclass(frozen=True)
class RepoConfig:
    name: str
    description: str
    url: str
    path: Path
    scope: str
    include: list[str]
    exclude: list[str]
    collection: str
    chunk_size: int
    chunk_overlap: int
    embedding_model: str
    reranker_model: str
    llm_base_url: str
    llm_model: str
    extra: dict = field(default_factory=dict)

    @property
    def target(self) -> Path:
        """Pasta efetivamente indexada (repositório + escopo)."""
        return (self.path / self.scope).resolve()


def _load() -> dict:
    with open(CONFIG_FILE, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def list_repos() -> list[str]:
    return list(_load()["repos"].keys())


def default_repo() -> str:
    return _load().get("default_repo") or list_repos()[0]


def get_repo(name: str | None = None) -> RepoConfig:
    raw = _load()
    name = name or default_repo()
    if name not in raw["repos"]:
        raise SystemExit(f"Repositório '{name}' não existe em {CONFIG_FILE.name}. "
                         f"Disponíveis: {', '.join(raw['repos'])}")
    d = raw.get("defaults", {})
    r = raw["repos"][name]

    def pick(key, fallback=None):
        return r.get(key, d.get(key, fallback))

    path = Path(r["path"])
    if not path.is_absolute():
        path = BASE_DIR / path
    return RepoConfig(
        name=name,
        description=r.get("description", name),
        url=r["url"],
        path=path,
        scope=r.get("scope", "."),
        include=r.get("include", ["**/*.py"]),
        exclude=list(d.get("exclude", [])) + list(r.get("exclude", [])),
        collection=r.get("collection", name.replace("_", "-")),
        chunk_size=int(pick("chunk_size", 1500)),
        chunk_overlap=int(pick("chunk_overlap", 200)),
        embedding_model=os.getenv("EMBEDDING_MODEL", pick("embedding_model", "all-MiniLM-L6-v2")),
        reranker_model=os.getenv("RERANKER_MODEL", pick("reranker_model", "cross-encoder/ms-marco-MiniLM-L-6-v2")),
        llm_base_url=os.getenv("LLM_BASE_URL", pick("llm_base_url", "http://localhost:1234/v1")),
        llm_model=os.getenv("LLM_MODEL", pick("llm_model", "prism-ml/bonsai-27b")),
    )
