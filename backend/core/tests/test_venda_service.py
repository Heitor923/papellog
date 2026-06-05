from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Cliente, Produto, StatusVenda, Usuario
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
            'usuario': self.usuario,
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

    # --- Rastreabilidade da finalização ---

    def test_finalizar_salva_finalizado_por(self):
        venda = self.service.criar(self._dados_venda())
        self.service.finalizar(venda.id, self.usuario)
        venda.refresh_from_db()
        self.assertEqual(venda.finalizado_por, self.usuario)

    def test_finalizar_salva_data_finalizacao(self):
        venda = self.service.criar(self._dados_venda())
        self.service.finalizar(venda.id, self.usuario)
        venda.refresh_from_db()
        self.assertIsNotNone(venda.data_finalizacao)

    def test_finalizar_sem_usuario_nao_levanta_erro(self):
        venda = self.service.criar(self._dados_venda())
        self.service.finalizar(venda.id)  # usuario=None é permitido
        venda.refresh_from_db()
        self.assertEqual(venda.status, StatusVenda.FINALIZADA)
        self.assertIsNone(venda.finalizado_por)

    def test_venda_pendente_ainda_pode_ser_finalizada(self):
        venda = self.service.criar(self._dados_venda())
        self.assertEqual(venda.status, StatusVenda.PENDENTE)
        self.service.finalizar(venda.id, self.usuario)
        venda.refresh_from_db()
        self.assertEqual(venda.status, StatusVenda.FINALIZADA)

    def test_estoque_descontado_corretamente_ao_finalizar(self):
        venda = self.service.criar(self._dados_venda())  # quantidade=2, estoque=10
        self.service.finalizar(venda.id, self.usuario)
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoqueAtual, 8)  # 10 - 2

    # --- Cancelamento ---

    def test_cancelar_venda_pendente_muda_status(self):
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Desistência do cliente')
        venda.refresh_from_db()
        self.assertEqual(venda.status, StatusVenda.CANCELADA)

    def test_cancelar_venda_pendente_nao_altera_estoque(self):
        venda = self.service.criar(self._dados_venda())  # quantidade=2
        self.service.cancelar(venda.id, 'Desistência')
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoqueAtual, 10)  # estoque intacto

    def test_cancelar_venda_finalizada_devolve_estoque(self):
        venda = self.service.criar(self._dados_venda())  # quantidade=2
        self.service.finalizar(venda.id)  # estoqueAtual: 10 - 2 = 8
        self.service.cancelar(venda.id, 'Devolução solicitada')
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.estoqueAtual, 10)  # 8 + 2 = 10

    def test_cancelar_venda_ja_cancelada_levanta_erro(self):
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Primeiro cancelamento')
        with self.assertRaises(ValidationError):
            self.service.cancelar(venda.id, 'Segundo cancelamento')

    def test_cancelamento_salva_motivo(self):
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Produto em falta')
        venda.refresh_from_db()
        self.assertEqual(venda.motivo_cancelamento, 'Produto em falta')

    def test_cancelamento_salva_data(self):
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Teste de data')
        venda.refresh_from_db()
        self.assertIsNotNone(venda.data_cancelamento)

    def test_cancelamento_salva_usuario(self):
        admin = Usuario.objects.create_user(
            username='admin_cancel', password='senha123', nome='Admin Cancel',
            perfil='ADMIN',
        )
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Cancelado pelo usuário', admin)
        venda.refresh_from_db()
        self.assertEqual(venda.cancelado_por, admin)

    # --- Autorização gerencial ---

    def test_admin_cancela_sem_senha_e_se_autoriza(self):
        admin = Usuario.objects.create_user(
            username='admin_auto', password='senha123', nome='Admin Auto',
            perfil='ADMIN',
        )
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Admin cancela', admin)
        venda.refresh_from_db()
        self.assertEqual(venda.status, StatusVenda.CANCELADA)
        self.assertEqual(venda.cancelado_por, admin)
        self.assertEqual(venda.autorizado_por, admin)

    def test_funcionario_com_senha_gerente_correta_cancela(self):
        from django.contrib.auth.hashers import make_password
        admin = Usuario.objects.create_user(
            username='admin_auth1', password='p', nome='Admin Auth', perfil='ADMIN',
        )
        admin.senha_operacional = make_password('senha_gerente')
        admin.save()
        venda = self.service.criar(self._dados_venda())
        self.service.cancelar(venda.id, 'Autorizado', self.usuario, 'senha_gerente')
        venda.refresh_from_db()
        self.assertEqual(venda.status, StatusVenda.CANCELADA)
        self.assertEqual(venda.cancelado_por, self.usuario)
        self.assertEqual(venda.autorizado_por, admin)

    def test_funcionario_com_senha_gerente_errada_levanta_erro(self):
        from django.contrib.auth.hashers import make_password
        admin = Usuario.objects.create_user(
            username='admin_auth2', password='p', nome='Admin Auth2', perfil='ADMIN',
        )
        admin.senha_operacional = make_password('senha_certa')
        admin.save()
        venda = self.service.criar(self._dados_venda())
        with self.assertRaises(ValidationError):
            self.service.cancelar(venda.id, 'Tentativa', self.usuario, 'senha_errada')

    def test_funcionario_sem_admin_com_senha_levanta_erro(self):
        venda = self.service.criar(self._dados_venda())
        with self.assertRaises(ValidationError):
            self.service.cancelar(venda.id, 'Sem admin', self.usuario, 'qualquer')
