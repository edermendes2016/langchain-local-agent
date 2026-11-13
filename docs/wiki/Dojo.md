# Dojo: treinar o olhar crítico com IA

Um dojo é um lugar para praticar com segurança. A ideia aqui é simples: peça a uma IA para criar repositórios com bugs, indexe esse código no agente, investigue e depois confira com o gabarito. Você treina três coisas ao mesmo tempo: ler código que não é seu, usar RAG como ferramenta de investigação e, principalmente, **desconfiar de respostas de IA**.

Hoje escrever código é a parte fácil. O que separa quem usa IA bem de quem só copia é conferir o que ela diz.

## O ciclo de treino

1. **Gerar.** Peça a uma IA um repositório pequeno com 2 ou 3 bugs plantados e um gabarito separado (o prompt está abaixo).
2. **Indexar.** Coloque o repositório no `repos.yaml` e rode `index`.
3. **Investigar.** Faça perguntas ao agente sobre o comportamento do código.
4. **Duvidar.** Para cada resposta, abra o arquivo e a linha citados e confira.
5. **Corrigir.** Ache o bug, corrija e rode os testes.
6. **Comparar.** Abra o gabarito. Onde você e o agente erraram? Por quê?
7. **Registrar.** Anote as respostas erradas da IA. Elas viram os melhores exercícios.

## Exercício pronto: a loja com 3 bugs

O repositório `dojo/loja` já vem pronto: um carrinho de compras com cupom e frete, 3 bugs e 9 testes (4 deles falham por causa dos bugs). O gabarito fica em `dojo/gabarito/loja.md`, fora da pasta indexada de propósito, para a IA não ler a resposta.

```bash
# 1. veja os testes falhando
cd dojo/loja
python -m unittest discover -s tests -v

# 2. indexe e pergunte
cd ../..
python agent_local.py index -r dojo-loja
python agent_local.py ask "A partir de qual valor o frete é grátis e como isso é verificado?" -r dojo-loja
```

Com Docker, o repositório já está na imagem: `docker compose exec agent python agent_local.py index -r dojo-loja`.

Desafio: ache os 3 bugs sem abrir o gabarito. Depois confira.

## Perguntas de arquitetura com resposta esperada

O arquivo `eval/langchain.yaml` e o `eval/aws-quiz.yaml` têm 30 perguntas, cada uma com os arquivos corretos conferidos no código. Use como prova:

1. Pegue uma pergunta, por exemplo "Onde está o decorador que transforma uma função Python em uma ferramenta para agentes?".
2. Procure a resposta no repositório sozinho e anote o arquivo.
3. Pergunte ao agente e compare com o `expected_files`.
4. Veja a posição em que o arquivo certo apareceu na recuperação. Se não apareceu, o problema é de busca, não do modelo.

Os resultados de cada configuração estão na página de [Avaliação](Avaliacao). Quando você escrever perguntas novas sobre o seu repositório, acrescente ao YAML e rode `evaluate.py` para medir.

## Cenários de falha para treinar

### 1. A pergunta que o código não responde

No `dojo-loja`, pergunte "Como o pagamento com cartão de crédito é processado?". Não existe pagamento nesse código.

O que se mede: a busca devolve blocos mesmo assim, porque sempre devolve os mais próximos. Mas as notas despencam: similaridade de 0,21 a 0,26 (contra 0,47 numa pergunta que tem resposta) e nota do reranker perto de -11 (contra +3,4). Nota baixa em todos os blocos é um sinal de que provavelmente não há resposta.

O que praticar: a resposta certa é "não há essa informação no código". Veja se o modelo diz isso ou se inventa um fluxo de pagamento. Um modelo que responde com confiança sobre algo inexistente é o risco mais caro em uso real.

### 2. Código renomeado sem reindexar

O índice é uma foto do código no momento da indexação. Renomeie `calcular_frete` para `calcular_taxa_entrega` em `dojo/loja/loja/frete.py` e no `carrinho.py`, e pergunte de novo sem reindexar. O agente vai citar o nome antigo e as linhas antigas, com toda a confiança.

O que praticar: confira se o trecho citado ainda existe. Depois rode `python agent_local.py index -r dojo-loja --reset` e compare. A regra prática: depois de mudar o código, reindexe antes de confiar.

### 3. A fonte está certa e a conclusão está errada

Exemplo real, medido neste projeto. Com o modelo `qwen2.5-coder:3b` no Docker, perguntamos onde fica a classe base dos modelos de chat e o que ela exige das subclasses. O agente acertou o arquivo (`chat_models.py`, linha 325) e acertou a classe (`BaseChatModel`), mas afirmou que as subclasses precisam implementar `_generate` e `_call`.

Conferindo o código: `BaseChatModel` exige `_generate` e `_llm_type`. O `_call` é abstrato na classe `SimpleChatModel`, que herda da base (linha 2703 em diante). A resposta parecia correta, tinha fonte, e estava parcialmente errada.

O que praticar: citação não é prova. Abra o trecho e ache cada afirmação nele.

### 4. Resposta sem fonte ou com fonte que não sustenta o que diz

Procure respostas que citam um arquivo, mas cuja afirmação não aparece naquele trecho. No `aws-quiz`, por exemplo, o modelo às vezes responde certo sobre o assunto sem citar o arquivo esperado. A avaliação automática registra isso na coluna "Cita o arquivo".

## Checklist de olhar crítico

- A resposta cita arquivo e linha? Abri e conferi?
- Cada afirmação aparece no trecho, ou o modelo completou com conhecimento geral?
- As notas de similaridade e de reranking estão altas, ou todos os blocos foram fracos?
- O índice está atualizado em relação ao código?
- Existe um teste que prova a afirmação? Se existir, rode.
- A resposta contradiz o comentário, o nome da função ou o teste? Contradição é onde moram os bugs.

## Gerar o seu próprio dojo

Peça a uma IA algo como:

```text
Crie um repositório Python pequeno (3 a 5 arquivos) de um sistema de <tema>,
com testes unittest. Plante exatamente 3 bugs realistas: um de lógica,
um de limite (maior ou maior ou igual) e um de unidade ou conversão.
Faça os testes falharem por causa deles. Não deixe comentários que revelem
os bugs. Entregue o gabarito em um arquivo separado, com arquivo, linha,
sintoma e correção de cada bug.
```

Confira você mesmo que os testes falham e que o gabarito é verdadeiro, rodando as correções numa cópia. Foi assim que o gabarito do `dojo/loja` foi validado. Depois adicione o repositório ao `repos.yaml` (sem `url`, com `path` local) e siga o ciclo.

Temas que rendem bons dojos: fila de atendimento, cálculo de folha, estoque, agendamento, API de pedidos. Para uso em equipe, cada pessoa pode trazer um bug real já resolvido (sem dados sensíveis) para virar exercício.
