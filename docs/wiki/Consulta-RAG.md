# Consulta RAG

Com o servidor do LM Studio ligado e o repositório indexado:

```powershell
python agent_local.py ask "Em qual arquivo fica a classe BaseChatModel e o que ela define?" -r langchain -k 6
```

O script executa, nesta ordem:

1. `collection.query()` busca os `k` blocos mais parecidos com a pergunta e lista arquivo, linha e similaridade.
2. Os blocos viram o contexto de um prompt que obriga o modelo a responder só com o que está nos trechos e a citar `[n] arquivo:linha`.
3. O prompt vai para o `prism-ml/bonsai-27b` pelo `ChatOpenAI`, e a resposta aparece no terminal.

![Consulta e resposta do modelo local](images/04-consulta.png)

## Como ler a saída

- **Documentos recuperados**: confira se os arquivos fazem sentido para a pergunta. Se não fazem, a resposta também não fará.
- **Resposta do agente**: cada afirmação cita a fonte. Abra o trecho para conferir.
- Quando o contexto não basta, o modelo avisa em vez de inventar. Reformule citando nomes de classes, funções ou arquivos, ou use o [Reranking](Reranking).

Modelos de 27B levam de 30 s a mais de 1 min por resposta.

Próximo: [Interface Streamlit](Interface-Streamlit)
