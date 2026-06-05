from django.utils import timezone

from core.models import ItemVenda, StatusVenda, Venda


class VendaRepository:

    def listar(self):
        return Venda.objects.all()

    def buscar_por_id(self, venda_id):
        return Venda.objects.get(id=venda_id)

    def criar(self, dados_venda):
        return Venda.objects.create(**dados_venda)

    def adicionar_item(self, venda, produto, quantidade, preco_unitario):
        subtotal = preco_unitario * quantidade
        return ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            precoUnitario=preco_unitario,
            subtotal=subtotal,
        )

    def atualizar_total(self, venda, total):
        venda.total = total
        venda.save()

    def atualizar_status(self, venda, novo_status):
        venda.status = novo_status
        venda.save()

    def finalizar(self, venda, usuario=None):
        venda.status = StatusVenda.FINALIZADA
        venda.finalizado_por = usuario
        venda.data_finalizacao = timezone.now()
        venda.save()
        return venda

    def cancelar(self, venda, motivo, usuario=None, autorizado_por=None):
        venda.status = StatusVenda.CANCELADA
        venda.motivo_cancelamento = motivo
        venda.data_cancelamento = timezone.now()
        venda.cancelado_por = usuario
        venda.autorizado_por = autorizado_por
        venda.save()
        return venda
