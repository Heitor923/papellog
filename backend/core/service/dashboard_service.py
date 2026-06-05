from core.repository.dashboard_repository import DashboardRepository


class DashboardService:

    DIAS_HISTORICO = 30

    def __init__(self):
        self.repo = DashboardRepository()

    def resumo(self):
        vendas_periodo = self.repo.vendas_por_produto_periodo(dias=self.DIAS_HISTORICO)
        produtos_reposicao = self.repo.produtos_para_reposicao()

        return {
            'vendas_do_dia': self.repo.vendas_do_dia(),
            'total_mes': self.repo.total_vendido_mes(),
            'produtos_cadastrados': self.repo.count_produtos_ativos(),
            'estoque_baixo_count': self.repo.count_estoque_baixo(),
            'vendas_pendentes': self.repo.count_vendas_pendentes(),
            'vendas_canceladas': self.repo.count_vendas_canceladas(),
            'ultimas_vendas': list(self.repo.ultimas_vendas()),
            'mais_vendidos': list(self.repo.produtos_mais_vendidos()),
            'menos_vendidos': list(self.repo.produtos_menos_vendidos()),
            'parados': self.repo.produtos_parados(),
            'estoque_baixo': self.repo.produtos_estoque_baixo(),
            'sugestao_reposicao': self._calcular_sugestao(produtos_reposicao),
            'previsao_duracao': self._calcular_previsao(vendas_periodo),
        }

    def _calcular_sugestao(self, produtos):
        return [
            {
                'produto': p,
                'gap': max(0, p.estoqueMinimo - p.estoqueAtual),
            }
            for p in produtos
        ]

    def _calcular_previsao(self, vendas_periodo):
        resultado = []
        for item in vendas_periodo:
            media_diaria = item['total_vendido'] / self.DIAS_HISTORICO
            if media_diaria > 0:
                dias_restantes = item['produto__estoqueAtual'] / media_diaria
                resultado.append({
                    'produto_nome': item['produto__nome'],
                    'produto_sku': item['produto__sku'],
                    'estoque_atual': item['produto__estoqueAtual'],
                    'media_diaria': round(media_diaria, 1),
                    'dias_restantes': round(dias_restantes),
                })
        return sorted(resultado, key=lambda x: x['dias_restantes'])[:10]
