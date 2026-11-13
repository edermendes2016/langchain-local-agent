"""
CLI do agente RAG local.

  python agent_local.py repos                       # lista os repositórios configurados
  python agent_local.py clone -r aws-quiz           # clona o repositório do repos.yaml
  python agent_local.py index -r aws-quiz [--reset] # indexa no ChromaDB
  python agent_local.py ask "pergunta" -r aws-quiz  # recupera, reordena e responde com o LLM local
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import warnings

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import default_repo, get_repo, list_repos  # noqa: E402


def cmd_repos(_):
    for name in list_repos():
        cfg = get_repo(name)
        marca = "*" if name == default_repo() else " "
        print(f"{marca} {name:12} {cfg.description}  [{cfg.collection}]")


def cmd_clone(args):
    cfg = get_repo(args.repo)
    if (cfg.path / ".git").exists():
        print(f"Já clonado em {cfg.path}")
        return
    cfg.path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "clone", "--depth", "1", cfg.url, str(cfg.path)], check=True)


def cmd_index(args):
    from indexer import index_repository
    index_repository(get_repo(args.repo), reset=args.reset)


def _wait(label, check, timeout=1800, every=3):
    import time
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            if check():
                print(f"[ok] {label}", flush=True)
                return
        except Exception:
            pass
        time.sleep(every)
    sys.exit(f"Tempo esgotado esperando: {label}")


def cmd_bootstrap(_):
    """Usado pelo Docker: espera os serviços, clona e indexa o que ainda não estiver no Chroma."""
    import os

    import requests

    from config import CHROMA_HOST, CHROMA_PORT
    from indexer import index_repository

    cfg0 = get_repo(None)
    if CHROMA_HOST:
        _wait("Chroma", lambda: requests.get(f"http://{CHROMA_HOST}:{CHROMA_PORT}/api/v2/heartbeat", timeout=3).ok)
    if cfg0.embedding_provider == "ollama":
        models = [cfg0.embedding_model, cfg0.llm_model]
        def has_models():
            tags = requests.get(cfg0.ollama_url.rstrip("/") + "/api/tags", timeout=5).json()["models"]
            names = {m["name"] for m in tags} | {m["name"].split(":")[0] for m in tags}
            return all(m in names or m.split(":")[0] + ":latest" in names for m in models)
        _wait("modelos do Ollama (" + ", ".join(models) + ")", has_models)

    for name in os.getenv("BOOTSTRAP_REPOS", cfg0.name).split(","):
        cfg = get_repo(name.strip())
        cmd_clone(argparse.Namespace(repo=cfg.name))
        # só indexa se a coleção estiver vazia (index_repository avisa e sai quando já há blocos)
        index_repository(cfg, reset=False)


def cmd_ask(args):
    from llm import answer, server_online
    from retriever import Retriever

    cfg = get_repo(args.repo)
    retriever = Retriever(cfg)
    if retriever.count() == 0:
        sys.exit(f"A coleção '{cfg.collection}' está vazia. Rode: python agent_local.py index -r {cfg.name}")

    use_rerank = not args.no_rerank
    print(f"\nREPOSITÓRIO: {cfg.name}\nPERGUNTA: {args.question}\n")
    hits = retriever.retrieve(args.question, k=args.k, rerank=use_rerank, fetch_k=args.fetch_k)
    modo = "busca vetorial + reranking" if use_rerank else "busca vetorial"
    print(f"--- DOCUMENTOS RECUPERADOS DA '{cfg.collection}' ({modo}) ---")
    for n, h in enumerate(hits, start=1):
        extra = f"rerank {h.rerank_score:+.2f}, posição vetorial #{h.vector_rank}" if use_rerank else ""
        print(f"[{n}] {h.ref}  (similaridade {h.vector_score:.3f}{', ' + extra if extra else ''})")

    if args.sources_only:
        return
    if not server_online(cfg):
        sys.exit(f"\nLM Studio indisponível em {cfg.llm_base_url} ou modelo '{cfg.llm_model}' não carregado.\n"
                 "Abra o LM Studio, carregue o modelo e ligue o servidor na aba Model Server.")
    print(f"\nConsultando {cfg.llm_model} em {cfg.llm_base_url} ...")
    text, secs = answer(cfg, args.question, hits)
    print(f"\n--- RESPOSTA DO AGENTE ({secs:.1f}s) ---\n\n{text}")


def main():
    parser = argparse.ArgumentParser(description="Agente RAG local sobre repositórios de código")
    sub = parser.add_subparsers(dest="cmd", required=True)

    def add_repo(p):
        p.add_argument("-r", "--repo", default=None, help=f"Nome em repos.yaml (padrão: {default_repo()})")

    add_repo(sub.add_parser("repos", help="Lista os repositórios configurados"))
    add_repo(sub.add_parser("clone", help="Clona o repositório configurado"))
    p_index = sub.add_parser("index", help="Indexa os arquivos no ChromaDB")
    add_repo(p_index)
    p_index.add_argument("--reset", action="store_true", help="Apaga e recria a coleção")
    sub.add_parser("bootstrap", help="Espera serviços, clona e indexa automaticamente (Docker)")
    p_ask = sub.add_parser("ask", help="Faz uma pergunta sobre o código")
    add_repo(p_ask)
    p_ask.add_argument("question")
    p_ask.add_argument("-k", type=int, default=6, help="Quantidade de blocos enviados ao LLM")
    p_ask.add_argument("--no-rerank", action="store_true", help="Usa só a busca vetorial")
    p_ask.add_argument("--fetch-k", type=int, default=None, help="Candidatos buscados antes do reranking")
    p_ask.add_argument("--sources-only", action="store_true", help="Mostra só as fontes, sem chamar o LLM")

    args = parser.parse_args()
    {"repos": cmd_repos, "clone": cmd_clone, "index": cmd_index, "ask": cmd_ask,
     "bootstrap": cmd_bootstrap}[args.cmd](args)


if __name__ == "__main__":
    main()
