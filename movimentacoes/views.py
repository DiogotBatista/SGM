from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.contrib import messages
from usuarios.mixins import AccessRequiredMixin
from .models import Movimentacao, MovimentoItem
from django.forms import inlineformset_factory
from .forms import MovimentoItemEntradaForm, MovimentoItemSaidaForm, MovimentacaoSaidaForm, MovimentacaoEntradaForm

class MovimentacoesDashboardView(AccessRequiredMixin, TemplateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    template_name = 'movimentacoes/dashboard_movimentacoes.html'

class MovimentoListView(AccessRequiredMixin, ListView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    template_name = 'movimentacoes/lista_movimentacoes.html'
    context_object_name = 'movimentacoes'
    paginate_by = 10
    ordering = ['-data_movimentacao']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        # Ajuste o filtro conforme necessário, por exemplo, por obra, etc.
        if query:
            queryset = queryset.filter(obra__nome__icontains=query)
        return queryset

class MovimentoDetailView(AccessRequiredMixin, DetailView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    template_name = 'movimentacoes/detalhe_movimentacoes.html'
    context_object_name = 'movimentacao'


MovimentoItemEntradaFormSet = inlineformset_factory(
    Movimentacao,
    MovimentoItem,
    form=MovimentoItemEntradaForm,
    extra=1,
    can_delete=False
)

class MovimentacaoEntradaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    form_class = MovimentacaoEntradaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_entrada.html'
    success_url = reverse_lazy('lista_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = MovimentoItemEntradaFormSet(self.request.POST, prefix='form')
        else:
            context['formset'] = MovimentoItemEntradaFormSet(prefix='form')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Atribui o usuário logado como quem realizou a movimentação
        form.instance.realizado_por = self.request.user
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            # Se o formset não for válido, renderize novamente o formulário com erros
            return self.form_invalid(form)
        messages.success(self.request, "Movimentação de entrada registrada com sucesso.")
        return super().form_valid(form)

MovimentoItemSaidaFormSet = inlineformset_factory(
    Movimentacao,
    MovimentoItem,
    form=MovimentoItemSaidaForm,
    extra=1,
    can_delete=False
)

class MovimentacaoSaidaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    form_class = MovimentacaoSaidaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_saida.html'
    success_url = reverse_lazy('lista_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = MovimentoItemSaidaFormSet(self.request.POST, prefix='form')
        else:
            context['formset'] = MovimentoItemSaidaFormSet(prefix='form')
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        # Atribui o usuário logado como quem realizou a movimentação
        form.instance.realizado_por = self.request.user
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        else:
            return self.form_invalid(form)
        messages.success(self.request, "Movimentação de saída registrada com sucesso.")
        return super().form_valid(form)




