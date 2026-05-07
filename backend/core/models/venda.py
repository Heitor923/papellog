from django.conf import settings
from django.db import models


class StatusVenda(models.TextChoices):
    PENDENTE = 'PENDENTE', 'Pendente'
    FINALIZADA = 'FINALIZADA', 'Finalizada'
    CANCELADA = 'CANCELADA', 'Cancelada'


class Venda(models.Model):
    data = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey('Cliente', on_delete=models.PROTECT, related_name='vendas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='vendas')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=StatusVenda.choices,
        default=StatusVenda.PENDENTE,
    )

    class Meta:
        db_table = 'vendas'

    def __str__(self):
        return f'Venda {self.id} — {self.status}'
