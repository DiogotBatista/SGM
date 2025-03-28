from django_filters.views import FilterView
from movimentacoes.models import Movimentacao
from .filters import MovimentoFilter
from django.views.generic import  TemplateView
from usuarios.mixins import AccessRequiredMixin

class RelatorioMovimentacoesView(FilterView):
    model = Movimentacao
    template_name = 'relatorios/relatorio_movimentacoes.html'
    context_object_name = 'movimentacoes'
    filterset_class = MovimentoFilter
    paginate_by = 10


class RelatoriosDashboardView(AccessRequiredMixin, TemplateView):
    allowed_roles = []
    template_name = 'relatorios/dashboard_relatorios.html'