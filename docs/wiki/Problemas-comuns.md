# Problemas comuns

| Sintoma | Causa provável | Solução |
|---|---|---|
| `LM Studio indisponível` | Servidor desligado ou modelo não carregado | Carregue `prism-ml/bonsai-27b` e inicie o servidor na aba Model Server |
| `A coleção está vazia` | Ainda não indexou esse repositório | `python agent_local.py index -r <nome>` |
| `Pasta não encontrada` | Repositório não clonado | `python agent_local.py clone -r <nome>` |
| `ConnectionResetError` no pip | Rede instável | `pip install --retries 10 --timeout 60 -r requirements.txt` |
| Aviso de symlinks do Hugging Face | Windows sem modo desenvolvedor | Inofensivo. Silencie com `$env:HF_HUB_DISABLE_SYMLINKS_WARNING=1` |
| Resposta diz que o contexto não tem a informação | A recuperação trouxe blocos errados | Use nomes exatos de classes, funções e arquivos, aumente `-k` ou ligue o reranking |
| Resposta lenta | Modelo de 27B | Normal. Reduza `-k` ou troque `llm_model` por um modelo menor |
| Pergunta em inglês é respondida em português | O prompt de sistema manda responder em português do Brasil | Limitação conhecida, ainda não alterada. Veja [Avaliação](Avaliacao#pontos-que-podem-ser-melhorados-nada-disso-foi-implementado) |
| Perguntas em português recuperam menos que em inglês | Os modelos padrão de embedding e de reranking são centrados em inglês | Limitação conhecida e medida. Uma pergunta em inglês ou nomes exatos de classes e funções ajudam. Melhorias em [Avaliação](Avaliacao#pontos-que-podem-ser-melhorados-nada-disso-foi-implementado) |

Variáveis de ambiente: `REPOS_CONFIG`, `CHROMA_PATH`, `EMBEDDING_MODEL`, `RERANKER_MODEL`, `LLM_BASE_URL`, `LLM_MODEL`.
