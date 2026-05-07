from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import PerfilUsuario
from core.serializers import ProdutoSerializer
from core.service import ProdutoService


class ProdutoListView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProdutoService()

    def get(self, request):
        produtos = self.service.listar()
        return Response(ProdutoSerializer(produtos, many=True).data)

    def post(self, request):
        serializer = ProdutoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            produto = self.service.criar(serializer.validated_data)
            return Response(ProdutoSerializer(produto).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)


class ProdutoDetailView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProdutoService()

    def get(self, request, id):
        try:
            produto = self.service.buscar(id)
            return Response(ProdutoSerializer(produto).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        serializer = ProdutoSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            produto = self.service.atualizar(id, serializer.validated_data)
            return Response(ProdutoSerializer(produto).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if request.user.perfil != PerfilUsuario.ADMIN:
            return Response({'erro': 'Apenas administradores podem excluir produtos.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            self.service.excluir(id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'erro': 'Produto não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response({'erro': 'Não é possível excluir porque existem registros vinculados.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)
