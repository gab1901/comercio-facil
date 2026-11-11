
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Produto, Venda, ItemVenda
from .forms import ProdutoForm, VendaForm


@login_required
def dashboard(request):
    hoje = timezone.localdate()

    produtos = Produto.objects.all()
    vendas_hoje = Venda.objects.filter(data__date=hoje)

    total_vendas = vendas_hoje.aggregate(
        total=Sum("valor_total")
    )["total"] or Decimal("0.00")

    produtos_baixo = produtos.filter(
        quantidade__lte=F("estoque_minimo")
    )

    ultimas_vendas = Venda.objects.all()[:5]

    contexto = {
        "total_produtos": produtos.count(),
        "total_vendas": total_vendas,
        "quantidade_vendas": vendas_hoje.count(),
        "produtos_baixo": produtos_baixo,
        "ultimas_vendas": ultimas_vendas,
    }

    return render(request, "core/dashboard.html", contexto)


@login_required
def produtos(request):
    termo = request.GET.get("busca", "").strip()

    lista = Produto.objects.all()

    if termo:
        lista = lista.filter(nome__icontains=termo)

    return render(
        request,
        "core/produtos.html",
        {"produtos": lista, "busca": termo},
    )


@login_required
def produto_novo(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto cadastrado com sucesso!")
            return redirect("produtos")
    else:
        form = ProdutoForm()

    return render(
        request,
        "core/produto_form.html",
        {"form": form, "titulo": "Cadastrar produto"},
    )


@login_required
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado com sucesso!")
            return redirect("produtos")
    else:
        form = ProdutoForm(instance=produto)

    return render(
        request,
        "core/produto_form.html",
        {"form": form, "titulo": "Editar produto"},
    )


@login_required
def produto_excluir(request, pk):
    produto = get_object_or_404(Produto, pk=pk)

    if request.method == "POST":
        produto.delete()
        messages.success(request, "Produto excluído com sucesso!")
        return redirect("produtos")

    return render(
        request,
        "core/produto_form.html",
        {
            "form": None,
            "titulo": "Confirmar exclusão",
            "produto": produto,
            "confirmar_exclusao": True,
        },
    )


@login_required
def vendas(request):
    lista = Venda.objects.prefetch_related("itens__produto").all()

    return render(
        request,
        "core/vendas.html",
        {"vendas": lista},
    )


@login_required
def venda_nova(request):
    if request.method == "POST":
        form = VendaForm(request.POST)
        produto_id = request.POST.get("produto")
        quantidade_texto = request.POST.get("quantidade", "1")

        if form.is_valid():
            try:
                quantidade = int(quantidade_texto)
                if quantidade < 1:
                    raise ValueError
            except (TypeError, ValueError):
                messages.error(request, "Informe uma quantidade válida.")
                return redirect("venda_nova")

            with transaction.atomic():
                produto = get_object_or_404(
                    Produto.objects.select_for_update(),
                    pk=produto_id,
                )

                if produto.quantidade < quantidade:
                    messages.error(
                        request,
                        "Estoque insuficiente para realizar a venda.",
                    )
                    return redirect("venda_nova")

                venda = form.save(commit=False)
                venda.valor_total = produto.preco * quantidade
                venda.save()

                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco,
                )

                produto.quantidade -= quantidade
                produto.save()

            messages.success(request, "Venda registrada com sucesso!")
            return redirect("vendas")
    else:
        form = VendaForm()

    return render(
        request,
        "core/vendas.html",
        {
            "form": form,
            "produtos_disponiveis": Produto.objects.filter(
                quantidade__gt=0
            ),
            "nova_venda": True,
        },
    )


@login_required
def historico(request):
    lista = Venda.objects.prefetch_related("itens__produto").all()

    data = request.GET.get("data", "")
    if data:
        lista = lista.filter(data__date=data)

    return render(
        request,
        "core/historico.html",
        {"vendas": lista, "data_filtro": data},
    )
