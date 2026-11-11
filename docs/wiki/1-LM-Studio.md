# 1. Subir o LLM local no LM Studio

1. Abra o LM Studio e carregue o modelo `prism-ml/bonsai-27b` (seletor no topo da aba **Chat**).
2. Vá na aba **Model Server** (menu lateral) e inicie o servidor local. A porta padrão é `1234`.
3. Confira que o servidor responde. No PowerShell:

```powershell
(Invoke-RestMethod http://localhost:1234/v1/models).data | Select-Object id
```

O modelo `prism-ml/bonsai-27b` precisa aparecer na lista.

![API do LM Studio listando os modelos](images/01-lmstudio-api.png)

O endereço `http://localhost:1234/v1` é compatível com a API da OpenAI. Por isso o projeto usa `ChatOpenAI` com `base_url` apontando para ele e `api_key="lm-studio"` (o valor é ignorado).

Próximo passo: [Preparar o ambiente Python](2-Ambiente-Python)
