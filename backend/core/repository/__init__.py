from .cliente_repository import ClienteRepository
from .dashboard_repository import DashboardRepository
from .ia_repository import IARepository
from .produto_repository import ProdutoRepository
from .relatorio_avancado_repository import RelatorioAvancadoRepository
from .relatorio_repository import RelatorioRepository
from .usuario_repository import UsuarioRepository
from .venda_repository import VendaRepository

__all__ = [
    'ClienteRepository', 'DashboardRepository', 'IARepository',
    'ProdutoRepository', 'RelatorioAvancadoRepository', 'RelatorioRepository',
    'UsuarioRepository', 'VendaRepository',
]
