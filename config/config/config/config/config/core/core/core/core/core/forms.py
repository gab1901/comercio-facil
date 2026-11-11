
from django import forms
from .models import Produto, Venda, ItemVenda


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            "nome",
            "categoria",
            "preco",
            "quantidade",
            "estoque_minimo",
            "descricao",
        ]
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome do produto",
            }),
            "categoria": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Categoria",
            }),
            "preco": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
            }),
            "estoque_minimo": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
            }),
            "descricao": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descrição do produto",
            }),
        }


class VendaForm(forms.ModelForm):
    class Meta:
        model = Venda
        fields = ["forma_pagamento"]
        widgets = {
            "forma_pagamento": forms.Select(attrs={
                "class": "form-select",
            }),
        }


class ItemVendaForm(forms.ModelForm):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade"]
        widgets = {
            "produto": forms.Select(attrs={
                "class": "form-select",
            }),
            "quantidade": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "1",
            }),
        }
