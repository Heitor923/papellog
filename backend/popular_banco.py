from decimal import Decimal
from core.models import Usuario, Cliente, Produto, Venda, ItemVenda
from core.models.venda import StatusVenda

print("Criando clientes...")

clientes = []

for i in range(1, 21):
    cliente, _ = Cliente.objects.get_or_create(
        cpf=f"000000000{i:02}",
        defaults={
            "nome": f"Cliente {i}",
            "email": f"cliente{i}@email.com",
            "telefone": f"6199999{i:04}",
            "endereco": f"Rua {i}"
        }
    )
    clientes.append(cliente)

print("Criando produtos...")

produtos = []

for i in range(1, 31):
    produto, _ = Produto.objects.get_or_create(
        sku=f"SKU{i:03}",
        defaults={
            "nome": f"Produto {i}",
            "descricao": f"Descrição do Produto {i}",
            "preco": Decimal("10.00") + i,
            "estoqueAtual": 100,
            "estoqueMinimo": 10,
            "ativo": True
        }
    )
    produtos.append(produto)

print("Buscando usuário...")

usuario = Usuario.objects.filter(is_superuser=True).first()

if not usuario:
    raise Exception("Nenhum usuário administrador encontrado.")

print("Criando vendas...")

for i in range(1, 51):

    cliente = clientes[i % len(clientes)]

    venda = Venda.objects.create(
        cliente=cliente,
        usuario=usuario,
        status=StatusVenda.PENDENTE
    )

    total = Decimal("0.00")

    for j in range(3):

        produto = produtos[(i + j) % len(produtos)]

        quantidade = (j + 1)

        subtotal = produto.preco * quantidade

        ItemVenda.objects.create(
            venda=venda,
            produto=produto,
            quantidade=quantidade,
            precoUnitario=produto.preco,
            subtotal=subtotal
        )

        total += subtotal

    venda.total = total

    if i % 5 == 0:
        venda.status = StatusVenda.CANCELADA

    elif i % 2 == 0:
        venda.status = StatusVenda.FINALIZADA

    venda.save()

print("Banco populado com sucesso!")