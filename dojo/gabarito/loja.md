# Gabarito do dojo "loja" (spoiler)

Só abra depois de tentar achar os bugs sozinho, com ou sem o agente.

## Como os bugs aparecem

```bash
cd dojo/loja
python -m unittest discover -s tests -v
```

Quatro testes falham, e eles vêm de **três bugs**.

## Bug 1: o subtotal ignora a quantidade

- Arquivo: `loja/carrinho.py`, linha 28.
- Código: `sum(item.preco for item in self.itens)`.
- Correção: `sum(item.preco * item.quantidade for item in self.itens)`.
- Sintoma: 3 canetas de R$ 5,00 dão subtotal de R$ 5,00 em vez de R$ 15,00. O teste `test_subtotal_considera_a_quantidade` falha.
- Por que é traiçoeiro: o `Item` tem o campo `quantidade` e a função `adicionar` até valida a quantidade, então a leitura rápida passa a impressão de que ela é usada.

## Bug 2: o desconto percentual divide por 10 em vez de 100

- Arquivo: `loja/cupons.py`, linha 14.
- Código: `valor - valor * percentual / 10`.
- Correção: `valor - valor * percentual / 100`.
- Sintoma: o cupom de 10% zera a compra (R$ 100,00 viram R$ 0,00) e o de 20% deixa o valor negativo (R$ -100,00). Falham `test_cupom_de_10_por_cento` e `test_cupom_de_20_por_cento`.
- Por que é traiçoeiro: o comentário no dicionário `CUPONS` diz "10% de desconto", e o texto parece certo. O erro está na conta.

## Bug 3: o frete grátis não vale "a partir de" R$ 200

- Arquivo: `loja/frete.py`, linha 8.
- Código: `valor_compra > FRETE_GRATIS_A_PARTIR_DE`.
- Correção: `valor_compra >= FRETE_GRATIS_A_PARTIR_DE`.
- Sintoma: uma compra de exatamente R$ 200,00 paga R$ 15,00 de frete. Falha `test_frete_gratis_a_partir_de_200`.
- Por que é traiçoeiro: é um erro de limite (maior contra maior ou igual). A constante e o comentário dizem "a partir de", e o `>` contradiz os dois.

## Conferência

Depois das três correções, `python -m unittest discover -s tests` deve mostrar `OK` nos 9 testes. O gabarito foi validado assim antes de entrar no repositório.

## Perguntas para fazer ao agente e o que esperar

| Pergunta | Arquivo esperado | Observação |
|---|---|---|
| A partir de qual valor o frete é grátis e como isso é verificado? | `loja/frete.py` | O agente deve citar R$ 200 e o operador `>`. Um bom leitor percebe a contradição com "a partir de". |
| Como o desconto de um cupom é calculado? | `loja/cupons.py` | Teste se o agente nota a divisão por 10 ou se apenas repete o comentário do dicionário. |
| O que o subtotal do carrinho soma? | `loja/carrinho.py` | Teste se ele afirma que a quantidade é considerada sem conferir a linha 28. |
| Como o pagamento com cartão é processado? | nenhum | Não existe no código. A resposta correta é dizer que não há essa informação. |

Na recuperação desta última, as notas ficam bem abaixo das outras perguntas (similaridade de 0,21 a 0,26 contra 0,47 na pergunta do frete, e reranker perto de -11 contra +3,4). Mesmo assim o agente devolve blocos, porque a busca vetorial sempre devolve os mais próximos, mesmo quando nenhum responde.
