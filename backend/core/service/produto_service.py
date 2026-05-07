from django.core.exceptions import ValidationError

from core.repository import ProdutoRepository


class ProdutoService:

    def __init__(self):
        self.repo = ProdutoRepository()

    def listar(self):
        return self.repo.listar()

    def buscar(self, produto_id):
        return self.repo.buscar_por_id(produto_id)

    def criar(self, dados_produto):
        self._validar_preco(dados_produto.get('preco', 0))
        self._validar_estoque(dados_produto)
        return self.repo.criar(dados_produto)

    def atualizar(self, produto_id, dados_produto):
        produto = self.repo.buscar_por_id(produto_id)
        if 'preco' in dados_produto:
            self._validar_preco(dados_produto['preco'])
        self._validar_estoque(dados_produto)
        return self.repo.atualizar(produto, dados_produto)

    def excluir(self, produto_id):
        produto = self.repo.buscar_por_id(produto_id)
        self.repo.excluir(produto)

    def _validar_preco(self, preco):
        if float(preco) < 0:
            raise ValidationError('Preço não pode ser negativo.')

    def _validar_estoque(self, dados_produto):
        if 'estoqueAtual' in dados_produto and dados_produto['estoqueAtual'] < 0:
            raise ValidationError('Estoque atual não pode ser negativo.')
        if 'estoqueMinimo' in dados_produto and dados_produto['estoqueMinimo'] < 0:
            raise ValidationError('Estoque mínimo não pode ser negativo.')
