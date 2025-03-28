from django.urls import path
from .views import  painel_relatorios

urlpatterns = [
    path('', painel_relatorios, name='painel_relatorios'),
]


