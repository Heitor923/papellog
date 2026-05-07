from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import PerfilUsuario
from core.serializers import ClienteSerializer
from core.service import ClienteService


class ClienteListView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClienteService()

    def get(self, request):
        clientes = self.service.listar()
        return Response(ClienteSerializer(clientes, many=True).data)

    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            cliente = self.service.criar(serializer.validated_data)
            return Response(ClienteSerializer(cliente).data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)


class ClienteDetailView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ClienteService()

    def get(self, request, id):
        try:
            cliente = self.service.buscar(id)
            return Response(ClienteSerializer(cliente).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        serializer = ClienteSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            cliente = self.service.atualizar(id, serializer.validated_data)
            return Response(ClienteSerializer(cliente).data)
        except ObjectDoesNotExist:
            return Response({'erro': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        if request.user.perfil != PerfilUsuario.ADMIN:
            return Response({'erro': 'Apenas administradores podem excluir clientes.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            self.service.excluir(id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response({'erro': 'Cliente não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except ProtectedError:
            return Response({'erro': 'Não é possível excluir porque existem registros vinculados.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'erro': e.messages}, status=status.HTTP_400_BAD_REQUEST)
