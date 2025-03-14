from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Contratante, Contrato
from .forms import ContratanteForm, ContratoForm
from usuarios.mixins import GestorOrSuperuserRequiredMixin
from django.db.models import Q

class MenuView(LoginRequiredMixin, TemplateView):
    template_name = 'configuracoes/menu.html'

# VIEWS DOS CONTRATANTES
class ContratanteListView(LoginRequiredMixin, ListView):
    model = Contratante
    template_name = 'configuracoes/contratantes/lista_contratante.html'
    context_object_name = 'contratantes'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(cnpj__icontains=query)
            )
        return queryset

class ContratanteCreateView(GestorOrSuperuserRequiredMixin, CreateView):
    model = Contratante
    form_class = ContratanteForm
    template_name = 'configuracoes/contratantes/cadastrar_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Empresa cadastrada com sucesso!")
        return super().form_valid(form)

class ContratanteUpdateView(GestorOrSuperuserRequiredMixin, UpdateView):
    model = Contratante
    form_class = ContratanteForm
    template_name = 'configuracoes/contratantes/editar_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)

class ContratanteDeleteView(GestorOrSuperuserRequiredMixin, DeleteView):
    model = Contratante
    template_name = 'configuracoes/contratantes/excluir_contratante.html'
    success_url = reverse_lazy('lista_contratantes')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Empresa excluída com sucesso!")
        return response


# VIEWS DOS CONTRATOS
class ContratosListView(LoginRequiredMixin, ListView):
    model = Contrato
    template_name = 'configuracoes/contratos/lista_contratos.html'
    context_object_name = 'contratos'
    paginate_by = 10
    ordering = ['id']

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(numero__icontains=query) |
                Q(contratante__nome__icontains=query)
            )
        return queryset

class ContratosCreateView(GestorOrSuperuserRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'configuracoes/contratos/cadastrar_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.updated_by = self.request.user
        messages.success(self.request, "Contrato cadastrado com sucesso!")
        return super().form_valid(form)

class ContratoUpdateView(GestorOrSuperuserRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'configuracoes/contratos/editar_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        messages.success(self.request, "Contrato atualizado com sucesso!")
        return super().form_valid(form)

class ContratoDeleteView(GestorOrSuperuserRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'configuracoes/contratos/excluir_contratos.html'
    success_url = reverse_lazy('lista_contratos')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Contrato excluído com sucesso!")
        return response


# VIEWS DAS OBRAS

