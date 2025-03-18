# materiais/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, DecimalField
from materiais.models import Material
from .models import MovimentoItem

@receiver(post_save, sender=MovimentoItem)
@receiver(post_delete, sender=MovimentoItem)
def update_material_quantity(sender, instance, **kwargs):
    material = instance.material
    # Calcula a soma de entradas
    entradas = material.movimento_itens.filter(tipo=MovimentoItem.ENTRADA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    # Calcula a soma de saídas
    saidas = material.movimento_itens.filter(tipo=MovimentoItem.SAIDA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    # Atualiza a quantidade para o saldo atual (caso o saldo inicial seja zero)
    novo_saldo = entradas - saidas
    # Atualiza o campo sem chamar o método save() (para evitar loops de sinal)
    Material.objects.filter(pk=material.pk).update(quantidade=novo_saldo)
