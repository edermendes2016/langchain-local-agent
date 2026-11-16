# Agente RAG local para repositórios de código

Pergunte sobre o código de qualquer repositório e receba respostas com arquivo e linha. Tudo roda na sua máquina com Docker: LLM e embeddings no Ollama, vetores no ChromaDB, reranking e interface web. **Sem chaves de API e sem passos manuais.**

## Rodar (3 comandos)

```bash
git clone https://github.com/edermendes2016/langchain-local-agent.git
cd langchain-local-agent
docker compose up --build
```

Quando o log mostrar **"Pronto! Abra http://localhost:8501"**, abra o endereço e pergunte. Na primeira vez o Ollama baixa os modelos sozinho (cerca de 2 GB) e o agente indexa o núcleo do LangChain, o que leva uns 10 minutos em CPU. O tempo total da primeira execução depende principalmente da velocidade da internet. Nas próximas vezes sobe em segundos.

**Requisitos:** Docker Desktop com Compose v2, 8 GB de RAM liberados para o Docker, cerca de 15 GB de disco livre e internet apenas na primeira execução. GPU é opcional.

## Documentação

Tudo o mais está na **[wiki](https://github.com/edermendes2016/langchain-local-agent/wiki)**:

- [Arquitetura](https://github.com/edermendes2016/langchain-local-agent/wiki/Arquitetura): como o agente funciona, com o diagrama completo.
- [Rodar tudo com Docker](https://github.com/edermendes2016/langchain-local-agent/wiki/Docker): configuração, modelos, GPU e outros repositórios.
- [Dojo](https://github.com/edermendes2016/langchain-local-agent/wiki/Dojo): treinar o olhar crítico sobre respostas de IA com repositórios com bugs.
- [Uso em empresas](https://github.com/edermendes2016/langchain-local-agent/wiki/Uso-em-empresas): privacidade, custo, limites do modelo e como escalar.
- [Avaliação](https://github.com/edermendes2016/langchain-local-agent/wiki/Avaliacao): resultados com perguntas de referência.

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE). Copyright (c) 2026 Eder Mendes Amaral.
