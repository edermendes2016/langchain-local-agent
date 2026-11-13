"""Carrinho de compras simples."""

from dataclasses import dataclass, field

from .cupons import aplicar_cupom
from .frete import calcular_frete


@dataclass
class Item:
    nome: str
    preco: float
    quantidade: int = 1


@dataclass
class Carrinho:
    itens: list[Item] = field(default_factory=list)
    cupom: str | None = None

    def adicionar(self, nome: str, preco: float, quantidade: int = 1) -> None:
        if preco <= 0 or quantidade <= 0:
            raise ValueError("preco e quantidade devem ser positivos")
        self.itens.append(Item(nome, preco, quantidade))

    def subtotal(self) -> float:
        """Soma dos itens, antes de cupom e frete."""
        return round(sum(item.preco for item in self.itens), 2)

    def total(self) -> float:
        """Valor final: subtotal com cupom aplicado, mais o frete."""
        com_desconto = aplicar_cupom(self.subtotal(), self.cupom)
        return round(com_desconto + calcular_frete(com_desconto), 2)
