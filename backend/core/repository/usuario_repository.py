from core.models.usuario import Usuario


class UsuarioRepository:

    def listar(self):
        return Usuario.objects.all()

    def buscar_por_id(self, usuario_id):
        return Usuario.objects.get(id=usuario_id)

    def criar(self, dados_usuario):
        senha = dados_usuario.pop('senha', None)
        dados_usuario['is_active'] = dados_usuario.get('ativo', True)
        usuario = Usuario(**dados_usuario)
        usuario.set_password(senha)
        usuario.save()
        return usuario

    def atualizar(self, usuario, dados_usuario):
        if 'ativo' in dados_usuario:
            dados_usuario['is_active'] = dados_usuario['ativo']
        for campo, valor in dados_usuario.items():
            setattr(usuario, campo, valor)
        usuario.save()
        return usuario

    def redefinir_senha(self, usuario, nova_senha):
        usuario.set_password(nova_senha)
        usuario.save()
