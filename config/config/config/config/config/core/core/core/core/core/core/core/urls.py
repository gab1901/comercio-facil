
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),

    path("produtos/", views.produtos, name="produtos"),
    path("produtos/novo/", views.produto_novo, name="produto_novo"),
    path(
        "produtos/<int:pk>/editar/",
        views.produto_editar,
        name="produto_editar",
    ),
    path(
        "produtos/<int:pk>/excluir/",
        views.produto_excluir,
        name="produto_excluir",
    ),

    path("vendas/", views.vendas, name="vendas"),
    path("vendas/nova/", views.venda_nova, name="venda_nova"),

    path("historico/", views.historico, name="historico"),
]
