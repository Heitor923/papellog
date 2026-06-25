from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from core.models import Cliente, ItemVenda, Produto, StatusVenda, Usuario, Venda


class IAViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.usuario = Usuario.objects.create_user(
            username='teste_ia',
            password='senha123',
            nome='Usuário Teste IA',
        )
        refresh = RefreshToken.for_user(self.usuario)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.cliente = Cliente.objects.create(
            cpf='11122233344',
            nome='Cliente IA Test',
            email='ia@test.com',
        )
        self.produto_vendido = Produto.objects.create(
            nome='Caneta Azul',
            descricao='Caneta esferográfica azul',
            sku='CAN_IA',
            preco=Decimal('5.00'),
            estoqueAtual=100,
            estoqueMinimo=5,
        )
        self.produto_parado = Produto.objects.create(
            nome='Borracha Branca',
            descricao='Borracha escolar',
            sku='BOR_IA',
            preco=Decimal('2.00'),
            estoqueAtual=50,
            estoqueMinimo=3,
        )

        venda = Venda.objects.create(
            cliente=self.cliente,
            usuario=self.usuario,
            total=Decimal('15.00'),
            status=StatusVenda.FINALIZADA,
        )
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto_vendido,
            quantidade=3,
            precoUnitario=Decimal('5.00'),
            subtotal=Decimal('15.00'),
        )

    # --- mais-vendidos ---

    def test_mais_vendidos_retorna_200(self):
        response = self.client.get('/ia/mais-vendidos')
        self.assertEqual(response.status_code, 200)

    def test_mais_vendidos_contem_produto_com_venda(self):
        response = self.client.get('/ia/mais-vendidos')
        nomes = [item['produto_nome'] for item in response.data]
        self.assertIn('Caneta Azul', nomes)

    def test_mais_vendidos_nao_contem_produto_parado(self):
        response = self.client.get('/ia/mais-vendidos')
        nomes = [item['produto_nome'] for item in response.data]
        self.assertNotIn('Borracha Branca', nomes)

    def test_mais_vendidos_ignora_venda_pendente(self):
        venda = Venda.objects.create(
            cliente=self.cliente,
            usuario=self.usuario,
            total=Decimal('2.00'),
        )
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto_parado,
            quantidade=1,
            precoUnitario=Decimal('2.00'),
            subtotal=Decimal('2.00'),
        )
        response = self.client.get('/ia/mais-vendidos')
        nomes = [item['produto_nome'] for item in response.data]
        self.assertNotIn('Borracha Branca', nomes)

    # --- menos-vendidos ---

    def test_menos_vendidos_retorna_200(self):
        response = self.client.get('/ia/menos-vendidos')
        self.assertEqual(response.status_code, 200)

    def test_menos_vendidos_contem_produto_com_venda(self):
        response = self.client.get('/ia/menos-vendidos')
        nomes = [item['produto_nome'] for item in response.data]
        self.assertIn('Caneta Azul', nomes)

    # --- produtos-parados ---

    def test_produtos_parados_retorna_200(self):
        response = self.client.get('/ia/produtos-parados')
        self.assertEqual(response.status_code, 200)

    def test_produtos_parados_contem_produto_sem_venda(self):
        response = self.client.get('/ia/produtos-parados')
        skus = [p['sku'] for p in response.data]
        self.assertIn('BOR_IA', skus)

    def test_produtos_parados_ignora_venda_pendente(self):
        venda = Venda.objects.create(
            cliente=self.cliente,
            usuario=self.usuario,
            total=Decimal('2.00'),
        )
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto_parado,
            quantidade=1,
            precoUnitario=Decimal('2.00'),
            subtotal=Decimal('2.00'),
        )
        response = self.client.get('/ia/produtos-parados')
        skus = [p['sku'] for p in response.data]
        self.assertIn('BOR_IA', skus)

    def test_produtos_parados_nao_contem_produto_vendido(self):
        response = self.client.get('/ia/produtos-parados')
        skus = [p['sku'] for p in response.data]
        self.assertNotIn('CAN_IA', skus)

    # --- autenticação ---

    def test_sem_autenticacao_mais_vendidos_retorna_401(self):
        response = APIClient().get('/ia/mais-vendidos')
        self.assertEqual(response.status_code, 401)

    def test_sem_autenticacao_menos_vendidos_retorna_401(self):
        response = APIClient().get('/ia/menos-vendidos')
        self.assertEqual(response.status_code, 401)

    def test_sem_autenticacao_produtos_parados_retorna_401(self):
        response = APIClient().get('/ia/produtos-parados')
        self.assertEqual(response.status_code, 401)
