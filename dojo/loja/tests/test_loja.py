import unittest

from loja import Carrinho
from loja.cupons import aplicar_cupom
from loja.frete import calcular_frete


class TestCarrinho(unittest.TestCase):
    def test_rejeita_quantidade_invalida(self):
        with self.assertRaises(ValueError):
            Carrinho().adicionar("Caneta", 3.0, 0)

    def test_subtotal_de_um_item_unico(self):
        c = Carrinho()
        c.adicionar("Caderno", 20.0)
        self.assertEqual(c.subtotal(), 20.0)

    def test_subtotal_considera_a_quantidade(self):
        c = Carrinho()
        c.adicionar("Caneta", 5.0, quantidade=3)
        self.assertEqual(c.subtotal(), 15.0)


class TestCupons(unittest.TestCase):
    def test_codigo_desconhecido_nao_altera_o_valor(self):
        self.assertEqual(aplicar_cupom(100.0, "INEXISTENTE"), 100.0)

    def test_cupom_de_10_por_cento(self):
        self.assertEqual(aplicar_cupom(100.0, "BEMVINDO10"), 90.0)

    def test_cupom_de_20_por_cento(self):
        self.assertEqual(aplicar_cupom(100.0, "PROMO20"), 80.0)


class TestFrete(unittest.TestCase):
    def test_frete_fixo_em_compra_pequena(self):
        self.assertEqual(calcular_frete(50.0), 15.0)

    def test_frete_gratis_acima_de_200(self):
        self.assertEqual(calcular_frete(250.0), 0.0)

    def test_frete_gratis_a_partir_de_200(self):
        self.assertEqual(calcular_frete(200.0), 0.0)


if __name__ == "__main__":
    unittest.main()
