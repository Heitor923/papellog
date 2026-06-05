from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import VendaCriarSerializer, VendaSerializer
from core.service import VendaService


class VendaListView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = VendaService()

    def get(self, request):
        vendas = self.service.listar()
        return Response(VendaSerializer(vendas, many=True).data)

    def post(self, request):
        serializer = VendaCriarSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            dados = serializer.validated_data
            dados['usuario'] = request.user
            venda = self.service.criar(dados)
            return Response(VendaSerializer(venda).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)


class VendaDetailView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = VendaService()

    def get(self, request, id):
        try:
            venda = self.service.buscar(id)
            return Response(VendaSerializer(venda).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)


class VendaFinalizarView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = VendaService()

    def post(self, request, id):
        try:
            venda = self.service.finalizar(id, request.user)
            return Response(VendaSerializer(venda).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)


class VendaCancelarView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = VendaService()

    def post(self, request, id):
        motivo = request.data.get('motivo', '')
        senha_operacional_gerente = request.data.get('senha_operacional_gerente', '')
        try:
            venda = self.service.cancelar(id, motivo, request.user, senha_operacional_gerente)
            return Response(VendaSerializer(venda).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Venda não encontrada.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)
