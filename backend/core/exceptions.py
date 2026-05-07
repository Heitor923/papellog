from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def tratar_excecao(exc, context):
    # tenta o tratamento padrão do DRF primeiro
    resposta = exception_handler(exc, context)
    if resposta is not None:
        return resposta

    # erro de validação de regra de negócio
    if isinstance(exc, ValidationError):
        return Response(
            {'erro': exc.messages},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # recurso não encontrado no banco
    if isinstance(exc, ObjectDoesNotExist):
        return Response(
            {'erro': 'Recurso não encontrado.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    # qualquer outro erro inesperado
    return Response(
        {'erro': 'Erro interno no servidor.'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
