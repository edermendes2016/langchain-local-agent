"""Cupons de desconto percentual."""

CUPONS = {
    "BEMVINDO10": 10,  # 10% de desconto
    "PROMO20": 20,  # 20% de desconto
}


def aplicar_cupom(valor: float, codigo: str | None) -> float:
    """Aplica o desconto do cupom. Código desconhecido ou vazio não altera o valor."""
    if not codigo or codigo not in CUPONS:
        return valor
    percentual = CUPONS[codigo]
    return round(valor - valor * percentual / 10, 2)
