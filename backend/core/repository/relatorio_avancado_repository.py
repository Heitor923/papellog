from django.db.models import Count, F, Sum

from core.models import ItemVenda, Produto, StatusVenda, Venda


class RelatorioAvancadoRepository:

    def buscar_vendas(self, filtros):
        qs = Venda.objects.select_related('cliente', 'usuario')
        if filtros.get('data_inicio'):
            qs = qs.filter(data__date__gte=filtros['data_inicio'])
        if filtros.get('data_fim'):
            qs = qs.filter(data__date__lte=filtros['data_fim'])
        if filtros.get('cliente_id'):
            qs = qs.filter(cliente_id=filtros['cliente_id'])
        if filtros.get('usuario_id'):
            qs = qs.filter(usuario_id=filtros['usuario_id'])
        if filtros.get('status'):
            qs = qs.filter(status=filtros['status'])
        return qs

    def ranking_produtos(self, filtros, limite=10):
        qs = ItemVenda.objects.filter(venda__status=StatusVenda.FINALIZADA)
        if filtros.get('data_inicio'):
            qs = qs.filter(venda__data__date__gte=filtros['data_inicio'])
        if filtros.get('data_fim'):
            qs = qs.filter(venda__data__date__lte=filtros['data_fim'])
        if filtros.get('cliente_id'):
            qs = qs.filter(venda__cliente_id=filtros['cliente_id'])
        if filtros.get('usuario_id'):
            qs = qs.filter(venda__usuario_id=filtros['usuario_id'])
        return list(
            qs.values('produto__id', 'produto__nome', 'produto__sku')
            .annotate(
                quantidade_vendida=Sum('quantidade'),
                valor_vendido=Sum('subtotal'),
            )
            .order_by('-valor_vendido')
            [:limite]
        )

    def ranking_funcionarios(self, filtros, limite=10):
        qs = Venda.objects.filter(status=StatusVenda.FINALIZADA)
        if filtros.get('data_inicio'):
            qs = qs.filter(data__date__gte=filtros['data_inicio'])
        if filtros.get('data_fim'):
            qs = qs.filter(data__date__lte=filtros['data_fim'])
        if filtros.get('cliente_id'):
            qs = qs.filter(cliente_id=filtros['cliente_id'])
        if filtros.get('usuario_id'):
            qs = qs.filter(usuario_id=filtros['usuario_id'])
        return list(
            qs.values('usuario__id', 'usuario__nome', 'usuario__username')
            .annotate(
                quantidade_vendas=Count('id'),
                valor_vendido=Sum('total'),
            )
            .order_by('-valor_vendido')
            [:limite]
        )

    def produtos_criticos(self):
        return list(
            Produto.objects.filter(
                ativo=True,
                estoqueAtual__lte=F('estoqueMinimo'),
            ).order_by('estoqueAtual')
        )
