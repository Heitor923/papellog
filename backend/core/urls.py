from django.urls import path

from core.views import (
    ClienteDetailView,
    ClienteListView,
    ProdutoDetailView,
    ProdutoListView,
    RelatorioVendaClienteView,
    RelatorioVendaPeriodoView,
    VendaDetailView,
    VendaFinalizarView,
    VendaListView,
)

urlpatterns = [
    path('clientes', ClienteListView.as_view(), name='cliente-list'),
    path('clientes/<int:id>', ClienteDetailView.as_view(), name='cliente-detail'),
    path('produtos', ProdutoListView.as_view(), name='produto-list'),
    path('produtos/<int:id>', ProdutoDetailView.as_view(), name='produto-detail'),
    path('vendas', VendaListView.as_view(), name='venda-list'),
    path('vendas/<int:id>', VendaDetailView.as_view(), name='venda-detail'),
    path('vendas/<int:id>/finalizar', VendaFinalizarView.as_view(), name='venda-finalizar'),
    path('relatorios/vendas/periodo', RelatorioVendaPeriodoView.as_view(), name='relatorio-periodo'),
    path('relatorios/vendas/cliente/<int:cliente_id>', RelatorioVendaClienteView.as_view(), name='relatorio-cliente'),
]
