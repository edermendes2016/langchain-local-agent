# Reranking

## O problema

A busca vetorial compara a pergunta com cada bloco separadamente e é rápida, mas imprecisa: os embeddings comprimem o texto num único vetor, e blocos genéricos às vezes ficam acima do bloco que realmente responde. Como só os `k` primeiros vão para o LLM, um acerto na posição 6 é um acerto perdido.

No `aws-quiz`, para a pergunta "Como o backend Lambda valida a resposta do usuário no quiz?", a busca vetorial trouxe três blocos de `questions.js` e um de `template.yaml`. O arquivo `backend/lambda_function.py` estava só na posição 6 e o modelo respondeu que o contexto não bastava.

## A solução em duas etapas

1. **Busca ampla.** `collection.query()` devolve `fetch_k` candidatos, por padrão `max(20, 4 × k)`.
2. **Reordenação.** Um cross-encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) lê pergunta e bloco juntos e dá uma nota de relevância. Os `k` melhores seguem para o LLM.

```python
candidates = retriever.vector_search(question, n=20)   # collection.query()
ranked = retriever.rerank(question, candidates)         # CrossEncoder.predict()
top_k = ranked[:6]
```

Um cross-encoder é mais preciso que a comparação de vetores porque enxerga pergunta e texto ao mesmo tempo, mas é mais caro. Por isso ele só reordena os poucos candidatos da primeira etapa, e não o repositório inteiro.

Com reranking, a mesma pergunta passou a trazer `backend/lambda_function.py` para dentro do top 4.

## Como usar

- Linha de comando: ligado por padrão. Use `--no-rerank` para comparar e `--fetch-k 40` para ampliar os candidatos.
- Interface: chave **Reranking com cross-encoder** na barra lateral. A tabela de fontes mostra a posição vetorial de cada bloco e a nota do reranker.

```powershell
python agent_local.py ask "Como o backend Lambda valida a resposta?" -r aws-quiz -k 4 --sources-only
python agent_local.py ask "Como o backend Lambda valida a resposta?" -r aws-quiz -k 4 --sources-only --no-rerank
```

O ganho medido em perguntas de referência está em [Avaliação](Avaliacao).

## Trocar o modelo

Altere `reranker_model` no `repos.yaml` ou a variável `RERANKER_MODEL`. Qualquer cross-encoder do `sentence-transformers` serve.
