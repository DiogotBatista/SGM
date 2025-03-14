from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class GestorOrSuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = False  # Impede a elevação direta da exceção

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name='Gestor').exists()

    def handle_no_permission(self):
        # Exibe uma mensagem de erro e redireciona para uma página segura, por exemplo, a home
        messages.warning(self.request, "Acesso não autorizado.")
        return redirect('index')


class GestorOrAlmoxarifeOrSuperuserRequidedMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = False  # Impede a elevação direta da exceção

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.groups.filter(name__in=['Gestor', 'Almoxarife']).exists()

    def handle_no_permission(self):
        # Exibe uma mensagem de erro e redireciona para uma página segura, por exemplo, a home
        messages.warning(self.request, "Acesso não autorizado.")
        return redirect('lista_materiais')