# 5. Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `Falha ao falar com o LM Studio` | Servidor desligado ou modelo não carregado | Abra o LM Studio, carregue `prism-ml/bonsai-27b` e inicie o servidor na aba Model Server |
| `A coleção está vazia` | Ainda não rodou a indexação | `python agent_local.py index` |
| `Pasta não encontrada` | `langchain_repo` não foi clonado | `git clone --depth 1 https://github.com/langchain-ai/langchain.git langchain_repo` |
| Download do pip falha com `ConnectionResetError` | Rede instável | `pip install --retries 10 --timeout 60 -r requirements.txt` |
| Aviso sobre symlinks do Hugging Face | Windows sem modo desenvolvedor | Inofensivo. Silencie com `$env:HF_HUB_DISABLE_SYMLINKS_WARNING=1` |
| Resposta diz que o contexto não tem a informação | Recuperação trouxe blocos errados | Use `-k 10` e nomes exatos de classes e métodos na pergunta |
| Resposta muito lenta | Modelo de 27B | Normal. Reduza `-k` ou use um modelo menor via `LLM_MODEL` |

Variáveis de ambiente úteis: `REPO_PATH`, `CHROMA_PATH`, `EMBEDDING_MODEL`, `LLM_BASE_URL`, `LLM_MODEL`.
