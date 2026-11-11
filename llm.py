"""Geração: envia o contexto recuperado ao LLM local (LM Studio) via ChatOpenAI."""

from __future__ import annotations

import re
import time

import requests
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config import RepoConfig
from retriever import Hit

SYSTEM_PROMPT = (
    "Você é um engenheiro de software sênior analisando o código-fonte de um repositório. "
    "Responda em português do Brasil usando APENAS os trechos fornecidos no contexto. "
    "Cite as fontes no formato [n] arquivo:linha para cada afirmação. "
    "Se o contexto não for suficiente, diga isso claramente em vez de inventar."
)


def build_context(hits: list[Hit]) -> str:
    parts = [f"### Fonte [{i}] {h.ref}\n```\n{h.text}\n```" for i, h in enumerate(hits, start=1)]
    return "\n\n".join(parts)


def server_online(cfg: RepoConfig, timeout: float = 3.0) -> bool:
    """Verifica se o LM Studio responde e se o modelo está disponível."""
    try:
        r = requests.get(cfg.llm_base_url.rstrip("/") + "/models", timeout=timeout)
        return any(m["id"] == cfg.llm_model for m in r.json().get("data", []))
    except Exception:
        return False


def answer(cfg: RepoConfig, question: str, hits: list[Hit]) -> tuple[str, float]:
    llm = ChatOpenAI(model=cfg.llm_model, base_url=cfg.llm_base_url, api_key="lm-studio",
                     temperature=0, timeout=900)
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Contexto recuperado do repositório:\n\n{build_context(hits)}\n\nPergunta: {question}"),
    ]
    t0 = time.time()
    text = llm.invoke(messages).content
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()  # alguns modelos expõem o raciocínio
    return text, time.time() - t0
