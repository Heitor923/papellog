from django.core.exceptions import ValidationError

from core.repository.usuario_repository import UsuarioRepository


class UsuarioService:

    def __init__(self):
        self.repo = UsuarioRepository()

    def listar(self):
        return self.repo.listar()

    def buscar(self, usuario_id):
        return self.repo.buscar_por_id(usuario_id)

    def criar(self, dados_usuario):
        if not dados_usuario.get('username'):
            raise ValidationError('Username é obrigatório.')
        if not dados_usuario.get('senha'):
            raise ValidationError('Senha é obrigatória.')
        return self.repo.criar(dados_usuario)

    def atualizar(self, usuario_id, dados_usuario):
        usuario = self.repo.buscar_por_id(usuario_id)
        return self.repo.atualizar(usuario, dados_usuario)

    def redefinir_senha(self, usuario_id, nova_senha):
        if not nova_senha:
            raise ValidationError('A nova senha não pode ser vazia.')
        usuario = self.repo.buscar_por_id(usuario_id)
        self.repo.redefinir_senha(usuario, nova_senha)
