from core.models import Cliente, Venda


class ClienteRepository:

    def listar(self):
        return Cliente.objects.all()

    def buscar_por_id(self, cliente_id):
        return Cliente.objects.get(id=cliente_id)

    def buscar_por_cpf(self, cpf):
        return Cliente.objects.filter(cpf=cpf).first()

    def tem_vendas(self, cliente_id):
        return Venda.objects.filter(cliente_id=cliente_id).exists()

    def salvar(self, dados_cliente):
        return Cliente.objects.create(**dados_cliente)

    def atualizar(self, cliente, dados_cliente):
        for campo, valor in dados_cliente.items():
            setattr(cliente, campo, valor)
        cliente.save()
        return cliente

    def excluir(self, cliente):
        cliente.delete()
