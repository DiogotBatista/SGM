from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from movimentacoes.models import MovimentoItem
from .forms import RelatorioObraForm, RelatorioContratoForm, RelatorioDataForm, RelatorioMaterialForm

@login_required
def painel_relatorios(request):
    tipo = request.GET.get('tipo_relatorio')
    itens = None
    form = None
    page_obj = None
    consulta_realizada = False

    if tipo == 'obra':
        form = RelatorioObraForm(request.GET)
        if form.is_valid():
            obra = form.cleaned_data['obra']
            itens = MovimentoItem.objects.filter(
                movimentacao__obra=obra,
                tipo='SAI'
            ).select_related('material', 'movimentacao', 'movimentacao__obra', 'movimentacao__obra__contrato')
            consulta_realizada = True

    elif tipo == 'contrato':
        form = RelatorioContratoForm(request.GET)
        if form.is_valid():
            contrato = form.cleaned_data['contrato']
            itens = MovimentoItem.objects.filter(
                movimentacao__obra__contrato=contrato,
                tipo='SAI'
            ).select_related('material', 'movimentacao', 'movimentacao__obra', 'movimentacao__obra__contrato')
            consulta_realizada = True

    elif tipo == 'data':
        form = RelatorioDataForm(request.GET)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            itens = MovimentoItem.objects.filter(
                movimentacao__data_movimentacao__date__range=(data_inicio, data_fim)
            ).select_related('material', 'movimentacao', 'movimentacao__obra', 'movimentacao__obra__contrato')
            consulta_realizada = True

    elif tipo == 'material':
        form = RelatorioMaterialForm(request.GET)
        if form.is_valid():
            material = form.cleaned_data['material']
            tipo_mov = form.cleaned_data.get('tipo')
            itens = MovimentoItem.objects.filter(material=material)
            if tipo_mov:
                itens = itens.filter(tipo=tipo_mov)
            itens = itens.select_related('movimentacao', 'movimentacao__obra', 'movimentacao__obra__contrato')
            consulta_realizada = True

    if itens is not None:
        paginator = Paginator(itens, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    if 'page' in query_params:
        del query_params['page']

    context = {
        'tipo': tipo,
        'form': form,
        'page_obj': page_obj,
        'consulta_realizada': consulta_realizada,
        'query_params': query_params.urlencode(),
        'total_resultados': itens.count() if itens is not None else 0,
        'mostrar_tipo': tipo == 'data' or tipo == 'material',
        'mostrar_obra_contrato': tipo == 'material',
    }
    return render(request, 'relatorios/painel.html', context)