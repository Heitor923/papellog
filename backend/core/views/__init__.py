from .cliente_view import ClienteDetailView, ClienteListView
from .ia_view import IAMaisVendidosView, IAMenosVendidosView, IAProdutosParadosView
from .produto_view import ProdutoDetailView, ProdutoListView
from .relatorio_view import RelatorioVendaClienteView, RelatorioVendaPeriodoView
from .venda_view import VendaCancelarView, VendaDetailView, VendaFinalizarView, VendaListView

__all__ = [
    'ClienteListView', 'ClienteDetailView',
    'ProdutoListView', 'ProdutoDetailView',
    'VendaListView', 'VendaDetailView', 'VendaFinalizarView', 'VendaCancelarView',
    'RelatorioVendaPeriodoView', 'RelatorioVendaClienteView',
    'IAMaisVendidosView', 'IAMenosVendidosView', 'IAProdutosParadosView',
]
