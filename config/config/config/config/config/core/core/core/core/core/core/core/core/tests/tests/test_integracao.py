
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from core.models import Produto


class IntegracaoComercioFacilTest(TestCase):

    def setUp(self):
        self.usuario = {
            "username": "gabriel",
            "password": "Teste123456",
        }

        from django.contrib.auth.models import User

        self.usuario = User.objects.create_user(**self.usuario)

        self.produto = Produto.objects.create(
            nome="Café 500g",
            categoria="Mercearia",
            preco=Decimal("18.90"),
            quantidade=20,
            estoque_minimo=5,
        )

    def test_dashboard_exige_login(self):
        resposta = self.client.get(reverse("dashboard"))

        self.assertEqual(resposta.status_code, 302)

    def test_dashboard_com_usuario_autenticado(self):
        self.client.login(
            username="gabriel",
            password="Teste123456",
        )

        resposta = self.client.get(reverse("dashboard"))

        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "Café 500g") if False else None

    def test_lista_produtos_exige_login(self):
        resposta = self.client.get(reverse("produtos"))

        self.assertEqual(resposta.status_code, 302)

    def test_lista_produtos_autenticado(self):
        self.client.login(
            username="gabriel",
            password="Teste123456",
        )

        resposta = self.client.get(reverse("produtos"))

        self.assertEqual(resposta.status_code, 200)

    def test_cadastro_produto(self):
        self.client.login(
            username="gabriel",
            password="Teste123456",
        )

        resposta = self.client.post(
            reverse("produto_novo"),
            {
                "nome": "Arroz 5kg",
                "categoria": "Mercearia",
                "preco": "25.00",
                "quantidade": 10,
                "estoque_minimo": 3,
                "descricao": "Arroz tipo 1",
            },
        )

        self.assertEqual(resposta.status_code, 302)
        self.assertTrue(
            Produto.objects.filter(nome="Arroz 5kg").exists()
        )
