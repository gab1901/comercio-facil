
from django.db import models
from django.core.validators import MinValueValidator


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantidade = models.PositiveIntegerField(default=0)
    descricao = models.TextField(blank=True)
    estoque_minimo = models.PositiveIntegerField(default=5)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return self.nome

    @property
    def estoque_baixo(self):
        return self.quantidade <= self.estoque_minimo


class Venda(models.Model):
    FORMAS_PAGAMENTO = [
        ("dinheiro", "Dinheiro"),
        ("pix", "PIX"),
        ("credito", "Cartão de crédito"),
        ("debito", "Cartão de débito"),
    ]

    data = models.DateTimeField(auto_now_add=True)
    forma_pagamento = models.CharField(
        max_length=20,
        choices=FORMAS_PAGAMENTO
    )
    valor_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["-data"]
        verbose_name = "Venda"
        verbose_name_plural = "Vendas"

    def __str__(self):
        return f"Venda #{self.id}"


class ItemVenda(models.Model):
    venda = models.ForeignKey(
        Venda,
        on_delete=models.CASCADE,
        related_name="itens"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )
    quantidade = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    preco_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    class Meta:
        verbose_name = "Item da venda"
        verbose_name_plural = "Itens da venda"

    def __str__(self):
        return f"{self.produto.nome} - {self.quantidade} unidade(s)"

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
