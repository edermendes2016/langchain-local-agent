# LM Studio

1. Abra o LM Studio e carregue o modelo `prism-ml/bonsai-27b`.
2. Na aba **Model Server**, inicie o servidor local. A porta padrão é `1234`.
3. Confirme que ele responde. No PowerShell:

```powershell
(Invoke-RestMethod http://localhost:1234/v1/models).data | Select-Object id
```

O `prism-ml/bonsai-27b` precisa aparecer na lista.

![API do LM Studio listando os modelos](images/01-lmstudio-api.png)

O endereço `http://localhost:1234/v1` segue o formato da API da OpenAI. Por isso o projeto usa `ChatOpenAI` com `base_url` apontando para ele e `api_key="lm-studio"` (o valor é ignorado). Trocar de modelo exige mudar apenas `llm_model` no `repos.yaml` ou a variável `LLM_MODEL`.

Próximo: [Ambiente Python](Ambiente-Python)
