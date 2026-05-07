from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import VendaSerializer
from core.service import RelatorioService


class RelatorioVendaPeriodoView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RelatorioService()

    def get(self, request):
        inicio = request.query_params.get('inicio')
        fim = request.query_params.get('fim')
        try:
            vendas = self.service.vendas_por_periodo(inicio, fim)
            return Response(VendaSerializer(vendas, many=True).data)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)


class RelatorioVendaClienteView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = RelatorioService()

    def get(self, request, cliente_id):
        vendas = self.service.vendas_por_cliente(cliente_id)
        return Response(VendaSerializer(vendas, many=True).data)
