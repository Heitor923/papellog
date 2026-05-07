from rest_framework import serializers

from core.models import ItemVenda, Venda


class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = ['id', 'produto_id', 'quantidade', 'precoUnitario', 'subtotal']


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True, read_only=True)

    class Meta:
        model = Venda
        fields = ['id', 'data', 'cliente_id', 'usuario_id', 'total', 'status', 'itens']


class ItemVendaCriarSerializer(serializers.Serializer):
    produto_id = serializers.IntegerField()
    quantidade = serializers.IntegerField(min_value=1)


class VendaCriarSerializer(serializers.Serializer):
    cliente_id = serializers.IntegerField()
    usuario_id = serializers.IntegerField()
    itens = ItemVendaCriarSerializer(many=True)
