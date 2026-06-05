from datetime import datetime
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db.models import Sum

from core.models import StatusVenda
from core.repository.relatorio_avancado_repository import RelatorioAvancadoRepository


class RelatorioAvancadoService:

    def __init__(self):
        self.repo = RelatorioAvancadoRepository()

    def gerar(self, filtros_raw):
        filtros = self._normalizar_filtros(filtros_raw)

        vendas = self.repo.buscar_vendas(filtros)
        finalizadas = vendas.filter(status=StatusVenda.FINALIZADA)
        total_vendido = finalizadas.aggregate(total=Sum('total'))['total'] or Decimal('0')
        quantidade_finalizadas = finalizadas.count()
        ticket_medio = (
            round(total_vendido / quantidade_finalizadas, 2)
            if quantidade_finalizadas > 0 else Decimal('0')
        )

        # EXPORTAÇÃO FUTURA
        # Ponto de extensão: antes de retornar, chamar exportar(formato, dados)
        # Para PDF: instalar weasyprint ou reportlab, gerar BytesIO e retornar HttpResponse
        # Para Excel: instalar openpyxl, gerar .xlsx via openpyxl.Workbook() e retornar
        # Assinatura sugerida: RelatorioAvancadoService.exportar(formato, dados) → bytes

        return {
            'filtros': filtros,
            'vendas': list(vendas.order_by('-data')),
            'total_vendido': total_vendido,
            'quantidade_vendas': vendas.count(),
            'ticket_medio': ticket_medio,
            'quantidade_canceladas': vendas.filter(status=StatusVenda.CANCELADA).count(),
            'quantidade_pendentes': vendas.filter(status=StatusVenda.PENDENTE).count(),
            'ranking_produtos': self.repo.ranking_produtos(filtros),
            'ranking_funcionarios': self.repo.ranking_funcionarios(filtros),
            'produtos_criticos': self._enriquecer_criticos(self.repo.produtos_criticos()),
        }

    def _enriquecer_criticos(self, produtos):
        return [
            {
                'produto': p,
                'diferenca': p.estoqueMinimo - p.estoqueAtual,
            }
            for p in produtos
        ]

    def _normalizar_filtros(self, filtros_raw):
        data_inicio = self._parse_data(filtros_raw.get('data_inicio'))
        data_fim = self._parse_data(filtros_raw.get('data_fim'))

        if data_inicio and data_fim and data_inicio > data_fim:
            raise ValidationError('A data inicial deve ser anterior à data final.')

        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'cliente_id': self._to_int(filtros_raw.get('cliente_id')),
            'usuario_id': self._to_int(filtros_raw.get('usuario_id')),
            'status': filtros_raw.get('status') or None,
        }

    def _parse_data(self, valor):
        if not valor:
            return None
        try:
            return datetime.strptime(str(valor).strip(), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            raise ValidationError('Formato de data inválido. Use YYYY-MM-DD.')

    def _to_int(self, valor):
        try:
            return int(valor) if valor else None
        except (ValueError, TypeError):
            return None
