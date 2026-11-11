
from django.contrib import admin
from .models import Produto, Venda, ItemVenda


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "categoria",
        "preco",
        "quantidade",
        "estoque_minimo",
        "estoque_baixo",
    )
    search_fields = ("nome", "categoria")
    list_filter = ("categoria",)
    ordering = ("nome",)


class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra = 1


@admin.register(Venda)
class VendaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "data",
        "forma_pagamento",
        "valor_total",
    )
    list_filter = ("forma_pagamento", "data")
    inlines = [ItemVendaInline]


@admin.register(ItemVenda)
class ItemVendaAdmin(admin.ModelAdmin):
    list_display = (
        "venda",
        "produto",
        "quantidade",
        "preco_unitario",
    )
    search_fields = ("produto__nome",)
