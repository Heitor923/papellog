from rest_framework import serializers

from core.models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    estoqueBaixo = serializers.SerializerMethodField()

    def get_estoqueBaixo(self, obj):
        return obj.estoqueAtual <= obj.estoqueMinimo

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'sku', 'preco', 'estoqueAtual', 'estoqueMinimo', 'ativo', 'estoqueBaixo']
