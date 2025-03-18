from django import forms
from .models import MovimentoItem, Movimentacao

class MovimentoItemEntradaForm(forms.ModelForm):
    class Meta:
        model = MovimentoItem
        # Campos que o usuário deve preencher; não incluímos 'tipo' pois ele será definido automaticamente
        fields = ['material', 'quantidade']
        labels = {
            'material': 'Material',
            'quantidade': 'Quantidade',
        }

    def save(self, commit=True):
        # Define o tipo de movimentação como "Entrada"
        self.instance.tipo = MovimentoItem.ENTRADA
        return super().save(commit=commit)


class MovimentoItemSaidaForm(forms.ModelForm):
    class Meta:
        model = MovimentoItem
        fields = ['material', 'quantidade']
        labels = {
            'material': 'Material',
            'quantidade': 'Quantidade',
        }


    def save(self, commit=True):
        # Define o tipo de movimentação como "Saída"
        self.instance.tipo = MovimentoItem.SAIDA
        return super().save(commit=commit)


class MovimentacaoEntradaForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['documento', 'observacoes']
        labels = {
            'documento': 'Documento de Origem',
            'observacoes': 'Observações',
        }
        help_texts = {
            'documento': 'Informe o documento de origem, ex: NF, devolução, etc.',
        }
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo "documento" obrigatório para entrada
        self.fields['documento'].required = True


class MovimentacaoSaidaForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['obra', 'observacoes']
        labels = {
            'obra': 'Obra',
            'observacoes': 'Observações',
        }
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Torna o campo "obra" obrigatório para saída
        self.fields['obra'].required = True

