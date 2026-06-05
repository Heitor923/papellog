from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from core.models import Cliente, ItemVenda, Produto, StatusVenda, Usuario, Venda
from core.service.relatorio_avancado_service import RelatorioAvancadoService


class RelatorioAvancadoServiceTest(TestCase):

    def setUp(self):
        self.service = RelatorioAvancadoService()

        self.func1 = Usuario.objects.create_user(
            username='func1_avancado', password='senha', nome='Func Um',
        )
        self.func2 = Usuario.objects.create_user(
            username='func2_avancado', password='senha', nome='Func Dois',
        )
        self.cliente1 = Cliente.objects.create(
            cpf='11122200011', nome='Cliente Um', email='c1@test.com',
        )
        self.cliente2 = Cliente.objects.create(
            cpf='22233300022', nome='Cliente Dois', email='c2@test.com',
        )
        self.produto1 = Produto.objects.create(
            nome='Caneta', descricao='Caneta azul', sku='CAN_AV',
            preco=Decimal('5.00'), estoqueAtual=20, estoqueMinimo=5, ativo=True,
        )
        self.produto2 = Produto.objects.create(
            nome='Caderno', descricao='Caderno 200f', sku='CAD_AV',
            preco=Decimal('20.00'), estoqueAtual=2, estoqueMinimo=5, ativo=True,
        )

    def _criar_venda(self, usuario, cliente, status, total, itens=None):
        venda = Venda.objects.create(
            cliente=cliente,
            usuario=usuario,
            total=Decimal(str(total)),
            status=status,
        )
        if itens:
            for produto, qtd, preco in itens:
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=qtd,
                    precoUnitario=Decimal(str(preco)),
                    subtotal=Decimal(str(qtd * preco)),
                )
        return venda

    def _mover_para_passado(self, venda, dias):
        data_passado = timezone.now() - timedelta(days=dias)
        Venda.objects.filter(pk=venda.pk).update(data=data_passado)

    # --- filtro por período ---

    def test_filtro_por_periodo_inclui_vendas_no_intervalo(self):
        venda_hoje = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '50.00')
        venda_antiga = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '30.00')
        self._mover_para_passado(venda_antiga, 60)

        hoje = timezone.localdate()
        inicio = (hoje - timedelta(days=7)).strftime('%Y-%m-%d')
        fim = hoje.strftime('%Y-%m-%d')

        dados = self.service.gerar({'data_inicio': inicio, 'data_fim': fim})
        ids = [v.id for v in dados['vendas']]

        self.assertIn(venda_hoje.id, ids)
        self.assertNotIn(venda_antiga.id, ids)

    def test_filtro_por_periodo_exclui_vendas_fora_do_intervalo(self):
        venda_antiga = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '30.00')
        self._mover_para_passado(venda_antiga, 60)

        hoje = timezone.localdate()
        inicio = (hoje - timedelta(days=7)).strftime('%Y-%m-%d')
        fim = hoje.strftime('%Y-%m-%d')

        dados = self.service.gerar({'data_inicio': inicio, 'data_fim': fim})
        ids = [v.id for v in dados['vendas']]

        self.assertNotIn(venda_antiga.id, ids)

    # --- filtro por cliente ---

    def test_filtro_por_cliente_retorna_apenas_vendas_do_cliente(self):
        v1 = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '50.00')
        v2 = self._criar_venda(self.func1, self.cliente2, StatusVenda.FINALIZADA, '30.00')

        dados = self.service.gerar({'cliente_id': str(self.cliente1.id)})
        ids = [v.id for v in dados['vendas']]

        self.assertIn(v1.id, ids)
        self.assertNotIn(v2.id, ids)

    def test_filtro_por_cliente_nao_retorna_vendas_de_outros(self):
        self._criar_venda(self.func1, self.cliente2, StatusVenda.FINALIZADA, '30.00')

        dados = self.service.gerar({'cliente_id': str(self.cliente1.id)})
        self.assertEqual(dados['quantidade_vendas'], 0)

    # --- filtro por funcionário ---

    def test_filtro_por_funcionario_retorna_vendas_do_usuario(self):
        v1 = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '50.00')
        v2 = self._criar_venda(self.func2, self.cliente1, StatusVenda.FINALIZADA, '30.00')

        dados = self.service.gerar({'usuario_id': str(self.func1.id)})
        ids = [v.id for v in dados['vendas']]

        self.assertIn(v1.id, ids)
        self.assertNotIn(v2.id, ids)

    # --- filtro por status ---

    def test_filtro_por_status_finalizada(self):
        v_fin = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '50.00')
        v_pen = self._criar_venda(self.func1, self.cliente1, StatusVenda.PENDENTE, '30.00')

        dados = self.service.gerar({'status': 'FINALIZADA'})
        ids = [v.id for v in dados['vendas']]

        self.assertIn(v_fin.id, ids)
        self.assertNotIn(v_pen.id, ids)

    def test_filtro_por_status_cancelada(self):
        v_can = self._criar_venda(self.func1, self.cliente1, StatusVenda.CANCELADA, '50.00')
        v_fin = self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '30.00')

        dados = self.service.gerar({'status': 'CANCELADA'})
        ids = [v.id for v in dados['vendas']]

        self.assertIn(v_can.id, ids)
        self.assertNotIn(v_fin.id, ids)

    # --- cálculo de total vendido ---

    def test_total_vendido_soma_apenas_finalizadas(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '100.00')
        self._criar_venda(self.func1, self.cliente1, StatusVenda.CANCELADA, '50.00')
        self._criar_venda(self.func1, self.cliente1, StatusVenda.PENDENTE, '30.00')

        dados = self.service.gerar({})
        self.assertEqual(dados['total_vendido'], Decimal('100.00'))

    def test_total_vendido_sem_finalizadas_e_zero(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.PENDENTE, '50.00')

        dados = self.service.gerar({})
        self.assertEqual(dados['total_vendido'], Decimal('0'))

    # --- cálculo de ticket médio ---

    def test_ticket_medio_calculado_corretamente(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '100.00')
        self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '60.00')

        dados = self.service.gerar({})
        # ticket_medio = 160 / 2 = 80.00
        self.assertEqual(dados['ticket_medio'], Decimal('80.00'))

    def test_ticket_medio_zero_sem_finalizadas(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.PENDENTE, '50.00')

        dados = self.service.gerar({})
        self.assertEqual(dados['ticket_medio'], Decimal('0'))

    # --- ranking de produtos ---

    def test_ranking_produtos_ordenado_por_valor(self):
        venda = self._criar_venda(
            self.func1, self.cliente1, StatusVenda.FINALIZADA, '115.00',
            itens=[
                (self.produto1, 3, 5.00),   # subtotal 15
                (self.produto2, 5, 20.00),  # subtotal 100
            ],
        )
        dados = self.service.gerar({})
        ranking = dados['ranking_produtos']

        self.assertGreaterEqual(len(ranking), 2)
        self.assertEqual(ranking[0]['produto__sku'], 'CAD_AV')   # maior valor
        self.assertEqual(ranking[1]['produto__sku'], 'CAN_AV')

    def test_ranking_produtos_considera_apenas_finalizadas(self):
        self._criar_venda(
            self.func1, self.cliente1, StatusVenda.PENDENTE, '15.00',
            itens=[(self.produto1, 3, 5.00)],
        )
        dados = self.service.gerar({})
        self.assertEqual(len(dados['ranking_produtos']), 0)

    # --- ranking de funcionários ---

    def test_ranking_funcionarios_ordenado_por_valor(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '200.00')
        self._criar_venda(self.func2, self.cliente1, StatusVenda.FINALIZADA, '50.00')

        dados = self.service.gerar({})
        ranking = dados['ranking_funcionarios']

        self.assertGreaterEqual(len(ranking), 2)
        self.assertEqual(ranking[0]['usuario__username'], 'func1_avancado')

    def test_ranking_funcionarios_conta_vendas_corretamente(self):
        self._criar_venda(self.func1, self.cliente1, StatusVenda.FINALIZADA, '100.00')
        self._criar_venda(self.func1, self.cliente2, StatusVenda.FINALIZADA, '80.00')

        dados = self.service.gerar({})
        func1_entry = next(
            (r for r in dados['ranking_funcionarios'] if r['usuario__username'] == 'func1_avancado'),
            None,
        )
        self.assertIsNotNone(func1_entry)
        self.assertEqual(func1_entry['quantidade_vendas'], 2)

    # --- produtos críticos ---

    def test_produtos_criticos_identifica_estoque_baixo(self):
        dados = self.service.gerar({})
        # produto2 (CAD_AV): estoqueAtual=2 <= estoqueMinimo=5
        skus_criticos = [item['produto'].sku for item in dados['produtos_criticos']]
        self.assertIn('CAD_AV', skus_criticos)

    def test_produtos_criticos_nao_inclui_estoque_ok(self):
        dados = self.service.gerar({})
        # produto1 (CAN_AV): estoqueAtual=20 > estoqueMinimo=5
        skus_criticos = [item['produto'].sku for item in dados['produtos_criticos']]
        self.assertNotIn('CAN_AV', skus_criticos)

    def test_produtos_criticos_calcula_diferenca(self):
        dados = self.service.gerar({})
        item = next(
            (i for i in dados['produtos_criticos'] if i['produto'].sku == 'CAD_AV'), None
        )
        self.assertIsNotNone(item)
        # CAD_AV: estoqueMinimo=5, estoqueAtual=2 → diferenca=3
        self.assertEqual(item['diferenca'], 3)

    # --- estrutura do retorno ---

    def test_estrutura_do_retorno_contem_todas_as_chaves(self):
        dados = self.service.gerar({})
        chaves_esperadas = [
            'filtros', 'vendas', 'total_vendido', 'quantidade_vendas',
            'ticket_medio', 'quantidade_canceladas', 'quantidade_pendentes',
            'ranking_produtos', 'ranking_funcionarios', 'produtos_criticos',
        ]
        for chave in chaves_esperadas:
            self.assertIn(chave, dados, msg=f'Chave ausente: {chave}')

    def test_data_inicio_maior_que_fim_levanta_erro(self):
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            self.service.gerar({
                'data_inicio': '2026-01-31',
                'data_fim': '2026-01-01',
            })
