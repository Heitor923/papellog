from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models import ProtectedError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def tratar_excecao(exc, context):
    resposta = exception_handler(exc, context)
    if resposta is not None:
        return resposta

    if isinstance(exc, ValidationError):
        return Response(
            {'erro': exc.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {'erro': 'Recurso não encontrado.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    if isinstance(exc, ProtectedError):
        return Response(
            {'erro': 'Não é possível excluir porque existem registros vinculados.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(
        {'erro': 'Erro interno no servidor.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
