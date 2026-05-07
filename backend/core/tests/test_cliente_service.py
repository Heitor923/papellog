from django.core.exceptions import ValidationError
from django.test import TestCase

from core.service import ClienteService


class ClienteServiceTest(TestCase):

    def setUp(self):
        self.service = ClienteService()
        self.dados_base = {
            'cpf': '12345678901',
            'nome': 'João Silva',
            'email': 'joao@email.com',
            'telefone': '',
            'endereco': '',
        }

    def test_criar_cliente_valido(self):
        cliente = self.service.criar(self.dados_base.copy())
        self.assertEqual(cliente.cpf, '12345678901')
        self.assertEqual(cliente.nome, 'João Silva')

    def test_cpf_duplicado_levanta_erro(self):
        self.service.criar(self.dados_base.copy())
        with self.assertRaises(ValidationError):
            self.service.criar(self.dados_base.copy())

    def test_email_invalido_levanta_erro(self):
        dados = self.dados_base.copy()
        dados['email'] = 'email-invalido'
        with self.assertRaises(ValidationError):
            self.service.criar(dados)

    def test_excluir_cliente_com_vendas_levanta_erro(self):
        from core.models import Cliente, Produto, Usuario
        from decimal import Decimal
        from core.service import VendaService

        cliente = self.service.criar(self.dados_base.copy())
        usuario = Usuario.objects.create_user(username='u', password='p', nome='U')
        produto = Produto.objects.create(
            nome='Prod', descricao='Desc', sku='SKU999',
            preco=Decimal('1.00'), estoqueAtual=10, estoqueMinimo=1,
        )
        VendaService().criar({
            'cliente_id': cliente.id,
            'usuario_id': usuario.id,
            'itens': [{'produto_id': produto.id, 'quantidade': 1}],
        })

        with self.assertRaises(ValidationError):
            self.service.excluir(cliente.id)
