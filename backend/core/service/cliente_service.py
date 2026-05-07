from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from core.repository import ClienteRepository


class ClienteService:

    def __init__(self):
        self.repo = ClienteRepository()

    def listar(self):
        return self.repo.listar()

    def buscar(self, cliente_id):
        return self.repo.buscar_por_id(cliente_id)

    def criar(self, dados_cliente):
        self._validar_email(dados_cliente.get('email', ''))
        self._validar_cpf_unico(dados_cliente.get('cpf', ''))
        return self.repo.criar(dados_cliente)

    def atualizar(self, cliente_id, dados_cliente):
        cliente = self.repo.buscar_por_id(cliente_id)
        if 'email' in dados_cliente:
            self._validar_email(dados_cliente['email'])
        if 'cpf' in dados_cliente and dados_cliente['cpf'] != cliente.cpf:
            self._validar_cpf_unico(dados_cliente['cpf'])
        return self.repo.atualizar(cliente, dados_cliente)

    def excluir(self, cliente_id):
        if self.repo.tem_vendas(cliente_id):
            raise ValidationError('Não é possível excluir cliente com vendas registradas.')
        cliente = self.repo.buscar_por_id(cliente_id)
        self.repo.excluir(cliente)

    def _validar_email(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Email inválido.')

    def _validar_cpf_unico(self, cpf):
        if self.repo.buscar_por_cpf(cpf):
            raise ValidationError('CPF já cadastrado.')
