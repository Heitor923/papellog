from rest_framework import serializers

from core.models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'sku', 'preco', 'estoqueAtual', 'estoqueMinimo', 'ativo']
