from django.urls import path
from .views import RelatorioMovimentacoesView, RelatoriosDashboardView

urlpatterns = [
    path('', RelatoriosDashboardView.as_view(), name='dashboard_relatorios'),
    path('movimentacoes/', RelatorioMovimentacoesView.as_view(), name='relatorio_movimentacoes'),
    # path('materiais/', RelatorioMateriaisView.as_view(), name='relatorio_materiais'),
]


