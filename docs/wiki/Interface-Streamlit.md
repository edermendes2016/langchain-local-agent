# Interface Streamlit

```powershell
streamlit run app.py
```

O navegador abre em `http://localhost:8501`.

![Interface Streamlit com resposta, fontes e trechos](images/05-streamlit.png)

## O que a interface mostra

- **Barra lateral**: seletor de repositório (lido do `repos.yaml`), controle de `k`, chave para gerar ou não a resposta com o LLM, quantidade de blocos indexados e status do LM Studio (online ou offline).
- **Resposta**: texto do `prism-ml/bonsai-27b` com as fontes citadas e o tempo gasto.
- **Fontes recuperadas**: tabela com arquivo, linha e similaridade, na ordem em que foram enviadas ao modelo.
- **Trechos**: um bloco expansível por fonte, com o código real e realce de sintaxe.
- **Histórico**: cada pergunta fica na página, da mais recente para a mais antiga, para comparar resultados com valores de `k` diferentes.

## Dicas de uso

- Desligue **Gerar resposta com o LLM local** para explorar só a recuperação. A busca é instantânea e mostra se os arquivos certos aparecem antes de gastar um minuto de inferência.
- Se a coleção estiver vazia, a página avisa qual comando de indexação rodar.
- Se o servidor do LM Studio estiver desligado, a interface continua mostrando as fontes e avisa que não há resposta.
