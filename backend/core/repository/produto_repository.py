from core.models import Produto


class ProdutoRepository:

    def listar(self):
        return Produto.objects.all()

    def buscar_por_id(self, produto_id):
        return Produto.objects.get(id=produto_id)

    def atualizar_estoque(self, produto, quantidade):
        produto.estoqueAtual -= quantidade
        produto.save()

    def criar(self, dados_produto):
        return Produto.objects.create(**dados_produto)

    def atualizar(self, produto, dados_produto):
        for campo, valor in dados_produto.items():
            setattr(produto, campo, valor)
        produto.save()
        return produto

    def excluir(self, produto):
        produto.delete()
