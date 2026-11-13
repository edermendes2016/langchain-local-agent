# Avaliação com perguntas de referência

Sem medir, "melhorou" é só impressão. O projeto traz 30 perguntas de referência, cada uma com os arquivos corretos conferidos no código (18 do `langchain`, 12 do `aws-quiz`), em `eval/langchain.yaml` e `eval/aws-quiz.yaml`.

```yaml
- id: lc07
  question: Onde está o decorador que transforma uma função Python em uma ferramenta para agentes?
  expected_files: [libs/core/langchain_core/tools/convert.py]
  keywords: [tool]
```

```powershell
python evaluate.py -r langchain            # só recuperação, rápido
python evaluate.py -r aws-quiz --answers   # também gera e confere respostas com o LLM local
```

Os relatórios completos ficam em `eval/results/` (Markdown e JSON).

## 1. Recuperação: busca vetorial contra reranking

Métricas calculadas sobre os blocos, na ordem em que iriam para o LLM. `hit@k` indica se o top-k tem algum bloco de um arquivo esperado, e `MRR` é a média de 1 dividido pela posição do primeiro bloco correto.

**langchain** (18 perguntas, 2.347 blocos)

| Métrica | Vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0,39 | 0,61 |
| hit@3 | 0,56 | 0,83 |
| hit@5 | 0,72 | 0,89 |
| MRR | 0,50 | 0,71 |

**aws-quiz** (12 perguntas, 40 blocos)

| Métrica | Vetorial | Vetorial + reranking |
|---|---|---|
| hit@1 | 0,08 | 0,33 |
| hit@3 | 0,25 | 0,50 |
| hit@5 | 0,33 | 0,75 |
| MRR | 0,21 | 0,48 |

O reranking subiu todas as métricas nos dois repositórios, e nenhuma pergunta piorou. Exemplos: `lc12` (interface de embeddings) foi da posição 7 para a 1, e `aq11` (testes do backend) saiu de fora do top 10 e foi para a posição 1.

## 2. Respostas do LLM local

Com `prism-ml/bonsai-27b`, k = 6 e reranking ligado, a conferência automática verifica se a resposta cita o arquivo esperado e se menciona as palavras-chave.

| Repositório | Citam o arquivo esperado | Citam o arquivo e todas as palavras-chave | Tempo médio |
|---|---|---|---|
| langchain | 14 de 18 | 11 de 18 | 49 s |
| aws-quiz | 8 de 12 | 5 de 12 | 66 s |

## O que os números mostram

- A recuperação é o gargalo. Quando o arquivo certo está no top 6, o modelo quase sempre o cita; quando não está, ele não consegue acertar. Foi o caso de `lc04`, `lc14`, `aq01` e `aq03`, em que o arquivo esperado ficou fora do top 10 mesmo com reranking.
- Perguntas pelo nome exato de uma classe ou função funcionam melhor do que descrições vagas.
- O aws-quiz tem poucos blocos e muita mistura de linguagens, e é onde a busca vetorial pura mais erra.

## Limites da avaliação

- Poucas perguntas por repositório. Os números indicam tendência, não precisão estatística.
- A conferência de respostas é textual (contém o caminho ou o nome do arquivo e as palavras-chave). Ela pode dar falso negativo quando o modelo escreve o termo de outra forma, e não avalia a qualidade da redação.
- O conjunto foi escrito depois do primeiro contato com os repositórios. Para uma comparação justa entre configurações, mantenha as perguntas fixas e mude uma coisa de cada vez (tamanho do bloco, `fetch_k`, modelo de embeddings ou de reranking).

## 3. No Docker, com modelos pequenos

A mesma avaliação rodou dentro da stack [Docker](Docker), com `nomic-embed-text` nos embeddings e `qwen2.5-coder:3b` nas respostas (`python evaluate.py -r langchain --answers --tag=-docker`).

**langchain**

| Métrica | Só vetorial | Cross-encoder | BM25 |
|---|---|---|---|
| hit@1 | 0,44 | 0,39 | 0,50 |
| hit@5 | 0,67 | 0,78 | 0,67 |
| MRR | 0,56 | 0,55 | 0,60 |

**aws-quiz**

| Métrica | Só vetorial | Cross-encoder | BM25 |
|---|---|---|---|
| hit@1 | 0,42 | 0,33 | 0,33 |
| hit@5 | 0,67 | 0,75 | 0,50 |
| MRR | 0,49 | 0,48 | 0,44 |

Leituras honestas dos números:

- Os embeddings `nomic-embed-text` já recuperam melhor que o `all-MiniLM-L6-v2` (no aws-quiz o hit@1 vai de 0,08 para 0,42), então sobra menos espaço para o reranking ganhar.
- O cross-encoder é o único que melhora o top 5 nos dois repositórios, que é o que importa quando se envia 6 blocos ao modelo. Por isso continua como padrão. Ele pode piorar a posição 1, como em `lc15` e `lc18`.
- O BM25 ajuda no MRR do langchain, onde as perguntas citam nomes de símbolos, mas piora no aws-quiz.
- As respostas do `qwen2.5-coder:3b` citaram o arquivo esperado em 11 de 18 (langchain) e 7 de 12 (aws-quiz), com tempo médio de 18 s e 43 s. A checagem de palavras-chave foi baixa (3 de 18 e 3 de 12), porque o modelo pequeno parafraseia mais do que o LM Studio com o 27B. Modelo menor significa resposta mais rápida e menos precisa; troque `LLM_MODEL` se houver RAM.

Os relatórios completos estão em `eval/results/*-docker.md` e `*-docker-bm25.md`.

## Próximas melhorias sugeridas

Busca híbrida (BM25 mais vetorial) para casar nomes exatos de símbolos, embeddings específicos para código e blocos por função em vez de por tamanho.
