# Usar com outro repositório

O agente não tem nada fixo sobre o LangChain. Tudo vem do arquivo `repos.yaml`. Para adicionar um projeto, copie um bloco e ajuste:

```yaml
repos:
  aws-quiz:
    description: Quiz da nuvem na AWS (Lambda, front-end e infraestrutura)
    url: https://github.com/edermendes2016/aws-sandbox-quiz-da-nuvem.git
    path: repos/aws-sandbox-quiz-da-nuvem
    scope: .
    include: ["**/*.py", "**/*.js", "**/*.html", "**/*.css", "**/*.sh", "**/*.yaml", "**/*.md"]
```

| Campo | Para que serve |
|---|---|
| `url` | De onde clonar |
| `path` | Pasta local do clone |
| `scope` | Subpasta que será indexada (`.` indexa tudo) |
| `include` | Padrões de arquivo a indexar |
| `exclude` | Padrões a ignorar, somados aos de `defaults` |
| `collection` | Nome da coleção no ChromaDB (padrão: o nome do repositório) |
| `chunk_size`, `chunk_overlap` | Tamanho dos blocos, se o padrão não servir |

Depois, três comandos:

```powershell
python agent_local.py clone -r meu-repo
python agent_local.py index -r meu-repo
python agent_local.py ask "Como funciona o fluxo de login?" -r meu-repo
```

Cada repositório tem a sua coleção, então as buscas nunca misturam projetos. Na [interface Streamlit](Interface-Streamlit) o repositório é escolhido num seletor.

## Exemplo real: aws-quiz

Projeto misto com Python (Lambda), JavaScript (front-end), HTML, YAML (CloudFormation) e shell. Foram 12 arquivos e 40 blocos. Cada extensão usa o splitter da sua linguagem, o que mantém funções e blocos de configuração inteiros sempre que possível.
