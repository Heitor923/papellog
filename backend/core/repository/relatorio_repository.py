from core.models import Venda


class RelatorioRepository:

    def buscar_por_periodo(self, data_inicio, data_fim):
        return Venda.objects.filter(data__date__gte=data_inicio, data__date__lte=data_fim)

    def buscar_por_cliente(self, cliente_id):
        return Venda.objects.filter(cliente_id=cliente_id)
