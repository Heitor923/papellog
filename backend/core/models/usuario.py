from django.contrib.auth.models import AbstractUser
from django.db import models


class PerfilUsuario(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    FUNCIONARIO = 'FUNCIONARIO', 'Funcionário'


class Usuario(AbstractUser):
    nome = models.CharField(max_length=150)
    perfil = models.CharField(
        max_length=20,
        choices=PerfilUsuario.choices,
        default=PerfilUsuario.FUNCIONARIO,
    )
    ativo = models.BooleanField(default=True)
    senha_operacional = models.CharField(max_length=128, null=True, blank=True)

    class Meta:
        db_table = 'usuarios'

    def __str__(self):
        return self.username
