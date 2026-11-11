# 2. Preparar o ambiente Python

No PowerShell, dentro da pasta onde quer o projeto:

```powershell
git clone https://github.com/edermendes2016/langchain-local-agent.git
cd langchain-local-agent

# código-fonte que será analisado (clone raso, bem mais rápido)
git clone --depth 1 https://github.com/langchain-ai/langchain.git langchain_repo

py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

O `requirements.txt` instala o PyTorch na versão CPU e depois `chromadb`, `langchain`, `langchain-community`, `langchain-openai`, `langchain-text-splitters`, `tiktoken` e `sentence-transformers`.

Se o PowerShell bloquear o script de ativação, rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

Se a rede cair no meio do download, repita com mais tentativas:

```powershell
pip install --retries 10 --timeout 60 -r requirements.txt
```

![Ambiente ativado e pacotes instalados](images/02-ambiente.png)

Próximo passo: [Indexar o código no ChromaDB](3-Indexacao)
