from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from core.models import PerfilUsuario, StatusVenda
from core.repository import ProdutoRepository, VendaRepository
from core.repository.usuario_repository import UsuarioRepository


class VendaService:

    def __init__(self):
        self.venda_repo = VendaRepository()
        self.produto_repo = ProdutoRepository()
        self.usuario_repo = UsuarioRepository()

    def listar(self):
        return self.venda_repo.listar()

    def buscar(self, venda_id):
        return self.venda_repo.buscar_por_id(venda_id)

    @transaction.atomic
    def criar(self, dados):
        lista_itens = dados.get('itens', [])
        if not lista_itens:
            raise ValidationError('A venda deve ter pelo menos um item.')

        self._validar_itens(lista_itens)

        dados_venda = {
            'cliente_id': dados['cliente_id'],
            'usuario_id': dados['usuario'].id,
        }
        venda = self.venda_repo.criar(dados_venda)

        total = Decimal('0')
        for dados_item in lista_itens:
            produto = self.produto_repo.buscar_por_id(dados_item['produto_id'])
            if not produto.ativo:
                raise ValidationError(f'O produto "{produto.nome}" está inativo e não pode ser vendido.')
            quantidade = dados_item['quantidade']
            self.venda_repo.adicionar_item(venda, produto, quantidade, produto.preco)
            total += produto.preco * quantidade

        self.venda_repo.atualizar_total(venda, total)
        return venda

    @transaction.atomic
    def finalizar(self, venda_id, usuario=None):
        venda = self.venda_repo.buscar_por_id(venda_id)

        if venda.status != StatusVenda.PENDENTE:
            raise ValidationError('Apenas vendas pendentes podem ser finalizadas.')

        for item in venda.itens.all():
            produto = self.produto_repo.buscar_por_id(item.produto_id)
            if produto.estoqueAtual < item.quantidade:
                raise ValidationError(
                    f'Estoque insuficiente para "{produto.nome}". '
                    f'Disponível: {produto.estoqueAtual}, solicitado: {item.quantidade}.'
                )
            self.produto_repo.atualizar_estoque(produto, item.quantidade)

        self.venda_repo.finalizar(venda, usuario)
        return venda

    @transaction.atomic
    def cancelar(self, venda_id, motivo, usuario=None, senha_operacional_gerente=None):
        venda = self.venda_repo.buscar_por_id(venda_id)

        if not motivo or not str(motivo).strip():
            raise ValidationError('Informe o motivo do cancelamento.')

        if venda.status == StatusVenda.CANCELADA:
            raise ValidationError('Esta venda já está cancelada.')

        autorizado_por = self._autorizar_cancelamento(usuario, senha_operacional_gerente)

        if venda.status == StatusVenda.FINALIZADA:
            for item in venda.itens.all():
                produto = self.produto_repo.buscar_por_id(item.produto_id)
                self.produto_repo.devolver_estoque(produto, item.quantidade)

        self.venda_repo.cancelar(venda, motivo, usuario, autorizado_por)
        return venda

    def _autorizar_cancelamento(self, usuario, senha_operacional_gerente):
        if usuario is None:
            return None
        if usuario.perfil == PerfilUsuario.ADMIN:
            return usuario
        admin = self.usuario_repo.buscar_admin_por_senha_operacional(
            senha_operacional_gerente or ''
        )
        if not admin:
            raise ValidationError(
                'Senha gerencial inválida. Solicite autorização de um administrador.'
            )
        return admin

    def _validar_itens(self, lista_itens):
        produtos_informados = set()
        for dados_item in lista_itens:
            produto_id = dados_item.get('produto_id')
            if produto_id in produtos_informados:
                raise ValidationError('A venda não pode conter o mesmo produto mais de uma vez.')
            produtos_informados.add(produto_id)

            quantidade = dados_item.get('quantidade')
            try:
                quantidade = int(quantidade)
            except (TypeError, ValueError):
                raise ValidationError('A quantidade de cada item deve ser um número inteiro maior ou igual a 1.')

            if quantidade < 1:
                raise ValidationError('A quantidade de cada item deve ser maior ou igual a 1.')

            dados_item['quantidade'] = quantidade

