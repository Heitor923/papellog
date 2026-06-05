from datetime import timedelta
from decimal import Decimal

from django.db.models import F, Sum
from django.utils import timezone

from core.models import ItemVenda, Produto, StatusVenda, Venda


class DashboardRepository:

    def vendas_do_dia(self):
        hoje = timezone.localdate()
        return Venda.objects.filter(data__date=hoje).count()

    def total_vendido_mes(self):
        hoje = timezone.localdate()
        resultado = Venda.objects.filter(
            status=StatusVenda.FINALIZADA,
            data__year=hoje.year,
            data__month=hoje.month,
        ).aggregate(total=Sum('total'))
        return resultado['total'] or Decimal('0')

    def count_produtos_ativos(self):
        return Produto.objects.filter(ativo=True).count()

    def count_estoque_baixo(self):
        return Produto.objects.filter(estoqueAtual__lte=F('estoqueMinimo')).count()

    def count_vendas_pendentes(self):
        return Venda.objects.filter(status=StatusVenda.PENDENTE).count()

    def count_vendas_canceladas(self):
        return Venda.objects.filter(status=StatusVenda.CANCELADA).count()

    def ultimas_vendas(self, limite=5):
        return Venda.objects.select_related('cliente', 'usuario').order_by('-data')[:limite]

    def produtos_mais_vendidos(self, limite=5):
        return (
            ItemVenda.objects
            .values('produto__id', 'produto__nome', 'produto__sku')
            .annotate(total_vendido=Sum('quantidade'))
            .order_by('-total_vendido')
            [:limite]
        )

    def produtos_menos_vendidos(self, limite=5):
        return (
            ItemVenda.objects
            .values('produto__id', 'produto__nome', 'produto__sku')
            .annotate(total_vendido=Sum('quantidade'))
            .order_by('total_vendido')
            [:limite]
        )

    def produtos_parados(self):
        ids_com_venda = ItemVenda.objects.values_list('produto_id', flat=True).distinct()
        return list(Produto.objects.filter(ativo=True).exclude(id__in=ids_com_venda))

    def produtos_para_reposicao(self, limite=10):
        return list(
            Produto.objects.filter(
                ativo=True,
                estoqueAtual__lte=F('estoqueMinimo'),
            ).order_by('estoqueAtual')[:limite]
        )

    def vendas_por_produto_periodo(self, dias=30):
        corte = timezone.now() - timedelta(days=dias)
        return list(
            ItemVenda.objects
            .filter(venda__data__gte=corte, venda__status=StatusVenda.FINALIZADA)
            .values('produto__id', 'produto__nome', 'produto__sku', 'produto__estoqueAtual')
            .annotate(total_vendido=Sum('quantidade'))
        )

    def produtos_estoque_baixo(self, limite=5):
        return list(
            Produto.objects.filter(
                estoqueAtual__lte=F('estoqueMinimo')
            ).order_by('estoqueAtual')[:limite]
        )
