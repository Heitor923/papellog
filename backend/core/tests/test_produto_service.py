from django.core.exceptions import ValidationError
from django.test import TestCase

from core.service import ProdutoService


class ProdutoServiceTest(TestCase):

    def setUp(self):
        self.service = ProdutoService()
        self.dados_base = {
            'nome': 'Caderno',
            'descricao': 'Caderno universitário 200 folhas',
            'sku': 'CAD001',
            'preco': '10.00',
            'estoqueAtual': 50,
            'estoqueMinimo': 5,
            'ativo': True,
        }

    def test_criar_produto_valido(self):
        produto = self.service.criar(self.dados_base.copy())
        self.assertEqual(produto.nome, 'Caderno')
        self.assertEqual(produto.sku, 'CAD001')

    def test_preco_negativo_levanta_erro(self):
        dados = self.dados_base.copy()
        dados['preco'] = '-5.00'
        with self.assertRaises(ValidationError):
            self.service.criar(dados)

    def test_preco_zero_permitido(self):
        dados = self.dados_base.copy()
        dados['preco'] = '0.00'
        produto = self.service.criar(dados)
        self.assertEqual(float(produto.preco), 0.0)

    def test_atualizar_preco_negativo_levanta_erro(self):
        produto = self.service.criar(self.dados_base.copy())
        with self.assertRaises(ValidationError):
            self.service.atualizar(produto.id, {'preco': '-1.00'})
