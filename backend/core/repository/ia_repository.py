from django.db.models import Sum

from core.models import ItemVenda, Produto


class IARepository:

    def buscar_mais_vendidos(self):
        return (
            ItemVenda.objects
            .values('produto__id', 'produto__nome')
            .annotate(total_vendido=Sum('quantidade'))
            .order_by('-total_vendido')
        )

    def buscar_menos_vendidos(self):
        return (
            ItemVenda.objects
            .values('produto__id', 'produto__nome')
            .annotate(total_vendido=Sum('quantidade'))
            .order_by('total_vendido')
        )

    def buscar_produtos_parados(self):
        ids_com_venda = ItemVenda.objects.values_list('produto_id', flat=True).distinct()
        return Produto.objects.exclude(id__in=ids_com_venda)
