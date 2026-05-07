from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import ProdutoSerializer
from core.service.ia_service import IAService


class IAMaisVendidosView(APIView):
    def get(self, request):
        return Response(IAService().analisar_mais_vendidos())


class IAMenosVendidosView(APIView):
    def get(self, request):
        return Response(IAService().analisar_menos_vendidos())


class IAProdutosParadosView(APIView):
    def get(self, request):
        produtos = IAService().identificar_produtos_parados()
        return Response(ProdutoSerializer(produtos, many=True).data)
