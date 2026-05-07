from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models.usuario import PerfilUsuario
from core.service import ClienteService, IAService, ProdutoService, RelatorioService, UsuarioService, VendaService


def tela_login(request):
    if request.method == 'POST':
        usuario = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password'),
        )
        if usuario:
            login(request, usuario)
            if usuario.perfil == PerfilUsuario.ADMIN:
                return redirect('/web/menu/admin/')
            return redirect('/web/menu/funcionario/')
        return render(request, 'login.html', {'erro': 'Usuário ou senha inválidos.'})
    return render(request, 'login.html')


def tela_logout(request):
    logout(request)
    return redirect('/web/login/')


@login_required(login_url='/web/login/')
def tela_menu(request):
    if request.user.perfil == PerfilUsuario.ADMIN:
        return redirect('/web/menu/admin/')
    return redirect('/web/menu/funcionario/')


@login_required(login_url='/web/login/')
def tela_menu_admin(request):
    if request.user.perfil != PerfilUsuario.ADMIN:
        return redirect('/web/menu/funcionario/')
    return render(request, 'menu_admin.html')


@login_required(login_url='/web/login/')
def tela_menu_funcionario(request):
    return render(request, 'menu_funcionario.html')


# --- Clientes ---

@login_required(login_url='/web/login/')
def tela_clientes(request):
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome'),
            'cpf': request.POST.get('cpf'),
            'email': request.POST.get('email'),
            'telefone': request.POST.get('telefone', ''),
            'endereco': request.POST.get('endereco', ''),
        }
        try:
            ClienteService().criar(dados)
            messages.success(request, 'Cliente cadastrado com sucesso.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('/web/clientes/')

    clientes = ClienteService().listar()
    return render(request, 'clientes.html', {'clientes': clientes})


@login_required(login_url='/web/login/')
def editar_cliente(request, cliente_id):
    try:
        cliente = ClienteService().buscar(cliente_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Cliente não encontrado.')
        return redirect('/web/clientes/')
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome'),
            'cpf': request.POST.get('cpf'),
            'email': request.POST.get('email'),
            'telefone': request.POST.get('telefone', ''),
            'endereco': request.POST.get('endereco', ''),
        }
        try:
            ClienteService().atualizar(cliente_id, dados)
            messages.success(request, 'Cliente atualizado com sucesso.')
            return redirect('/web/clientes/')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'editar_cliente.html', {'cliente': cliente})


@login_required(login_url='/web/login/')
def excluir_cliente(request, cliente_id):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Apenas administradores podem excluir clientes.')
        return redirect('/web/clientes/')
    try:
        ClienteService().excluir(cliente_id)
        messages.success(request, 'Cliente excluído com sucesso.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('/web/clientes/')


# --- Produtos ---

@login_required(login_url='/web/login/')
def tela_produtos(request):
    if request.method == 'POST':
        if request.user.perfil != PerfilUsuario.ADMIN:
            messages.error(request, 'Apenas administradores podem cadastrar produtos.')
            return redirect('/web/produtos/')
        try:
            dados = {
                'nome': request.POST.get('nome'),
                'descricao': request.POST.get('descricao', ''),
                'sku': request.POST.get('sku'),
                'preco': request.POST.get('preco'),
                'estoqueAtual': int(request.POST.get('estoqueAtual', 0)),
                'estoqueMinimo': int(request.POST.get('estoqueMinimo', 0)),
                'ativo': 'ativo' in request.POST,
            }
            ProdutoService().criar(dados)
            messages.success(request, 'Produto cadastrado com sucesso.')
        except (ValueError, TypeError):
            messages.error(request, 'Valores de estoque inválidos.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('/web/produtos/')

    produtos = ProdutoService().listar()
    return render(request, 'produtos.html', {'produtos': produtos})


@login_required(login_url='/web/login/')
def editar_produto(request, produto_id):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Apenas administradores podem editar produtos.')
        return redirect('/web/produtos/')
    try:
        produto = ProdutoService().buscar(produto_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Produto não encontrado.')
        return redirect('/web/produtos/')
    if request.method == 'POST':
        try:
            dados = {
                'nome': request.POST.get('nome'),
                'descricao': request.POST.get('descricao', ''),
                'sku': request.POST.get('sku'),
                'preco': request.POST.get('preco'),
                'estoqueAtual': int(request.POST.get('estoqueAtual', 0)),
                'estoqueMinimo': int(request.POST.get('estoqueMinimo', 0)),
                'ativo': 'ativo' in request.POST,
            }
            ProdutoService().atualizar(produto_id, dados)
            messages.success(request, 'Produto atualizado com sucesso.')
            return redirect('/web/produtos/')
        except (ValueError, TypeError):
            messages.error(request, 'Valores de estoque inválidos.')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'editar_produto.html', {'produto': produto})


@login_required(login_url='/web/login/')
def excluir_produto(request, produto_id):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Apenas administradores podem excluir produtos.')
        return redirect('/web/produtos/')
    try:
        ProdutoService().excluir(produto_id)
        messages.success(request, 'Produto excluído com sucesso.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('/web/produtos/')


# --- Vendas ---

@login_required(login_url='/web/login/')
def tela_vendas(request):
    if request.method == 'POST':
        try:
            produto_ids = request.POST.getlist('produto_ids')
            quantidades = request.POST.getlist('quantidades')
            itens = [
                {'produto_id': int(pid), 'quantidade': int(qtd)}
                for pid, qtd in zip(produto_ids, quantidades)
                if pid and qtd
            ]
            dados = {
                'cliente_id': int(request.POST.get('cliente_id')),
                'usuario_id': request.user.id,
                'itens': itens,
            }
            VendaService().criar(dados)
            messages.success(request, 'Venda registrada com sucesso.')
        except (ValueError, TypeError):
            messages.error(request, 'Dados de venda inválidos.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('/web/vendas/')

    vendas = VendaService().listar()
    clientes = ClienteService().listar()
    produtos = ProdutoService().listar()
    return render(request, 'vendas.html', {
        'vendas': vendas,
        'clientes': clientes,
        'produtos': produtos,
    })


@login_required(login_url='/web/login/')
def finalizar_venda(request, venda_id):
    try:
        VendaService().finalizar(venda_id)
        messages.success(request, 'Venda finalizada com sucesso.')
    except Exception as e:
        messages.error(request, str(e))
    return redirect('/web/vendas/')


# --- Análise IA ---

@login_required(login_url='/web/login/')
def tela_ia(request):
    service = IAService()
    return render(request, 'ia.html', {
        'mais_vendidos': service.analisar_mais_vendidos(),
        'menos_vendidos': service.analisar_menos_vendidos(),
        'parados': service.identificar_produtos_parados(),
    })


# --- Usuários (ADMIN only) ---

@login_required(login_url='/web/login/')
def tela_usuarios(request):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('/web/menu/')

    if request.method == 'POST':
        dados = {
            'username': request.POST.get('username'),
            'nome': request.POST.get('nome', ''),
            'email': request.POST.get('email', ''),
            'perfil': request.POST.get('perfil', PerfilUsuario.FUNCIONARIO),
            'ativo': 'ativo' in request.POST,
            'senha': request.POST.get('senha'),
        }
        try:
            UsuarioService().criar(dados)
            messages.success(request, 'Usuário criado com sucesso.')
        except Exception as e:
            messages.error(request, str(e))
        return redirect('/web/usuarios/')

    usuarios = UsuarioService().listar()
    return render(request, 'usuarios.html', {
        'usuarios': usuarios,
        'perfis': PerfilUsuario.choices,
    })


@login_required(login_url='/web/login/')
def editar_usuario(request, usuario_id):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('/web/menu/')

    try:
        usuario = UsuarioService().buscar(usuario_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('/web/usuarios/')
    if request.method == 'POST':
        dados = {
            'nome': request.POST.get('nome', ''),
            'email': request.POST.get('email', ''),
            'perfil': request.POST.get('perfil', PerfilUsuario.FUNCIONARIO),
            'ativo': 'ativo' in request.POST,
        }
        try:
            UsuarioService().atualizar(usuario_id, dados)
            messages.success(request, 'Usuário atualizado com sucesso.')
            return redirect('/web/usuarios/')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'editar_usuario.html', {
        'usuario': usuario,
        'perfis': PerfilUsuario.choices,
    })


@login_required(login_url='/web/login/')
def redefinir_senha(request, usuario_id):
    if request.user.perfil != PerfilUsuario.ADMIN:
        messages.error(request, 'Acesso restrito a administradores.')
        return redirect('/web/menu/')

    try:
        usuario = UsuarioService().buscar(usuario_id)
    except ObjectDoesNotExist:
        messages.error(request, 'Usuário não encontrado.')
        return redirect('/web/usuarios/')
    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha', '')
        try:
            UsuarioService().redefinir_senha(usuario_id, nova_senha)
            messages.success(request, 'Senha redefinida com sucesso.')
            return redirect('/web/usuarios/')
        except Exception as e:
            messages.error(request, str(e))
    return render(request, 'redefinir_senha.html', {'usuario': usuario})


# --- Relatórios ---

@login_required(login_url='/web/login/')
def tela_relatorios(request):
    inicio = request.GET.get('inicio', '')
    fim = request.GET.get('fim', '')
    cliente_id = request.GET.get('cliente_id', '')
    vendas = []
    erro = ''

    if inicio and fim:
        try:
            vendas = list(RelatorioService().vendas_por_periodo(inicio, fim))
        except Exception as e:
            erro = str(e)
    elif cliente_id:
        vendas = list(RelatorioService().vendas_por_cliente(cliente_id))

    total_vendido = sum(v.total for v in vendas)
    quantidade_vendas = len(vendas)

    produtos_vendidos = {}
    for venda in vendas:
        for item in venda.itens.select_related('produto'):
            nome = item.produto.nome
            produtos_vendidos[nome] = produtos_vendidos.get(nome, 0) + item.quantidade

    return render(request, 'relatorios.html', {
        'resultado': vendas,
        'inicio': inicio,
        'fim': fim,
        'cliente_id': cliente_id,
        'erro': erro,
        'total_vendido': total_vendido,
        'quantidade_vendas': quantidade_vendas,
        'produtos_vendidos': produtos_vendidos,
    })
