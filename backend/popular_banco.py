import os
import random
from decimal import Decimal
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papellog.settings")

import django
django.setup()

from django.utils import timezone
from core.models import Cliente, Produto, Venda, ItemVenda, Usuario


def criar_usuarios():
    gerente, _ = Usuario.objects.get_or_create(
        username="gerente",
        defaults={
            "nome": "Carlos Henrique Almeida",
            "email": "gerente@papellog.com",
            "perfil": "ADMIN",
            "is_staff": True,
            "is_superuser": True,
            "ativo": True,
        }
    )
    gerente.set_password("123456")
    gerente.save()

    funcionarios_dados = [
        ("ana.souza", "Ana Souza", "ana@papellog.com"),
        ("bruno.lima", "Bruno Lima", "bruno@papellog.com"),
        ("mariana.costa", "Mariana Costa", "mariana@papellog.com"),
    ]

    funcionarios = []

    for username, nome, email in funcionarios_dados:
        funcionario, _ = Usuario.objects.get_or_create(
            username=username,
            defaults={
                "nome": nome,
                "email": email,
                "perfil": "FUNCIONARIO",
                "ativo": True,
            }
        )
        funcionario.set_password("123456")
        funcionario.save()
        funcionarios.append(funcionario)

    return gerente, funcionarios


def criar_clientes():
    clientes_dados = [
        ("João Pedro Martins", "11122233344", "joao@email.com", "61999990001", "Brasília - DF"),
        ("Maria Clara Rocha", "22233344455", "maria@email.com", "61999990002", "Sobradinho - DF"),
        ("Lucas Ferreira", "33344455566", "lucas@email.com", "61999990003", "Planaltina - DF"),
        ("Fernanda Alves", "44455566677", "fernanda@email.com", "61999990004", "Taguatinga - DF"),
        ("Rafael Gomes", "55566677788", "rafael@email.com", "61999990005", "Ceilândia - DF"),
        ("Camila Ribeiro", "66677788899", "camila@email.com", "61999990006", "Águas Claras - DF"),
        ("Pedro Henrique", "77788899900", "pedro@email.com", "61999990007", "Guará - DF"),
        ("Juliana Mendes", "88899900011", "juliana@email.com", "61999990008", "Lago Norte - DF"),
    ]

    clientes = []

    for nome, cpf, email, telefone, endereco in clientes_dados:
        cliente, _ = Cliente.objects.get_or_create(
            cpf=cpf,
            defaults={
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "endereco": endereco,
            }
        )
        clientes.append(cliente)

    return clientes


def criar_produtos():
    produtos_dados = [
        ("Caderno Universitário 10 Matérias", "Caderno capa dura 200 folhas", "CAD001", 24.90, 120, 20),
        ("Caneta Azul BIC", "Caneta esferográfica azul", "CAN001", 2.50, 300, 50),
        ("Caneta Preta BIC", "Caneta esferográfica preta", "CAN002", 2.50, 250, 50),
        ("Lápis HB Faber-Castell", "Lápis grafite escolar", "LAP001", 1.80, 200, 40),
        ("Borracha Branca", "Borracha escolar macia", "BOR001", 2.00, 180, 30),
        ("Apontador Simples", "Apontador plástico escolar", "APO001", 1.50, 150, 30),
        ("Estojo Escolar", "Estojo com zíper", "EST001", 18.90, 80, 15),
        ("Mochila Escolar", "Mochila reforçada", "MOC001", 89.90, 40, 8),
        ("Resma A4", "Papel sulfite A4 500 folhas", "PAP001", 29.90, 70, 10),
        ("Marca Texto Amarelo", "Caneta marca texto", "MAR001", 4.90, 110, 20),
        ("Cola Branca 90g", "Cola escolar branca", "COL001", 5.50, 90, 15),
        ("Tesoura Escolar", "Tesoura sem ponta", "TES001", 7.90, 60, 10),
        ("Régua 30cm", "Régua transparente", "REG001", 3.50, 100, 20),
        ("Pasta Catálogo", "Pasta catálogo com plásticos", "PAS001", 22.90, 50, 8),
        ("Grampeador Pequeno", "Grampeador escolar", "GRA001", 16.90, 35, 5),
    ]

    produtos = []

    for nome, descricao, sku, preco, estoque, minimo in produtos_dados:
        produto, _ = Produto.objects.get_or_create(
            sku=sku,
            defaults={
                "nome": nome,
                "descricao": descricao,
                "preco": Decimal(str(preco)),
                "estoqueAtual": estoque,
                "estoqueMinimo": minimo,
                "ativo": True,
            }
        )
        produtos.append(produto)

    return produtos


def criar_vendas(clientes, produtos, funcionarios):
    status_opcoes = ["FINALIZADA", "FINALIZADA", "FINALIZADA", "PENDENTE", "CANCELADA"]

    for i in range(35):
        cliente = random.choice(clientes)
        funcionario = random.choice(funcionarios)
        status = random.choice(status_opcoes)

        venda = Venda.objects.create(
            cliente=cliente,
            usuario=funcionario,
            status=status,
            data=timezone.now() - timedelta(days=random.randint(0, 45)),
        )

        total = Decimal("0.00")
        produtos_da_venda = random.sample(produtos, random.randint(1, 4))

        for produto in produtos_da_venda:
            quantidade = random.randint(1, 8)
            subtotal = produto.preco * quantidade

            ItemVenda.objects.create(
                venda=venda,
                produto=produto,
                quantidade=quantidade,
                precoUnitario=produto.preco,
                subtotal=subtotal,
            )

            total += subtotal

            if status == "FINALIZADA":
                produto.estoqueAtual = max(0, produto.estoqueAtual - quantidade)
                produto.save()

        venda.total = total

        if status == "FINALIZADA":
            venda.finalizado_por = funcionario
            venda.data_finalizacao = venda.data + timedelta(minutes=random.randint(5, 90))

        if status == "CANCELADA":
            venda.cancelado_por = funcionario
            venda.data_cancelamento = venda.data + timedelta(minutes=random.randint(5, 90))

        venda.save()


def popular():
    print("Limpando banco...")

    ItemVenda.objects.all().delete()
    Venda.objects.all().delete()
    Produto.objects.all().delete()
    Cliente.objects.all().delete()
    Usuario.objects.exclude(is_superuser=True).delete()

    print("Criando usuários...")
    gerente, funcionarios = criar_usuarios()

    print("Criando clientes...")
    clientes = criar_clientes()

    print("Criando produtos...")
    produtos = criar_produtos()

    print("Criando vendas...")
    criar_vendas(clientes, produtos, funcionarios)

    print("Banco populado com sucesso!")
    print()
    print("Login gerente:")
    print("Usuário: gerente")
    print("Senha: 123456")
    print()
    print("Funcionários:")
    print("ana.souza / 123456")
    print("bruno.lima / 123456")
    print("mariana.costa / 123456")


if __name__ == "__main__":
    popular()