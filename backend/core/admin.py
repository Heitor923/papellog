from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models.usuario import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nome', 'email', 'perfil', 'ativo', 'is_staff', 'is_superuser')
    list_filter = ('perfil', 'ativo', 'is_staff')
    list_editable = ('perfil', 'ativo')
    search_fields = ('username', 'nome', 'email')

    fieldsets = UserAdmin.fieldsets + (
        ('Dados do Sistema', {'fields': ('nome', 'perfil', 'ativo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Dados do Sistema', {'fields': ('nome', 'perfil', 'ativo')}),
    )
