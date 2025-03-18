from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from usuarios.mixins import AccessRequiredMixin
from .models import Movimentacao, MovimentoItem
from django.forms import inlineformset_factory
from .forms import (
    MovimentoItemEntradaForm,
    MovimentoItemSaidaForm,
    MovimentacaoSaidaForm,
    MovimentacaoEntradaForm,
    MovimentoItemSaidaFormSet  # Importamos o formset customizado do forms.py
)

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
        if query:
            queryset = queryset.filter(
                Q(obra__codigo__icontains=query) |
                Q(codigo__icontains=query)
            )
        return queryset


class MovimentoDetailView(AccessRequiredMixin, DetailView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    template_name = 'movimentacoes/detalhe_movimentacoes.html'
    context_object_name = 'movimentacao'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        itens_list = self.object.itens.all()  # 'itens' é o related_name definido no MovimentoItem
        paginator = Paginator(itens_list, 10)  # 10 itens por página
        page = self.request.GET.get('page')
        try:
            itens_paginated = paginator.page(page)
        except PageNotAnInteger:
            itens_paginated = paginator.page(1)
        except EmptyPage:
            itens_paginated = paginator.page(paginator.num_pages)
        context['itens_paginated'] = itens_paginated
        return context


# Formset para movimentação de entrada (sem customização adicional)
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
    success_url = reverse_lazy('dashboard_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            context['formset'] = MovimentoItemEntradaFormSet(self.request.POST, prefix='form')
        else:
            context['formset'] = MovimentoItemEntradaFormSet(prefix='form')
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context.get('formset')
        form.instance.realizado_por = self.request.user

        # Cria o objeto principal sem salvar no BD
        self.object = form.save(commit=False)

        # Verifica se o formset é válido antes de salvar o objeto principal
        if formset.is_valid():
            with transaction.atomic():
                self.object.save()  # Agora o objeto é salvo
                formset.instance = self.object
                formset.save()
            messages.success(self.request, "Movimentação de entrada registrada com sucesso.")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        formset = context.get('formset')
        errors = []
        if formset:
            # Captura erros gerais do formset
            errors.extend(formset.non_form_errors())
            # Captura erros dos campos individuais de cada formulário do formset
            for form_item in formset:
                for field in form_item:
                    if field.errors:
                        errors.extend(field.errors)
        if errors:
            from django.contrib import messages
            messages.warning(self.request, "Erro(s): " + " ".join(errors))
        return self.render_to_response(context)


class MovimentacaoSaidaCreateView(AccessRequiredMixin, CreateView):
    allowed_roles = ['Gestor', 'Almoxarife', 'Operador']
    model = Movimentacao
    form_class = MovimentacaoSaidaForm
    template_name = 'movimentacoes/cadastrar_movimentacao_saida.html'
    success_url = reverse_lazy('dashboard_movimentacoes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == "POST":
            # Aqui usamos o formset customizado que já valida se o saldo é suficiente
            context['formset'] = MovimentoItemSaidaFormSet(self.request.POST, prefix='form')
        else:
            context['formset'] = MovimentoItemSaidaFormSet(prefix='form')
        return context

    def form_valid(self, form):
        context = self.get_context_data(form=form)
        formset = context.get('formset')
        form.instance.realizado_por = self.request.user

        # Cria o objeto principal sem salvar imediatamente
        self.object = form.save(commit=False)

        if formset.is_valid():
            with transaction.atomic():
                self.object.save()
                formset.instance = self.object
                formset.save()
            messages.success(self.request, "Movimentação de saída registrada com sucesso.")
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        formset = context.get('formset')
        errors = []
        if formset:
            # Captura erros gerais do formset
            errors.extend(formset.non_form_errors())
            # Captura erros dos campos individuais de cada formulário do formset
            for form_item in formset:
                for field in form_item:
                    if field.errors:
                        errors.extend(field.errors)
        if errors:
            from django.contrib import messages
            messages.warning(self.request, "Erro(s): " + " ".join(errors))
        return self.render_to_response(context)
