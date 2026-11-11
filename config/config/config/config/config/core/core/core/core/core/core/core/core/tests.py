
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Produto, Venda, ItemVenda


class ProdutoTestCase(TestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Café 500g",
            categoria="Mercearia",
            preco=Decimal("18.90"),
            quantidade=20,
            estoque_minimo=5,
        )

    def test_cadastro_produto(self):
        self.assertEqual(self.produto.nome, "Café 500g")
        self.assertEqual(self.produto.quantidade, 20)

    def test_identifica_estoque_baixo(self):
        self.produto.quantidade = 3
        self.produto.save()

        self.assertTrue(self.produto.estoque_baixo)

    def test_estoque_normal(self):
        self.assertFalse(self.produto.estoque_baixo)


class VendaTestCase(TestCase):

    def setUp(self):
        self.produto = Produto.objects.create(
            nome="Arroz 5kg",
            categoria="Mercearia",
            preco=Decimal("25.00"),
            quantidade=10,
        )

    def test_registro_de_venda(self):
        venda = Venda.objects.create(
            forma_pagamento="pix",
            valor_total=Decimal("50.00"),
        )

        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=2,
            preco_unitario=self.produto.preco,
        )

        self.assertEqual(venda.valor_total, Decimal("50.00"))
        self.assertEqual(venda.itens.count(), 1)

    def test_subtotal_do_item(self):
        venda = Venda.objects.create(
            forma_pagamento="dinheiro",
            valor_total=Decimal("25.00"),
        )

        item = ItemVenda.objects.create(
            venda=venda,
            produto=self.produto,
            quantidade=1,
            preco_unitario=self.produto.preco,
        )

        self.assertEqual(item.subtotal, Decimal("25.00"))
