from django import forms
from .models import Roupa, Pedido
from django.forms import BaseFormSet, formset_factory

class RoupaForm(forms.ModelForm):
    class Meta:
        model = Roupa
        fields = '__all__'

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'

class ItemPedidoForm(forms.Form):
    roupa = forms.ModelChoiceField(queryset=Roupa.objects.none())
    quantidade = forms.IntegerField(min_value=1)

    def __init__(self, *args, **kwargs):
        usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        if usuario:
            self.fields['roupa'].queryset = Roupa.objects.filter(usuario=usuario)

class BaseItemPedidoFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def _construct_forms(self):
        self.forms = []
        for i in range(self.total_form_count()):
            self.forms.append(self._construct_form(i, usuario=self.usuario))

ItemPedidoFormSet = formset_factory(
    ItemPedidoForm,
    extra=3,
    formset=BaseItemPedidoFormSet
)
