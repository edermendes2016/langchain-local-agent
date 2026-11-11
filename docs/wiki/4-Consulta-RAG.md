# 4. Enviar um prompt e receber a resposta

Com o servidor do LM Studio ligado e o código indexado:

```powershell
python agent_local.py ask "Em qual arquivo fica a classe base BaseChatModel e o que ela define?" -k 6
```

O script faz três coisas, nesta ordem:

1. `collection.query()` busca os `k` blocos mais parecidos com a pergunta e lista cada um com arquivo, linha e similaridade.
2. Esses blocos viram o contexto de um prompt de sistema que obriga o modelo a responder só com o que está nos trechos e a citar as fontes.
3. O prompt é enviado ao `prism-ml/bonsai-27b` pelo `ChatOpenAI`, e a resposta aparece no terminal.

![Consulta e resposta do modelo local](images/04-consulta.png)

## Como ler a saída

- **DOCUMENTOS RECUPERADOS**: confira se os arquivos fazem sentido para a pergunta. Se não fazem, a resposta também não vai fazer.
- **RESPOSTA DO AGENTE**: o modelo cita `arquivo:linha`. Abra o trecho para conferir.
- Quando o contexto não basta, o modelo avisa em vez de inventar. Aumente `-k` (por exemplo `-k 10`) ou reformule citando nomes de classes e métodos.

Perguntas que funcionam bem: nomes concretos (`BaseChatModel`, `invoke`, `generate_prompt`). Perguntas vagas recuperam blocos genéricos.

Respostas de modelos de 27B em CPU/GPU doméstica levam de 30 s a mais de 1 min.
