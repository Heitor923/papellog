from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Cliente, Produto, Usuario
from core.service import VendaService


class VendaServiceTest(TestCase):

    def setUp(self):
        self.service = VendaService()
        self.usuario = Usuario.objects.create_user(
            username='teste',
            password='senha123',
            nome='Usuário Teste',
        )
        self.cliente = Cliente.objects.create(
            cpf='12345678901',
            nome='Cliente Teste',
            email='cliente@teste.com',
        )
        self.produto = Produto.objects.create(
            nome='Caneta',
            descricao='Caneta esferográfica azul',
            sku='CAN001',
            preco=Decimal('5.00'),
            estoqueAtual=10,
            estoqueMinimo=2,
        )

    def _dados_venda(self, itens=None):
        return {
            'cliente_id': self.cliente.id,
            'usuario_id': self.usuario.id,
            'itens': itens if itens is not None else [
                {'produto_id': self.produto.id, 'quantidade': 2}
            ],
        }

    def test_venda_sem_itens_levanta_erro(self):
        with self.assertRaises(ValidationError):
            self.service.criar(self._dados_venda(itens=[]))

    def test_calculo_total_automatico(self):
        venda = self.service.criar(self._dados_venda())
        self.assertEqual(venda.total, Decimal('10.00'))  # 5.00 * 2

    def test_calculo_total_multiplos_itens(self):
        produto2 = Produto.objects.create(
            nome='Lápis', descricao='Lápis HB', sku='LAP001',
            preco=Decimal('2.00'), estoqueAtual=20, estoqueMinimo=1,
        )
        venda = self.service.criar(self._dados_venda(itens=[
            {'produto_id': self.produto.id, 'quantidade': 3},
            {'produto_id': produto2.id, 'quantidade': 4},
        ]))
        esperado = Decimal('5.00') * 3 + Decimal('2.00') * 4  # 15 + 8 = 23
        self.assertEqual(venda.total, esperado)

    def test_estoque_insuficiente_bloqueia_finalizacao(self):
        venda = self.service.criar(self._dados_venda(itens=[
            {'produto_id': self.produto.id, 'quantidade': 20}  # estoque=10
        ]))
        with self.assertRaises(ValidationError):
            self.service.finalizar(venda.id)

    def test_estoque_atualizado_ao_finalizar(self):
        venda = self.service.criar(self._dados_venda())  # quantidade=2
        self.service.finalizar(venda.id)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoqueAtual, 8)  # 10 - 2

    def test_finalizar_venda_ja_finalizada_levanta_erro(self):
        venda = self.service.criar(self._dados_venda())
        self.service.finalizar(venda.id)
        with self.assertRaises(ValidationError):
            self.service.finalizar(venda.id)
