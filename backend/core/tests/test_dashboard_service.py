from decimal import Decimal

from django.test import TestCase

from core.models import Cliente, ItemVenda, Produto, StatusVenda, Usuario, Venda
from core.service.dashboard_service import DashboardService


class DashboardServiceTest(TestCase):

    def setUp(self):
        self.service = DashboardService()
        self.usuario = Usuario.objects.create_user(
            username='teste_dash', password='senha123', nome='Dashboard Teste',
        )
        self.cliente = Cliente.objects.create(
            cpf='55544433301', nome='Cliente Dashboard', email='dash@test.com',
        )
        self.produto_normal = Produto.objects.create(
            nome='Caneta', descricao='Caneta azul', sku='CAN_DASH',
            preco=Decimal('5.00'), estoqueAtual=20, estoqueMinimo=5, ativo=True,
        )
        self.produto_baixo = Produto.objects.create(
            nome='Borracha', descricao='Borracha branca', sku='BOR_DASH',
            preco=Decimal('2.00'), estoqueAtual=2, estoqueMinimo=5, ativo=True,
        )

    def _criar_venda(self, status, total='10.00'):
        return Venda.objects.create(
            cliente=self.cliente,
            usuario=self.usuario,
            total=Decimal(total),
            status=status,
        )

    # --- total do mês ---

    def test_total_mes_considera_apenas_finalizadas(self):
        self._criar_venda(StatusVenda.FINALIZADA, '100.00')
        dados = self.service.resumo()
        self.assertEqual(dados['total_mes'], Decimal('100.00'))

    def test_total_mes_nao_conta_canceladas(self):
        self._criar_venda(StatusVenda.FINALIZADA, '100.00')
        self._criar_venda(StatusVenda.CANCELADA, '50.00')
        dados = self.service.resumo()
        self.assertEqual(dados['total_mes'], Decimal('100.00'))

    def test_total_mes_nao_conta_pendentes(self):
        self._criar_venda(StatusVenda.PENDENTE, '200.00')
        dados = self.service.resumo()
        self.assertEqual(dados['total_mes'], Decimal('0'))

    def test_total_mes_soma_multiplas_finalizadas(self):
        self._criar_venda(StatusVenda.FINALIZADA, '100.00')
        self._criar_venda(StatusVenda.FINALIZADA, '50.00')
        dados = self.service.resumo()
        self.assertEqual(dados['total_mes'], Decimal('150.00'))

    # --- contagens ---

    def test_conta_vendas_pendentes(self):
        self._criar_venda(StatusVenda.PENDENTE)
        self._criar_venda(StatusVenda.PENDENTE)
        dados = self.service.resumo()
        self.assertEqual(dados['vendas_pendentes'], 2)

    def test_conta_vendas_canceladas(self):
        self._criar_venda(StatusVenda.CANCELADA)
        dados = self.service.resumo()
        self.assertEqual(dados['vendas_canceladas'], 1)

    def test_vendas_pendentes_nao_contam_canceladas(self):
        self._criar_venda(StatusVenda.PENDENTE)
        self._criar_venda(StatusVenda.CANCELADA)
        dados = self.service.resumo()
        self.assertEqual(dados['vendas_pendentes'], 1)
        self.assertEqual(dados['vendas_canceladas'], 1)

    # --- estoque baixo ---

    def test_identifica_produto_com_estoque_baixo(self):
        dados = self.service.resumo()
        self.assertGreaterEqual(dados['estoque_baixo_count'], 1)
        skus = [p.sku for p in dados['estoque_baixo']]
        self.assertIn('BOR_DASH', skus)

    def test_produto_estoque_normal_nao_aparece_em_baixo(self):
        dados = self.service.resumo()
        skus = [p.sku for p in dados['estoque_baixo']]
        self.assertNotIn('CAN_DASH', skus)

    # --- últimas vendas ---

    def test_lista_ultimas_vendas(self):
        for _ in range(3):
            self._criar_venda(StatusVenda.FINALIZADA)
        dados = self.service.resumo()
        self.assertEqual(len(dados['ultimas_vendas']), 3)

    def test_ultimas_vendas_limita_a_cinco(self):
        for _ in range(8):
            self._criar_venda(StatusVenda.FINALIZADA)
        dados = self.service.resumo()
        self.assertLessEqual(len(dados['ultimas_vendas']), 5)

    # --- mais vendidos ---

    def test_lista_produtos_mais_vendidos(self):
        venda = self._criar_venda(StatusVenda.FINALIZADA, '15.00')
        ItemVenda.objects.create(
            venda=venda,
            produto=self.produto_normal,
            quantidade=3,
            precoUnitario=Decimal('5.00'),
            subtotal=Decimal('15.00'),
        )
        dados = self.service.resumo()
        nomes = [item['produto__nome'] for item in dados['mais_vendidos']]
        self.assertIn('Caneta', nomes)

    def test_mais_vendidos_limita_a_cinco(self):
        for i in range(7):
            prod = Produto.objects.create(
                nome=f'Prod {i}', descricao='Desc', sku=f'SKU_MV_{i}',
                preco=Decimal('1.00'), estoqueAtual=100, estoqueMinimo=0,
            )
            venda = self._criar_venda(StatusVenda.FINALIZADA, '10.00')
            ItemVenda.objects.create(
                venda=venda, produto=prod,
                quantidade=i + 1,
                precoUnitario=Decimal('1.00'),
                subtotal=Decimal(str(i + 1)),
            )
        dados = self.service.resumo()
        self.assertLessEqual(len(dados['mais_vendidos']), 5)

    # --- menos vendidos ---

    def test_lista_produtos_menos_vendidos(self):
        venda = self._criar_venda(StatusVenda.FINALIZADA, '10.00')
        ItemVenda.objects.create(
            venda=venda, produto=self.produto_normal,
            quantidade=1, precoUnitario=Decimal('5.00'), subtotal=Decimal('5.00'),
        )
        dados = self.service.resumo()
        self.assertIn('menos_vendidos', dados)
        nomes = [item['produto__nome'] for item in dados['menos_vendidos']]
        self.assertIn('Caneta', nomes)

    # --- produtos parados ---

    def test_lista_produtos_parados(self):
        dados = self.service.resumo()
        self.assertIn('parados', dados)
        skus = [p.sku for p in dados['parados']]
        self.assertIn('CAN_DASH', skus)
        self.assertIn('BOR_DASH', skus)

    def test_produto_com_venda_nao_aparece_em_parados(self):
        venda = self._criar_venda(StatusVenda.FINALIZADA, '5.00')
        ItemVenda.objects.create(
            venda=venda, produto=self.produto_normal,
            quantidade=1, precoUnitario=Decimal('5.00'), subtotal=Decimal('5.00'),
        )
        dados = self.service.resumo()
        skus = [p.sku for p in dados['parados']]
        self.assertNotIn('CAN_DASH', skus)

    # --- sugestão de reposição ---

    def test_sugestao_reposicao_inclui_produto_baixo(self):
        dados = self.service.resumo()
        self.assertIn('sugestao_reposicao', dados)
        skus = [item['produto'].sku for item in dados['sugestao_reposicao']]
        self.assertIn('BOR_DASH', skus)

    def test_sugestao_reposicao_calcula_gap(self):
        dados = self.service.resumo()
        item = next(
            (i for i in dados['sugestao_reposicao'] if i['produto'].sku == 'BOR_DASH'), None
        )
        self.assertIsNotNone(item)
        # BOR_DASH: estoqueMinimo=5, estoqueAtual=2 → gap=3
        self.assertEqual(item['gap'], 3)

    def test_produto_estoque_ok_nao_entra_em_sugestao(self):
        dados = self.service.resumo()
        skus = [item['produto'].sku for item in dados['sugestao_reposicao']]
        self.assertNotIn('CAN_DASH', skus)

    # --- previsão de duração ---

    def test_previsao_duracao_retorna_chave(self):
        dados = self.service.resumo()
        self.assertIn('previsao_duracao', dados)

    def test_previsao_duracao_calcula_dias(self):
        venda = self._criar_venda(StatusVenda.FINALIZADA, '50.00')
        ItemVenda.objects.create(
            venda=venda, produto=self.produto_normal,
            quantidade=30, precoUnitario=Decimal('5.00'), subtotal=Decimal('150.00'),
        )
        dados = self.service.resumo()
        item = next(
            (i for i in dados['previsao_duracao'] if i['produto_sku'] == 'CAN_DASH'), None
        )
        self.assertIsNotNone(item)
        # estoqueAtual=20, media_diaria=30/30=1.0 → dias_restantes=20
        self.assertEqual(item['dias_restantes'], 20)

    def test_produto_parado_nao_aparece_em_previsao(self):
        # produto_baixo (BOR_DASH) não tem vendas → media_diaria=0 → não entra na previsão
        dados = self.service.resumo()
        skus = [i['produto_sku'] for i in dados['previsao_duracao']]
        self.assertNotIn('BOR_DASH', skus)

    # --- chaves do resumo ---

    def test_resumo_retorna_todas_as_chaves(self):
        dados = self.service.resumo()
        chaves_esperadas = [
            'vendas_do_dia', 'total_mes', 'produtos_cadastrados',
            'estoque_baixo_count', 'vendas_pendentes', 'vendas_canceladas',
            'ultimas_vendas', 'mais_vendidos', 'menos_vendidos', 'parados',
            'estoque_baixo', 'sugestao_reposicao', 'previsao_duracao',
        ]
        for chave in chaves_esperadas:
            self.assertIn(chave, dados, msg=f'Chave ausente: {chave}')
