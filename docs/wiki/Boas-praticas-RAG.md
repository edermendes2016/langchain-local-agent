# Boas práticas de RAG aplicadas

Cada decisão abaixo existe por um motivo concreto de qualidade ou de custo.

## Indexação

- **Splitter por linguagem.** `RecursiveCharacterTextSplitter.from_language` corta em fronteiras de `class` e `def` (ou `function`, tags HTML, títulos Markdown), em vez de cortar no meio de uma função.
- **Sobreposição de 200 caracteres** entre blocos de 1.500, para não perder contexto na fronteira.
- **Cabeçalho contextual.** Cada bloco começa com `# arquivo: caminho/do/arquivo`. O caminho entra no embedding e ajuda perguntas do tipo "onde fica X".
- **Metadados ricos.** Arquivo, linha inicial e final, extensão e repositório. É isso que permite citar a fonte exata e filtrar depois.
- **Ids determinísticos.** Hash de repositório, arquivo e posição. A mesma entrada gera o mesmo id.
- **Uma coleção por repositório**, evitando mistura de contextos.
- **Embeddings locais** (`all-MiniLM-L6-v2`) com distância de cosseno: sem custo, sem envio de código para fora.

## Recuperação

- **Duas etapas**: busca vetorial ampla e depois [reranking](Reranking) com cross-encoder para escolher os melhores blocos.
- **Top-k pequeno no prompt.** Contexto enxuto reduz ruído e latência do modelo local.

## Geração

- **Grounding.** O prompt de sistema obriga o modelo a usar só o contexto, citar `[n] arquivo:linha` e dizer quando o contexto não basta. `temperature=0` para respostas reproduzíveis.
- **Endpoint compatível com OpenAI.** O mesmo `ChatOpenAI` serve para LM Studio, Ollama ou um provedor em nuvem, trocando `base_url` e `model`.

## Qualidade

- **[Avaliação](Avaliacao)** com perguntas de referência e arquivos esperados, medindo acerto no top-k e MRR antes e depois de cada mudança.
- **Configuração fora do código** (`repos.yaml` e variáveis de ambiente): trocar de repositório, modelo ou tamanho de bloco não exige editar Python.
