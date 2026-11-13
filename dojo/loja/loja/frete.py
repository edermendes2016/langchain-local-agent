"""Cálculo de frete."""

FRETE_FIXO = 15.0
FRETE_GRATIS_A_PARTIR_DE = 200.0  # frete grátis a partir de R$ 200,00


def calcular_frete(valor_compra: float) -> float:
    if valor_compra > FRETE_GRATIS_A_PARTIR_DE:
        return 0.0
    return FRETE_FIXO
