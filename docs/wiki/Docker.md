# Rodar tudo com Docker

O caminho de menor esforço: um comando sobe o LLM, o banco vetorial e o agente, sem chaves de API.

```bash
git clone https://github.com/edermendes2016/langchain-local-agent.git
cd langchain-local-agent
docker compose up --build
```

Abra http://localhost:8501 quando o log mostrar "Pronto!".

## O que sobe

| Serviço | Imagem | Papel |
|---|---|---|
| `ollama` | build local sobre `ollama/ollama` | Serve o LLM `qwen2.5-coder:3b` e os embeddings `nomic-embed-text`. Baixa os dois modelos sozinho no primeiro start. |
| `chroma` | `chromadb/chroma:1.5.9` | Banco vetorial com persistência em volume. |
| `agent` | build local (Python 3.12) | Espera os dois serviços, clona o repositório, indexa se o Chroma estiver vazio e abre a interface Streamlit. |

## Ordem de inicialização

1. `ollama` e `chroma` sobem em paralelo. O healthcheck do Ollama só fica verde quando **os dois modelos** já estão baixados.
2. O `agent` só inicia depois que ambos estão saudáveis (`depends_on` com `service_healthy`).
3. O comando `agent_local.py bootstrap` clona o repositório (clone raso), e indexa apenas se a coleção estiver vazia. Em reinícios ele pula essa etapa.
4. A interface Streamlit sobe e o healthcheck do agente aponta para ela.

## Volumes

| Volume | Conteúdo |
|---|---|
| `ollama-data` | Modelos baixados |
| `chroma-data` | Índice vetorial |
| `repos-data` | Repositórios clonados |

`docker compose down` mantém os volumes. `docker compose down -v` apaga tudo e força o download e a indexação de novo.

## Configuração

Variáveis em um arquivo `.env` (modelo em `.env.example`):

| Variável | Padrão | Efeito |
|---|---|---|
| `LLM_MODEL` | `qwen2.5-coder:3b` | Qualquer modelo do Ollama. Modelos maiores respondem melhor e exigem mais RAM. |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Modelo de embeddings. Ao trocar, rode `docker compose down -v` para reindexar. |
| `RERANKER` | `cross-encoder` | `cross-encoder` (mais preciso), `bm25` (mais leve) ou `none`. |
| `BOOTSTRAP_REPOS` | `langchain` | Repositórios indexados no primeiro start, separados por vírgula. |
| `APP_PORT` | `8501` | Porta da interface. |

## Usar outro repositório

Adicione um bloco em `docker/repos.docker.yaml`, como o `aws-quiz` que já está lá, e rode:

```bash
docker compose exec agent python agent_local.py clone -r meu-repo
docker compose exec agent python agent_local.py index -r meu-repo
```

Ele aparece no seletor da interface.

## Requisitos e tempos

- Docker Desktop com Compose v2, 8 GB de RAM para o Docker, cerca de 15 GB de disco (a imagem do Ollama é grande) e internet na primeira execução.
- GPU NVIDIA é opcional: `docker compose -f docker-compose.yml -f docker-compose.gpu.yml up`.
- Medido em um PC com 32 CPUs (sem GPU): indexação de 2.347 blocos em 512 s na primeira vez; resposta do `qwen2.5-coder:3b` em cerca de 20 s; reinício do agente em 9 s, sem reindexar. Os resultados da [avaliação](Avaliacao) neste ambiente também estão documentados.

## Problemas comuns

| Sintoma | Solução |
|---|---|
| Demora muito no primeiro start | É o download dos modelos (cerca de 2 GB). Acompanhe com `docker compose logs -f ollama`. |
| Porta 8501 ocupada | Defina `APP_PORT=8502` no `.env`. |
| Respostas fracas | Troque `LLM_MODEL` por um modelo maior, por exemplo `qwen2.5-coder:7b`, se houver RAM. |
| Quer começar do zero | `docker compose down -v` |
