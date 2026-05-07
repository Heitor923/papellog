from .cliente_view import ClienteDetailView, ClienteListView
from .ia_view import IAMaisVendidosView, IAMenosVendidosView, IAProdutosParadosView
from .produto_view import ProdutoDetailView, ProdutoListView
from .relatorio_view import RelatorioVendaClienteView, RelatorioVendaPeriodoView
from .venda_view import VendaDetailView, VendaFinalizarView, VendaListView

__all__ = [
    'ClienteListView', 'ClienteDetailView',
    'IAMaisVendidosView', 'IAMenosVendidosView', 'IAProdutosParadosView',
    'ProdutoListView', 'ProdutoDetailView',
    'VendaListView', 'VendaDetailView', 'VendaFinalizarView',
    'RelatorioVendaPeriodoView', 'RelatorioVendaClienteView',
]
