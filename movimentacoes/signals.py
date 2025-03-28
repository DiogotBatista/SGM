from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, DecimalField
from materiais.models import Material
from movimentacoes.models import MovimentoItem

@receiver(post_save, sender=MovimentoItem)
@receiver(post_delete, sender=MovimentoItem)
def update_material_quantity(sender, instance, **kwargs):
    material = instance.material
    # Soma as quantidades de entradas
    entradas = material.movimento_itens.filter(tipo=MovimentoItem.ENTRADA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    # Soma as quantidades de saídas
    saidas = material.movimento_itens.filter(tipo=MovimentoItem.SAIDA).aggregate(
        total=Sum('quantidade', output_field=DecimalField())
    )['total'] or 0
    # Calcula o saldo atual considerando o saldo_inicial
    novo_saldo = material.saldo_inicial + entradas - saidas
    # Atualiza o campo 'saldo_atual' sem chamar o método save() (para evitar loops de sinal)
    Material.objects.filter(pk=material.pk).update(saldo_atual=novo_saldo)
