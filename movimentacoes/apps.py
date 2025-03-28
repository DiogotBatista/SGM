from django.apps import AppConfig

class MovimentacoesConfig(AppConfig):
    name = 'movimentacoes'

    def ready(self):
        import movimentacoes.signals
