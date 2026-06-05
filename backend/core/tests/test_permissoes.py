from decimal import Decimal

from django.test import Client, TestCase

from core.models import Cliente, Produto, Usuario


class PermissoesWebTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin = Usuario.objects.create_user(
            username='admin_test', password='senha123', nome='Admin Teste',
            perfil='ADMIN',
        )
        self.funcionario = Usuario.objects.create_user(
            username='func_test', password='senha123', nome='Func Teste',
            perfil='FUNCIONARIO',
        )
        self.cliente_obj = Cliente.objects.create(
            cpf='99988877701', nome='Cliente Permissao', email='perm@test.com',
        )
        self.produto_obj = Produto.objects.create(
            nome='Produto Permissao', descricao='Desc', sku='SKU_PERM',
            preco=Decimal('10.00'), estoqueAtual=10, estoqueMinimo=1,
        )

    # --- Acesso sem autenticação ---

    def test_sem_login_clientes_redireciona(self):
        response = self.client.get('/web/clientes/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/web/login/', response['Location'])

    def test_sem_login_vendas_redireciona(self):
        response = self.client.get('/web/vendas/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/web/login/', response['Location'])

    def test_sem_login_usuarios_redireciona(self):
        response = self.client.get('/web/usuarios/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/web/login/', response['Location'])

    # --- Exclusão de cliente ---

    def test_funcionario_nao_pode_excluir_cliente(self):
        self.client.login(username='func_test', password='senha123')
        self.client.post(f'/web/clientes/{self.cliente_obj.id}/excluir/')
        self.assertTrue(Cliente.objects.filter(id=self.cliente_obj.id).exists())

    def test_admin_pode_excluir_cliente(self):
        self.client.login(username='admin_test', password='senha123')
        self.client.post(f'/web/clientes/{self.cliente_obj.id}/excluir/')
        self.assertFalse(Cliente.objects.filter(id=self.cliente_obj.id).exists())

    def test_excluir_cliente_via_get_nao_deleta(self):
        self.client.login(username='admin_test', password='senha123')
        self.client.get(f'/web/clientes/{self.cliente_obj.id}/excluir/')
        self.assertTrue(Cliente.objects.filter(id=self.cliente_obj.id).exists())

    # --- Exclusão de produto ---

    def test_funcionario_nao_pode_excluir_produto(self):
        self.client.login(username='func_test', password='senha123')
        self.client.post(f'/web/produtos/{self.produto_obj.id}/excluir/')
        self.assertTrue(Produto.objects.filter(id=self.produto_obj.id).exists())

    def test_admin_pode_excluir_produto(self):
        self.client.login(username='admin_test', password='senha123')
        self.client.post(f'/web/produtos/{self.produto_obj.id}/excluir/')
        self.assertFalse(Produto.objects.filter(id=self.produto_obj.id).exists())

    def test_excluir_produto_via_get_nao_deleta(self):
        self.client.login(username='admin_test', password='senha123')
        self.client.get(f'/web/produtos/{self.produto_obj.id}/excluir/')
        self.assertTrue(Produto.objects.filter(id=self.produto_obj.id).exists())

    # --- Tela de usuários (ADMIN only) ---

    def test_funcionario_nao_acessa_tela_usuarios(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/usuarios/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/web/menu/')

    def test_admin_acessa_tela_usuarios(self):
        self.client.login(username='admin_test', password='senha123')
        response = self.client.get('/web/usuarios/')
        self.assertEqual(response.status_code, 200)

    # --- Edição de produto (ADMIN only) ---

    def test_funcionario_nao_pode_editar_produto(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get(f'/web/produtos/{self.produto_obj.id}/editar/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/web/produtos/')

    def test_admin_pode_acessar_edicao_produto(self):
        self.client.login(username='admin_test', password='senha123')
        response = self.client.get(f'/web/produtos/{self.produto_obj.id}/editar/')
        self.assertEqual(response.status_code, 200)

    # --- Edição de usuário (ADMIN only) ---

    def test_funcionario_nao_pode_editar_usuario(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get(f'/web/usuarios/{self.funcionario.id}/editar/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], '/web/menu/')

    def test_admin_pode_acessar_edicao_usuario(self):
        self.client.login(username='admin_test', password='senha123')
        response = self.client.get(f'/web/usuarios/{self.funcionario.id}/editar/')
        self.assertEqual(response.status_code, 200)

    # --- Telas acessíveis para funcionário ---

    def test_funcionario_acessa_clientes(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/clientes/')
        self.assertEqual(response.status_code, 200)

    def test_funcionario_acessa_produtos(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/produtos/')
        self.assertEqual(response.status_code, 200)

    def test_funcionario_acessa_vendas(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/vendas/')
        self.assertEqual(response.status_code, 200)

    def test_funcionario_acessa_relatorios(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/relatorios/')
        self.assertEqual(response.status_code, 200)

    def test_funcionario_acessa_ia(self):
        self.client.login(username='func_test', password='senha123')
        response = self.client.get('/web/ia/')
        self.assertEqual(response.status_code, 200)
