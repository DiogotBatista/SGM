import django_filters
from movimentacoes.models import Movimentacao

class MovimentoFilter(django_filters.FilterSet):
    contrato = django_filters.NumberFilter(
        field_name='contrato__id',
        lookup_expr='exact',
        label="Contrato"
    )
    obra = django_filters.NumberFilter(
        field_name='obra__id',
        lookup_expr='exact',
        label="Obra"
    )

    class Meta:
        model = Movimentacao
        fields = ['contrato', 'obra']
