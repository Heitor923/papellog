from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import StatusVenda
from core.repository import ProdutoRepository, VendaRepository


class VendaService:

    def __init__(self):
        self.venda_repo = VendaRepository()
        self.produto_repo = ProdutoRepository()

    def listar(self):
        return self.venda_repo.listar()

    def buscar(self, venda_id):
        return self.venda_repo.buscar_por_id(venda_id)

    @transaction.atomic
    def criar(self, dados):
        lista_itens = dados.get('itens', [])
        if not lista_itens:
            raise ValidationError('A venda deve ter pelo menos um item.')

        itens_validados = []
        for dados_item in lista_itens:
            quantidade = dados_item['quantidade']
            if quantidade <= 0:
                raise ValidationError('A quantidade de cada item deve ser maior que zero.')
            produto = self.produto_repo.buscar_por_id(dados_item['produto_id'])
            if produto.estoqueAtual < quantidade:
                raise ValidationError(
                    f'Estoque insuficiente para "{produto.nome}". '
                    f'Disponível: {produto.estoqueAtual}, solicitado: {quantidade}.'
                )
            itens_validados.append({'produto': produto, 'quantidade': quantidade})

        venda = self.venda_repo.criar({
            'cliente_id': dados['cliente_id'],
            'usuario_id': dados['usuario_id'],
        })

        total = Decimal('0')
        for item in itens_validados:
            produto = item['produto']
            quantidade = item['quantidade']
            self.venda_repo.adicionar_item(venda, produto, quantidade, produto.preco)
            total += produto.preco * quantidade

        self.venda_repo.atualizar_total(venda, total)
        return venda

    @transaction.atomic
    def finalizar(self, venda_id):
        venda = self.venda_repo.buscar_por_id(venda_id)

        if venda.status != StatusVenda.PENDENTE:
            raise ValidationError('Apenas vendas pendentes podem ser finalizadas.')

        for item in venda.itens.all():
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            if produto.estoqueAtual < item.quantidade:
                raise ValidationError(
                    f'Estoque insuficiente para "{produto.nome}". '
                    f'Disponível: {produto.estoqueAtual}, solicitado: {item.quantidade}.'
                )
            self.produto_repo.atualizar_estoque(produto, item.quantidade)

        self.venda_repo.atualizar_status(venda, StatusVenda.FINALIZADA)
        return venda
