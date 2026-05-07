from datetime import datetime

from django.core.exceptions import ValidationError

from core.repository import RelatorioRepository


class RelatorioService:

    def __init__(self):
        self.repo = RelatorioRepository()

    def vendas_por_periodo(self, inicio, fim):
        if not inicio or not fim:
            raise ValidationError('Informe os parâmetros inicio e fim.')

        try:
            data_inicio = datetime.strptime(inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(fim, '%Y-%m-%d').date()
        except ValueError:
            raise ValidationError('Formato de data inválido. Use YYYY-MM-DD.')

        if data_inicio > data_fim:
            raise ValidationError('A data de início deve ser anterior à data de fim.')

        return self.repo.buscar_por_periodo(data_inicio, data_fim)

    def vendas_por_cliente(self, cliente_id):
        return self.repo.buscar_por_cliente(cliente_id)
