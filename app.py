"""Interface Streamlit para navegar por perguntas, fontes e trechos recuperados.

  streamlit run app.py
"""

from __future__ import annotations

import warnings

import streamlit as st

warnings.filterwarnings("ignore")

from config import get_repo, list_repos, default_repo  # noqa: E402
from indexer import HIGHLIGHT_BY_EXT  # noqa: E402
from llm import answer, server_online  # noqa: E402
from retriever import Retriever  # noqa: E402

st.set_page_config(page_title="Agente RAG local", page_icon="🔎", layout="wide")


@st.cache_resource(show_spinner="Carregando banco vetorial e modelo de embeddings...")
def load_retriever(repo: str) -> Retriever:
    return Retriever(get_repo(repo))


@st.cache_data(ttl=10)
def lm_online(repo: str) -> bool:
    return server_online(get_repo(repo))


# ----------------------------------------------------------------------------- barra lateral
repos = list_repos()
with st.sidebar:
    st.title("Agente RAG local")
    repo = st.selectbox("Repositório", repos, index=repos.index(default_repo()),
                        format_func=lambda n: f"{n}  |  {get_repo(n).description}")
    cfg = get_repo(repo)
    retriever = load_retriever(repo)
    k = st.slider("Blocos enviados ao LLM (k)", 1, 15, 6)
    use_llm = st.toggle("Gerar resposta com o LLM local", value=True,
                        help="Desligue para navegar apenas pelas fontes recuperadas (instantâneo).")

    st.divider()
    st.caption(f"Coleção: `{cfg.collection}`  \nBlocos indexados: **{retriever.count()}**")
    st.caption(f"Embeddings: `{cfg.embedding_model}`")
    online = lm_online(repo)
    st.caption(f"LLM: `{cfg.llm_model}`  \n" + ("🟢 servidor online" if online else "🔴 servidor offline"))

    if st.button("Limpar histórico"):
        st.session_state.history = []

if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------------------------------------------------------- consulta
st.header("Pergunte sobre o código")
if retriever.count() == 0:
    st.warning(f"A coleção `{cfg.collection}` está vazia. Rode no terminal: "
               f"`python agent_local.py index -r {repo}`")
    st.stop()

with st.form("pergunta"):
    question = st.text_area("Pergunta", height=90, placeholder="Ex.: Onde fica a classe base dos modelos de chat?")
    submitted = st.form_submit_button("Perguntar", type="primary")

if submitted and question.strip():
    with st.spinner("Buscando trechos no ChromaDB..."):
        hits = retriever.retrieve(question.strip(), k=k)
    text, secs = None, None
    if use_llm:
        if not online:
            st.error("LM Studio offline ou modelo não carregado. Mostrando só as fontes.")
        else:
            with st.spinner(f"Consultando {cfg.llm_model} (pode levar mais de 1 minuto)..."):
                try:
                    text, secs = answer(cfg, question.strip(), hits)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Falha ao consultar o LLM: {exc}")
    st.session_state.history.insert(0, {"repo": repo, "question": question.strip(), "k": k,
                                        "hits": hits, "answer": text, "secs": secs})

# ----------------------------------------------------------------------------- resultados
for i, item in enumerate(st.session_state.history):
    with st.container(border=True):
        st.subheader(item["question"])
        st.caption(f"Repositório: {item['repo']}  |  k = {item['k']}")
        if item["answer"]:
            st.markdown(f"**Resposta** ({item['secs']:.0f}s)")
            st.markdown(item["answer"])

        st.markdown("**Fontes recuperadas**")
        st.dataframe(
            [{"#": n, "Arquivo": h.source, "Linha": h.start_line, "Similaridade": round(h.vector_score, 3)}
             for n, h in enumerate(item["hits"], start=1)],
            hide_index=True, width="stretch",
        )
        for n, h in enumerate(item["hits"], start=1):
            with st.expander(f"[{n}] {h.source}:{h.start_line}-{h.end_line}  (similaridade {h.vector_score:.3f})",
                             expanded=(i == 0 and n == 1)):
                st.code(h.text, language=HIGHLIGHT_BY_EXT.get(h.ext, None), line_numbers=False)
