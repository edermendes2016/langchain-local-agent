"""
Avalia a recuperação (e opcionalmente as respostas) contra perguntas de referência.

  python evaluate.py -r langchain                 # busca vetorial vs. vetorial + reranking
  python evaluate.py -r aws-quiz --answers        # também gera respostas com o LLM local e confere

Métricas de recuperação (sobre os blocos, na ordem em que iriam para o LLM):
  hit@k     o top-k contém algum bloco de um arquivo esperado
  recall@k  fração dos arquivos esperados presentes no top-k
  MRR       média de 1 / posição do primeiro bloco correto
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

import yaml

warnings.filterwarnings("ignore")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from config import BASE_DIR, get_repo  # noqa: E402
from retriever import Retriever  # noqa: E402

KS = (1, 3, 5)
MAX_K = 10


def first_correct_rank(hits, expected):
    for pos, h in enumerate(hits, start=1):
        if h.source in expected:
            return pos
    return None


def retrieval_metrics(rows: list[dict], mode: str) -> dict:
    n = len(rows)
    out = {}
    for k in KS:
        out[f"hit@{k}"] = sum(1 for r in rows if r[mode]["rank"] and r[mode]["rank"] <= k) / n
        out[f"recall@{k}"] = sum(
            len(set(r["expected"]) & set(r[mode]["files"][:k])) / len(r["expected"]) for r in rows) / n
    out["MRR"] = sum(1 / r[mode]["rank"] for r in rows if r[mode]["rank"]) / n
    return out


def check_answer(text: str, item: dict) -> dict:
    low = text.lower()
    cites = any(f.lower() in low or Path(f).name.lower() in low for f in item["expected_files"])
    kw = [k for k in item.get("keywords", []) if str(k).lower() in low]
    return {"cites_expected_file": cites,
            "keywords_found": len(kw), "keywords_total": len(item.get("keywords", [])),
            "ok": cites and len(kw) == len(item.get("keywords", []))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--repo", default=None)
    ap.add_argument("--fetch-k", type=int, default=40, help="Candidatos buscados antes do reranking")
    ap.add_argument("--answers", action="store_true", help="Gera respostas com o LLM local e confere")
    ap.add_argument("-k", type=int, default=6, help="Blocos enviados ao LLM ao avaliar respostas")
    args = ap.parse_args()

    cfg = get_repo(args.repo)
    dataset = yaml.safe_load((BASE_DIR / "eval" / f"{cfg.name}.yaml").read_text(encoding="utf-8"))
    retriever = Retriever(cfg)
    if retriever.count() == 0:
        sys.exit(f"Coleção vazia. Rode: python agent_local.py index -r {cfg.name}")

    rows = []
    for item in dataset:
        expected = item["expected_files"]  # mesmo formato dos caminhos indexados (relativos à raiz do clone)
        vec = retriever.retrieve(item["question"], k=MAX_K, rerank=False)
        rer = retriever.retrieve(item["question"], k=MAX_K, rerank=True, fetch_k=args.fetch_k)
        rows.append({
            "id": item["id"], "question": item["question"], "expected": expected, "item": item,
            "vector": {"rank": first_correct_rank(vec, expected), "files": [h.source for h in vec]},
            "rerank": {"rank": first_correct_rank(rer, expected), "files": [h.source for h in rer]},
            "rerank_hits": rer,
        })

    m_vec, m_rer = retrieval_metrics(rows, "vector"), retrieval_metrics(rows, "rerank")

    lines = [f"# Avaliação de recuperação: {cfg.name}", "",
             f"{len(rows)} perguntas de referência, coleção `{cfg.collection}` ({retriever.count()} blocos), "
             f"reranker `{cfg.reranker_model}`, {args.fetch_k} candidatos antes do reranking.", "",
             "| Métrica | Busca vetorial | Vetorial + reranking |", "|---|---|---|"]
    for key in m_vec:
        lines.append(f"| {key} | {m_vec[key]:.2f} | {m_rer[key]:.2f} |")
    lines += ["", "## Posição do primeiro bloco correto", "",
              "| Id | Pergunta | Vetorial | Rerank |", "|---|---|---|---|"]
    fmt = lambda r: str(r) if r else f">{MAX_K}"  # noqa: E731
    for r in rows:
        lines.append(f"| {r['id']} | {r['question']} | {fmt(r['vector']['rank'])} | {fmt(r['rerank']['rank'])} |")

    answers = []
    if args.answers:
        from llm import answer, server_online
        if not server_online(cfg):
            sys.exit("LM Studio indisponível: ligue o servidor com o modelo carregado para avaliar respostas.")
        for i, r in enumerate(rows, start=1):
            print(f"[{i}/{len(rows)}] {r['question']}", flush=True)
            text, secs = answer(cfg, r["question"], r["rerank_hits"][:args.k])
            chk = check_answer(text, r["item"])
            answers.append({"id": r["id"], "seconds": round(secs, 1), "answer": text, **chk})
        ok = sum(a["ok"] for a in answers)
        cite = sum(a["cites_expected_file"] for a in answers)
        avg = sum(a["seconds"] for a in answers) / len(answers)
        lines += ["", "## Respostas do LLM local", "",
                  f"Modelo `{cfg.llm_model}`, k = {args.k}, com reranking.", "",
                  f"- Citam o arquivo esperado: **{cite}/{len(answers)}**",
                  f"- Citam o arquivo esperado e mencionam todas as palavras-chave: **{ok}/{len(answers)}**",
                  f"- Tempo médio por resposta: **{avg:.0f} s**", "",
                  "| Id | Cita o arquivo | Palavras-chave | Tempo |", "|---|---|---|---|"]
        for a in answers:
            lines.append(f"| {a['id']} | {'sim' if a['cites_expected_file'] else 'não'} | "
                         f"{a['keywords_found']}/{a['keywords_total']} | {a['seconds']:.0f} s |")
        lines += ["", "A conferência de respostas é automática e simples (texto contém o caminho ou o nome do arquivo "
                      "esperado e as palavras-chave). Ela mede ancoragem, não qualidade da redação."]

    out_dir = BASE_DIR / "eval" / "results"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{cfg.name}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out_dir / f"{cfg.name}.json").write_text(json.dumps({
        "repo": cfg.name, "date": time.strftime("%Y-%m-%d"), "fetch_k": args.fetch_k,
        "metrics": {"vector": m_vec, "rerank": m_rer},
        "questions": [{k: v for k, v in r.items() if k not in ("item", "rerank_hits")} for r in rows],
        "answers": answers}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
