# Ambiente Python

No PowerShell:

```powershell
git clone https://github.com/edermendes2016/langchain-local-agent.git
cd langchain-local-agent

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# baixa os repositórios que serão analisados (clone raso)
python agent_local.py clone -r langchain
python agent_local.py clone -r aws-quiz
```

O `requirements.txt` instala o PyTorch na versão CPU, o ChromaDB, o LangChain (`langchain`, `langchain-community`, `langchain-openai`, `langchain-text-splitters`), `sentence-transformers`, `tiktoken`, `streamlit` e `pyyaml`.

Se o PowerShell bloquear a ativação do ambiente, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`. Se a rede cair durante o download, repita com mais tentativas:

```powershell
pip install --retries 10 --timeout 60 -r requirements.txt
```

![Ambiente ativado e pacotes instalados](images/02-ambiente.png)

Próximo: [Indexação](Indexacao)
