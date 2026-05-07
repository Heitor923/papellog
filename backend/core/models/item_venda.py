from django.db import models


class ItemVenda(models.Model):
    venda = models.ForeignKey('Venda', on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey('Produto', on_delete=models.PROTECT, related_name='itens_venda')
    quantidade = models.IntegerField()
    precoUnitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'itens_venda'

    def __str__(self):
        return f'{self.quantidade}x {self.produto_id} (Venda {self.venda_id})'
