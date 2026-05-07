from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField()
    sku = models.CharField(max_length=50, unique=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoqueAtual = models.IntegerField(default=0)
    estoqueMinimo = models.IntegerField(default=0)
    ativo = models.BooleanField(default=True)

    class Meta:
        db_table = 'produtos'

    def __str__(self):
        return self.nome
